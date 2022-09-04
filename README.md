# LIBJXL parallel compression/decompression runner

This project allows to perform image compress-decompress runs using different executables in parallel.

The main goal for that is to gather the compression/decompression results and stats
(i.e. ensure that lossless transcoding gives the expected result; be able to compare compression ratios and times).

## Executables

Different executables are to be stored under `executables/<coder-name>` directory.
Initially, this repo contains two versions of libjxl and a few other image coders:

1. `executables/libjxl` ([7fada7a4061c979b1021068e0a1811c1eeadf0d7](https://github.com/libjxl/libjxl/tree/7fada7a4061c979b1021068e0a1811c1eeadf0d7))
    - plain libjxl
2. `executables/acp` ([7506630093ebe8227be40e98ec1299a681bd0888](https://github.com/mkondratek/libjxl-ac-prediction/tree/7506630093ebe8227be40e98ec1299a681bd0888))
    - libjxl enhanced with AC prediction
3. `executables/brunsli` ([300af107deecab45bec40c2df90611bb533b606b](https://github.com/google/brunsli/tree/300af107deecab45bec40c2df90611bb533b606b))
    - brunsli
4. `executables/brotli` ([9801a2c5d6c67c467ffad676ac301379bb877fc3](https://github.com/google/brotli/tree/9801a2c5d6c67c467ffad676ac301379bb877fc3))
    - brotli
5. `executables/lepton` ([429fe880d331b49a5be08b4d8dc762cbada6d4ca](https://github.com/dropbox/lepton/tree/429fe880d331b49a5be08b4d8dc762cbada6d4ca))
    - lepton

For libjxl-based coders each version directory contains **all build output** from a code of specific version.

## Run

Use the Pycharm configuration specifying the data set dir as a parameter or execute:

```shell
python3 main.py data/<data-set-name>
```

## Results

The results are stores in timestamped directories.
Such a directory contains:

- `<coder-name>` subdirectory with compressed and decompressed images
- `<coder-name>-stats.csv` file with the run stats

## Stats file

It looks like that.

|jpg_file_name                           |width|height|jpg_bytes|jpg_bpp            |compressed_bytes|compressed_bpp            |enc_time           |dec_time          |
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