import copy
import csv
import hashlib
import os
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from os.path import basename
from typing import Callable

from PIL import Image


@dataclass
class Program:
    exec: str
    args: Callable[[str, str], list[int]]

    def cmd(self, i: str, o: str) -> list[str]:
        return [self.exec, *self.args(i, o)]


@dataclass
class EncoderAndDecoder:
    name: str
    encoder: Program
    decoder: Program


@dataclass
class CodersSet:
    libjxl: EncoderAndDecoder = EncoderAndDecoder(
        name='libjxl',
        encoder=Program(
            exec='executables/libjxl/cjxl',
            args=lambda i, o: ['--quiet', '--lossless_jpeg=1', i, o]
        ),
        decoder=Program(
            exec='executables/libjxl/djxl',
            args=lambda i, o: ['--quiet', i, o]
        )
    )

    acp: EncoderAndDecoder = EncoderAndDecoder(
        name='acp',
        encoder=Program(
            exec='executables/acp/cjxl',
            args=lambda i, o: ['--quiet', '--lossless_jpeg=1', i, o]
        ),
        decoder=Program(
            exec='executables/acp/djxl',
            args=lambda i, o: ['--quiet', i, o]
        )
    )

    brotli: EncoderAndDecoder = EncoderAndDecoder(
        name='brotli',
        encoder=Program(
            exec='executables/brotli/brotli',
            args=lambda i, o: [i, '-o', o]
        ),
        decoder=Program(
            exec='executables/brotli/brotli',
            args=lambda i, o: ['--decompress', i, '-o', o]
        )
    )

    brunsli: EncoderAndDecoder = EncoderAndDecoder(
        name='brunsli',
        encoder=Program(
            exec='executables/brunsli/cbrunsli',
            args=lambda i, o: [i,  o]
        ),
        decoder=Program(
            exec='executables/brunsli/dbrunsli',
            args=lambda i, o: [ i,  o]
        )
    )


    lepton: EncoderAndDecoder = EncoderAndDecoder(
        name='lepton',
        encoder=Program(
            exec='executables/lepton/lepton',
            args=lambda i, o: [i,  o]
        ),
        decoder=Program(
            exec='executables/lepton/lepton',
            args=lambda i, o: [ i,  o]
        )
    )

    @staticmethod
    def all():
        return [CodersSet.acp, CodersSet.libjxl, CodersSet.brotli, CodersSet.brunsli, CodersSet.lepton]


@dataclass
class ImageInfo:
    path: str
    width: int
    height: int
    bytes: int

    def bpp(self):
        return self.bytes / (self.width * self.height)


def compress_and_decompress(execs: EncoderAndDecoder, in_jpg_path: str, workdir_name: str, stats_writer):
    img_wd = basename(in_jpg_path).replace('.', '_')
    out_jxl_path = f'{workdir_name}/{img_wd}/output.jxl'
    out_jpg_path = f'{workdir_name}/{img_wd}/output.jpg'
    enc_cmd = execs.encoder.cmd(in_jpg_path, out_jxl_path)
    dec_cmd = execs.decoder.cmd(out_jxl_path, out_jpg_path)

    os.mkdir(f'{workdir_name}/{img_wd}')

    commands = [enc_cmd, dec_cmd]
    command_times: list[float] = []
    for command in commands:
        start_time = time.time()
        output = subprocess.check_output(command)
        end_time = time.time()
        command_times += [end_time - start_time]
        with open(f'{workdir_name}/{img_wd}/{basename(command[0])}-output.txt', 'wb') as f:
            f.write(output)

    data = get_csv_data(in_jpg_path, out_jxl_path, command_times[0], command_times[1])
    stats_writer.writerow(data)

    in_sha256 = get_sha256(in_jpg_path)
    out_sha256 = get_sha256(out_jpg_path)
    if in_sha256 != out_sha256:
        raise Exception(f'Checksum mismatch!\nInput image: {in_sha256}\nOutput image: {out_sha256}')


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


def run_for_exec(execs: EncoderAndDecoder, data: str, workdir: str):
    sub_wd = f'{workdir}/{execs.name}'
    os.mkdir(sub_wd)

    header = ['jpg_file_name', 'width', 'height', 'jpg_bytes', 'jpg_bpp', 'compressed_bytes', 'compressed_bpp', 'enc_time',
              'dec_time']
    with open(f'{sub_wd}-stats.csv', 'w', encoding='UTF8') as stats_file:
        stats_writer = csv.writer(stats_file)
        stats_writer.writerow(header)

        time_start = time.time()

        for jpg in os.listdir(data):
            if not jpg.endswith('.jpg'):
                continue
            compress_and_decompress(execs, f'{data}/{jpg}', sub_wd, stats_writer)

        time_end = time.time()
        print(f'Overall time for {execs.name}: {(time_end - time_start):.3f}s')


def main():
    data = sys.argv[1]

    start_time = time.time()
    workdir = str(int(start_time))
    os.mkdir(workdir)
    print(f'Start ({workdir})')

    execs_list = CodersSet.all()
    threads_list = []
    for execs in execs_list:
        thread = threading.Thread(target=run_for_exec, args=(execs, data, workdir))
        threads_list += [thread]
        thread.start()

    for thread in threads_list:
        thread.join()

    end_time = time.time()
    print(f'Done ({int(end_time)})')
    time_diff = end_time - start_time
    print(f'Diff ({time_diff:.3f}s)')


if __name__ == '__main__':
    main()
