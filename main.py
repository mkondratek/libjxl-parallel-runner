import csv
import os
import sys
import threading
import time
from os.path import basename

from commons import run_commands
from data import EncoderAndDecoder, CodersSet


def compress_and_decompress(execs: EncoderAndDecoder, in_jpg_path: str, workdir_name: str, stats_writer):
    img_wd = basename(in_jpg_path).replace('.', '_')
    out_jxl_path = f'{workdir_name}/{img_wd}/output.jxl'
    out_jpg_path = f'{workdir_name}/{img_wd}/output.jpg'
    enc_cmd = execs.encoder.cmd([in_jpg_path, out_jxl_path])
    dec_cmd = execs.decoder.cmd([out_jxl_path, out_jpg_path])

    os.mkdir(f'{workdir_name}/{img_wd}')
    img_wd_path = f'{workdir_name}/{img_wd}'

    commands = [enc_cmd, dec_cmd]
    run_commands(commands, img_wd_path, in_jpg_path, out_jpg_path, out_jxl_path, stats_writer)


def run_for_exec(execs: EncoderAndDecoder, data: str, workdir: str):
    sub_wd = f'{workdir}/{execs.name}'
    os.mkdir(sub_wd)

    header = ['jpg_file_name', 'width', 'height', 'jpg_bytes', 'jpg_bpp', 'compressed_bytes', 'compressed_bpp',
              'enc_time',
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
