# PSD Module


**This module provides easy-to-use tools for quick data visualization and spectral
analysis.**

Data must be stored on text or Numpy files, and all formats compatible with
the standard `numpy.loadtxt` and `numpy.load` are accepted. First dimension, or
rows, is used for time and second dimension, or columns, for series. The first
column is always assumed to represent the times associated with each row.

## Installation

Make sure that Python 3 is available on your machine, and run

```shell
pip3 install psd
```

The package is also available at https://pypi.python.org/pypi?name=psd&version=1.0&:action=display.

## Getting Started

You can visualize time-series from Numpy or text files using
```python
psd --time-series my_file.npy another_file.txt ...
```

To compute Power Spectral Density (PSD) estimates for each series using the
[Welch method](https://en.wikipedia.org/wiki/Welch%27s_method), simply use
```python
psd my_file.npy
```

You can specify the number of rows at the top of the files you want to skip
using `-s SKIPROWS` option, the number of points per segment you want to use
with `-n NPERSEF` option, or the windowing function using `--window WINDOW`.

For time-series visualization and spectral analysis, you can hide the legend
with the `--no-legend` option, specify a title with `--title TITLE`, or save
the output as a text file, a Numpy file or an image using `-o OUTPUT`.

## Documentation

Other options are available, use `psd --help` to show documentation.

Developped by Jean-Baptiste Bayle (APC/CNES/CNRS), bayle@apc.in2p3.fr.
