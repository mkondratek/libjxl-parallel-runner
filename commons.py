import copy
import hashlib
import os
import subprocess
import time
from os.path import basename

from PIL import Image

from data import ImageInfo


def get_csv_data(in_jpg_path: str, out_jxl_path: str, enc_time: float, dec_time: float) -> list:
    jpg_image_info = get_image_info(in_jpg_path)
    jxl_image_info = copy.copy(jpg_image_info)
    jxl_image_info.path = out_jxl_path
    jxl_image_info.bytes = os.path.getsize(out_jxl_path)
    data = [jpg_image_info.path, jpg_image_info.width, jpg_image_info.height, jpg_image_info.bytes,
            jpg_image_info.bpp(), jxl_image_info.bytes, jxl_image_info.bpp(), enc_time, dec_time]
    return data


def get_image_info(img_path) -> ImageInfo:
    image = Image.open(img_path)
    width, height = image.size
    return ImageInfo(img_path, width, height, os.path.getsize(img_path))


def get_sha256(file) -> str:
    BUF_SIZE: int = 65536
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


def run_commands(commands, img_wd_path, in_jpg_path, out_jpg_path, out_jxl_path, stats_writer):
    command_times: list[float] = []
    for command in commands:
        start_time = time.time()
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end_time = time.time()
        command_times += [end_time - start_time]
        with open(f'{img_wd_path}/{basename(command[0])}-stdout.txt', 'wb') as f:
            f.write(process.stdout)
        with open(f'{img_wd_path}/{basename(command[0])}-stderr.txt', 'wb') as f:
            f.write(process.stderr)
    data = get_csv_data(in_jpg_path, out_jxl_path, command_times[0], command_times[1])
    stats_writer.writerow(data)
    in_sha256 = get_sha256(in_jpg_path)
    out_sha256 = get_sha256(out_jpg_path)
    if in_sha256 != out_sha256:
        raise Exception(f'Checksum mismatch ({img_wd_path})!\nInput image: {in_sha256}\nOutput image: {out_sha256}')
