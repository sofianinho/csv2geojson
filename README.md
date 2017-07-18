# A small utility to convert OpenCellID data from csv to geojson
This is a small python utility that converts CSV data extracted from OpenCellID to GeoJSON.
The program is very easily adaptable to other kinds of CSVs that you would wish to convert to geojson. This program takes advantage of multiprocessing and the cores available to it on your platform, which is especially useful if the dataset is huge.

# Using the utility
You must first install the dependencies (in a python virtualenv preferably).
```sh
pip install -r requirements.txt
```
You are already all set up. Try the provided example as follows:
```sh
python csv2geojson.py -i examples/test.csv -o /tmp/output.json
```
And then have a look at the generated /tmp/output.json. If no output file argument is given, a local "out.json" is created.

# Usage

```sh
Usage: csv2geojson.py -h
 csv2geojson.py [-i INPUT] [-o OUTPUT]
 csv2geojson.py --version
 csv2geojson.py --help | -h

Options:
 -i INPUT, --input INPUT       The CVS file to be converted   
 -o OUTPUT, --output OUTPUT      The GeoJSON file to write    [default: out.json]
 -h --help   Prints this help
 --version   Programme version
```

# Context
You might want to transform the data downloaded from OpenCellID in a csv format to GeoJSON to show on a map (geojson.io, for example). This is what I wanted, and made this modest utility that serves the purpose. If it's not the case for you, please put an issue, I will try to fix it if possible.

This utility takes advantage of the multiprocessing library in python to dispatch the conversion job among the available cores. If the number of threads is not enough for you, feel free to tweak the `MAX_NB_PROCESS` constant. This comes especially handy when the dataset is huge. The utility can still be used for smaller datasets though.

# License
The MIT License (MIT)

Copyright (c) 2017 sofianinho

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



