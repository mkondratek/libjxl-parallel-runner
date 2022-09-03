import copy
import hashlib
import os

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
