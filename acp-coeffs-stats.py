import csv
import os
import sys
import time
from os.path import basename

import numpy as np

import matplotlib.pyplot as plt


def read_col(csv_file_path: str, field: str, atype: type):
    with open(csv_file_path, 'r', encoding='UTF8') as file:
        header = file.readline().strip().split(',')
        field_idx = header.index(field)
        return [atype(r[field_idx]) for r in csv.reader(file)]


def main():
    results_path = sys.argv[1].removesuffix('/')
    selected_field = 'compressed_bpp'

    start_time = time.time()
    wd = results_path.replace('.', '_').replace('/', '_')
    print(f'Start ({start_time})')

    title = np.array([f for f in os.listdir(results_path) if f.endswith('.TITLE')])[0]
    title = basename(title).removesuffix('.TITLE')

    listdir = np.array([f for f in os.listdir(results_path) if f.endswith('.csv')])
    plt_data = np.zeros((len(listdir)))
    for i, result_file in enumerate(listdir):
        col = read_col(f'{results_path}/{result_file}', selected_field, atype=float)
        plt_data[i] = sum(col) / len(col)

    sort_idx = np.argsort(plt_data)
    listdir = listdir[sort_idx]
    plt_data = plt_data[sort_idx]

    all_zeros_idx = np.where(listdir == 'acp-coeffs-all-zeros_txt-stats.csv')
    all_zeros_idx = all_zeros_idx[0][0]

    index_min = min(range(len(plt_data)), key=plt_data.__getitem__)
    plt.title(f'Average {selected_field} by {results_path} results and {title} dataset\n'
              f'from ACP runs with different coefficients')
    plt.plot(plt_data, listdir, 'k.')
    plt.plot(plt_data[all_zeros_idx], listdir[all_zeros_idx], 'ro')
    plt.plot(plt_data[index_min], listdir[index_min], 'go')

    plt.annotate(f'{plt_data[all_zeros_idx]:.5f}', (plt_data[all_zeros_idx], listdir[all_zeros_idx]),
                 textcoords='offset points', xytext=(-100, -10), arrowprops=dict(arrowstyle="->",
                                                                                 connectionstyle="arc3,rad=.2"))
    plt.annotate(f'{plt_data[index_min]:.5f}', (plt_data[index_min], listdir[index_min]),
                 textcoords='offset points', xytext=(-5, 50), arrowprops=dict(arrowstyle="->",
                                                                              connectionstyle="arc3,rad=.2"))

    plt.yticks(fontsize=6)
    plt.savefig(f'{wd}-stats.png', bbox_inches='tight', dpi=300)
    plt.clf()

    end_time = time.time()
    print(f'Done ({int(end_time)})')
    time_diff = end_time - start_time
    print(f'Diff ({time_diff:.3f}s)')


if __name__ == '__main__':
    main()
