# A small utility to convert OpenCellID data from csv to geojson
This is a small python utility that converts CSV data extracted from OpenCellID to GeoJSON.
The program is very easily adaptable to other kinds of CSVs that you would wish to convert to geojson

# Using the utility
You must first install the dependencies (in a python virtualenv preferably).
```sh
pip install -r requirements.txt
```
You are already all set up. Try the provided example as follows:
```sh
python csv2geojson.py -i examples/test.csv 
```
And then have a look at the generated out.json 

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
You might want to transform the data downloaded from OpenCellID in a csv format to GeoJSON to show on a map (geojson.io, for example). This is what I wanted, and made this modest utility that serves the purpose, I think. If it's not the case for you, please put an issue, I will try to fix it if possible.

Special caution when using very large datasets, as the utility is really not optimized in terms of the used datastructures and the moments it writes in the output file. Very large dataset is 1 GB for example. Please tell me if encountered this need. Of course, no guarantee can be made here as stated in the license.


