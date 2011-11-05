import glob
import os
import re
import time
import csv
from datetime import datetime

def analyze_nico():
  files = glob.glob(os.path.join("data/nico/", "*.data"))
  data = []
  for i,fpath in enumerate(files):
    f = open(fpath, 'r')
    data.append(data_parser(f.read(), fpath))
    f.close()
  headers = ("length", "comments", "views", "mylists", "tags")
  write_csv("nico.csv", headers, data)
    
def data_parser(raw, fpath):
    length_str, date_str, comments, views, mylists, tags = raw.split("\n")

    # video length in seconds: convert "1:23" -> 83 
    minutes, seconds = length_str.split(":")
    length = int(seconds) + (int(minutes) * 60)
    
    # distance between time extracted and time created in seconds
    created_on = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S+09:00")
    extracted_str = time.ctime(os.path.getmtime(fpath))
    extracted_on = datetime.strptime(extracted_str, "%a %b %d %H:%M:%S %Y")
    dist = extracted_on - created_on
    dist = (dist.days * 86400) + dist.seconds
    
    return [length, int(tags), float(comments)/dist, float(views)/dist, float(mylists)/dist]
  
def write_csv(fname, headers, list_of_lists):
  f = open(fname, 'wb')
  writer = csv.writer(f)
  writer.writerow(headers)
  for l in list_of_lists:
    writer.writerow(l)
  f.close()

if __name__=="__main__":
  analyze_nico()
