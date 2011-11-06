import glob
import os
import re
import time
import csv
from datetime import datetime

def analyze_nico():
  files = glob.glob(os.path.join("data/nico/", "*.data"))
  data, todo = [], []
  for i,fpath in enumerate(files):
    f = open(fpath, 'r')
    final_data, todo_data = data_parser(f.read(), fpath)
    data.append(final_data)
    todo.append(todo_data)
    f.close()

  scaled = scale(todo)
  for i in range(len(data)):
    data[i].extend(scaled[i])
  
  headers = ("length", "tags", "year", "comments", "views", "mylists")
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
    
    # divide comments, views, mylists by amount of time passed and video length 
    div = dist * length 
    return [length, int(tags), created_on.year], [float(comments)/div, float(views)/div, float(mylists)/div]
  
def scale(data):
  num_points = len(data[0])
  mins, maxes = [None]*num_points, [0]*num_points
  for d in data:
    for i,val in enumerate(d):
      if (not mins[i] or val < mins[i]) and mins[i] != 0:
        mins[i] = val
      if val > maxes[i]:
        maxes[i] = val

  scaled_data = []
  for d in data:
    scaled = []
    for i,val in enumerate(d):
      dist = float(val)
      # scale from 0-1, where 1 = highest activity, 0 = lowest
      scaled_dist = (dist - mins[i]) / (maxes[i] - mins[i])
      scaled.append(scaled_dist)
    scaled_data.append(scaled)
  return scaled_data

def write_csv(fname, headers, list_of_lists):
  f = open(fname, 'wb')
  writer = csv.writer(f)
  writer.writerow(headers)
  for l in list_of_lists:
    writer.writerow(l)
  f.close()

if __name__=="__main__":
  analyze_nico()
