#!/usr/bin/env python2
"""
Usage:  csv2geojson.py -h
 csv2geojson.py [-i INPUT] [-o OUTPUT]
 csv2geojson.py --version
 csv2geojson.py --help | -h

Options:
 -i INPUT, --input INPUT       The CVS file to be converted   
 -o OUTPUT, --output OUTPUT      The GeoJSON file to write    [default: out.json]
 -h --help   Prints this help
 --version   Programme version
"""

from docopt import docopt, printable_usage
import csv
from geojson import Point, Feature, FeatureCollection, dumps


def convert_me(infile, outfile):
 """
  Converts the CSV entry into geojson using the files given

  :param infile: input file (the CSV)
  :param outfile: output file (the geojson)
  :type infile: String
  :type outfile: String
  :return: True if the operation was successful
  :rtype: Boolean 
 """
 my_features=list()
 try:
  nb_lines = sum(1 for line in open(infile))
  with open(outfile, 'w') as outf:
   with open(infile, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    i=0.0
    for row in reader:
     my_point = Point((float(row['lon']),float(row['lat'])))
     my_feat=Feature(geometry=my_point, properties={'radio':row['radio'],'mcc':row['mcc'],'net':row['net'],'area':row['area'],'cell':row['cell'],'unit':row['unit'],'range':row['range'],'samples':row['samples'],'changeable':row['changeable'],'created':row['created'],'updated':row['updated'],'averageSignal':row['averageSignal']})
     my_features.append(my_feat)
     i+=1
     processed = int(((i/nb_lines))*100)
     if (processed%5 == 0):
      print "Processed "+str(processed)+" %"
   outf.write(dumps(FeatureCollection(my_features), sort_keys=True))
   csvfile.close()
  outf.close()
 except IOError as e:
  print "Error when handling the files. Details: "+str(e)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='csv2geojson utility v0.1, Author: Sofiane Imadali <sofianinho@gmail.com>')
    if arguments["--input"] is not None:
     print "Converting "+arguments["--input"]+" to geojson in the file: "+arguments["--output"]
     convert_me(arguments["--input"], arguments["--output"])
    else:
     print "\nYou must give an input file to convert. Try -h or --help option for help.\n"
     print(printable_usage(__doc__))
