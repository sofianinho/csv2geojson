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
from tqdm import tqdm
import csv
from geojson import Point, Feature, FeatureCollection, dumps
from multiprocessing import Process, cpu_count
import os, shutil, subprocess, time

# I choose to have 3 times the number of cores as a basis for the max 
# number of processes to run the conversion task if the file size is important
# if the file is relatively small the min number is take. Small file is under 
# 10000 lines
FILE_SIZE_THRESHOLD = 10000
MAX_NB_PROCESS = cpu_count()*2
MIN_NB_PROCESS = 2

def nb_processes(nb_file_lines):
  """
  Returns MAX_NB_PROCESS if files_size > FILE_SIZE_THRESHOLD, MIN_NB_PROCESS otherwise

  :param nb_file_lines: number of lines in the file
  :param nb_file_lines: Integer
  :return: the number of processes to run to process the file
  :rtype: Integer
  """
  if nb_file_lines > MIN_NB_PROCESS*2 and nb_file_lines <= FILE_SIZE_THRESHOLD:
    return MIN_NB_PROCESS
  elif nb_file_lines <= MIN_NB_PROCESS*2:
    return 1
  return MAX_NB_PROCESS

def unitary_conversion(infile, start, stop, subOutFile, pb_pos=0):
  """
  Actually converts the csv entries to a geojson format
  
  :param infile: the inout file (the CSV)
  :param start: line number to start conversion
  :param stop: line number where to stop conversion
  :param subOutFile: output file (part of the resulting geojson)
  :param pb_pos: Progress bar position for tqdm
  :param infile: String
  :param start: Integer
  :param stop: Integer
  :param subOutFile: String
  :param pb_pos: Integer
  """
  with open(subOutFile, 'a') as dst:
    with open(infile, 'r') as src:
      reader = csv.DictReader(src)
      for i, row in tqdm(enumerate(reader), desc="Partial processing", unit="lines", total=((stop-start)+1), position=pb_pos):
        if i >= start and i <= stop:
          _p = Point((float(row['lon']), float(row['lat'])))
          _f = Feature(geometry=_p, properties={'radio':row['radio'],
                                                'mcc':row['mcc'],
                                                'net':row['net'],
                                                'area':row['area'],
                                                'cell':row['cell'],
                                                'unit':row['unit'],
                                                'range':row['range'],
                                                'samples':row['samples'],
                                                'changeable':row['changeable'],
                                                'created':row['created'],
                                                'updated':row['updated'],
                                                'averageSignal':row['averageSignal']}
                      )
          dst.write(dumps(_f, sort_keys=True)+',\n')
    src.close()
  dst.close()

def merge_results(listfiles, outfile,  pb_pos=0):
  """
  Merge a set of files into one 

  :param listFiles: The list of files to merge
  :param outfile: The output file
  :param pb_pos: Progress bar position for tqdm
  :param listFiles: list
  :param outfile: String
  :param pb_pos: Integer
  """
  with open(outfile, 'a') as dst:
    for k, v in tqdm(enumerate(listfiles), desc="Merging results", unit="files", position=pb_pos):
      #remove the last ',' in the last file, otherwise the JSON will not be correct
      if k != listfiles.index(listfiles[-1]) :
        with open(v, 'r') as src:
          shutil.copyfileobj(src, dst)
        src.close()
      else:
        # read the last file
        src = open(listfiles[-1], 'rw+')
        # go to the last line where the ','and the '\n' are
        src.seek(-len(','+os.linesep), os.SEEK_END)
        #remove the ',\n' characters
        src.write(' ')
        #close the file to take into account the modification
        src.close()
        #copy like previously
        with open(listfiles[-1], 'r') as src:
          shutil.copyfileobj(src, dst)
        src.close()
  dst.close()


def whole_convert(infile, outfile):
  """
  Converts the CSV entry into geojson using the files given

  :param infile: input file (the CSV)
  :param outfile: output file (the geojson)
  :type infile: String
  :type outfile: String
  """
  # In order to process the file among different processes, we will divide it
  # Total number of lines
  nb_lines = sum(1 for line in open(infile))
  # Total number of processes that will handle the file
  processes = nb_processes(nb_lines)
  # size of the processed portion per process
  step = (nb_lines/processes)
  start = 0
  # output files (one per subprocess)
  list_out_files = list()
  list_processes = list()
  try:
    # dispatch the job
    for i in range(processes):
      stop = start + step
      list_out_files.append(outfile+'.'+str(i))
      p = Process(target=unitary_conversion, args=[infile, start, stop, outfile+'.'+str(i)], kwargs={"pb_pos": i})
      start = stop + 1
      list_processes.append(p)
      p.start()
    # wait for completion
    for p in list_processes:
      p.join()
    # merge the results
    # 0- clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    # 1- the FeatureCollection part of the geojson
    with open(outfile, 'a') as dst:
      dst.write('{ "type": "FeatureCollection",\n"features": [\n')
    dst.close()
    # 2- the subparts of the converted source file
    merge_results(list_out_files, outfile) 
    #3- closing the geojson FeatureCollection property
    with open(outfile, 'a') as dst:
      dst.write('\n]\n}\n')
    dst.close()
    #4- deleting the sub files
    for f in list_out_files:
      os.remove(f)    
  except IOError as e:
    print "Error when handling the files. Details: "+str(e)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='csv2geojson utility v0.1, Author: Sofiane Imadali <sofianinho@gmail.com>')
    if arguments["--input"] is not None:
     print "Converting "+arguments["--input"]+" to geojson in the file: "+arguments["--output"]
     whole_convert(arguments["--input"], arguments["--output"])
     print "All done! Your output is in: "+arguments["--output"]
    else:
     print "\nYou must give an input file to convert. Try -h or --help option for help.\n"
     print(printable_usage(__doc__))
