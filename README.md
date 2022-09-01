# LIBJXL parallel compression/decompression runner

This project allows to perform image compress-decompress runs using different executables in parallel.

The main goal for that is to gather the compression/decompression results and stats
(i.e. ensure that lossless transcoding gives the expected result; be able to compare compression ratios and times).

## Executables

Different executables are to be stored under `executables/<version-name>` directory.
Initially, this repo contains two versions of libjxl:
1. `executables/libjxl` ([0103e5a901b776c46b55081fd6b647fbdd618472](https://github.com/libjxl/libjxl/tree/0103e5a901b776c46b55081fd6b647fbdd618472)) - plain libjxl
2. `executables/acp` ([806ffa55d9d0c2840ed7f8082d7a5b888980be5b](https://github.com/mkondratek/libjxl-ac-prediction/tree/806ffa55d9d0c2840ed7f8082d7a5b888980be5b)) - libjxl enhanced with AC prediction 

Each version directory contains both `cjxl` and `djxl` compile from a code of specific version.

## Before run

1. Add `cjxl` and `djxl` executables to `executables/<version-name>`
2. Add image data set directory into `data`

## Run

Use the Pycharm configuration specifying the data set dir as a parameter or execute:
```shell
python3 main.py data/<data-set-name>
```

## Results
The results are stores in timestamped directories.
Such a directory contains:
- `<version-name>` subdirectory with compressed and decompressed images
- `<version-name>-stats.csv` file with the run stats

## Stats file 

It looks like that.

|jpg_file_name                           |width|height|jpg_bytes|jpg_bpp            |jxl_bytes|jxl_bpp            |enc_time           |dec_time          |
|----------------------------------------|-----|------|---------|-------------------|---------|-------------------|-------------------|------------------|
|data/stock_snap/StockSnap_M7OOW736UB.jpg|5653 |3180  |2052294  |0.11416512855087797|1687329  |0.09386283456104456|0.39095234870910645|0.3856770992279053|
|data/stock_snap/StockSnap_WELQ7DLMJQ.jpg|6000 |4000  |21700445 |0.9041852083333334 |17807551 |0.7419812916666667 |0.9308886528015137 |3.791001319885254 |

## Program output 

Note that script output logs the start and end time of its run.
It also prints the overall execution time of each version executables. 
Here is an example output.

```
Start (1662053930)
Overall time for libjxl: 1.798s
Overall time for acp: 1.809s
Done (1662053932)
Diff (1.809s)
```