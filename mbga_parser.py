#-*- encoding:utf-8 -*-
"""
Parse MBGA data to generate statistics.
"""
import glob
import os
import re
import csv
import numpy
from PIL import Image
from datetime import datetime
DATA_PATH = "data/mbga/{0}/"
PERMISSIONS = {
  "メンバー全員": 1 # all members
  ,"主催者+副管理": 2 # sponsors and moderators
  ,"主催者のみ": 3 # sponsors
}
EMOTIONS = {
  "normal": 1
  ,"shy": 2
  ,"smile": 3
  ,"angry": 4
  ,"cry": 5
}

def analyze_groups():
  group_files = files('group', '*.data')
  groups = []
  min_dist, max_dist = None, 0
  for i in range(1, len(group_files), 2):
    n_members, permissions = parse(group_files[i-1], meta_parser)
    dist = parse(group_files[i], time_dist_parser)
    if dist and dist > max_dist:
      max_dist = dist
    if dist and (dist < min_dist or min_dist is None):
      min_dist = dist
    if not dist: dist = 0
    groups.append([n_members, permissions, dist])
  
  min_members_dist, max_members_dist = None, 0
  for i,g in enumerate(groups):
    if g[2] is 0:
      groups[i].append(0)
      continue
    n_members, dist = g[0], float(g[2])
    # scale from 0.01 (least activity) to 1.0 (most activity)
    scaled_dist = 1 - ((dist - min_dist) / (max_dist - min_dist) * 0.99)
    groups[i][2] = scaled_dist
    members_dist = scaled_dist / n_members
    groups[i].append(members_dist)
    if members_dist < min_members_dist or min_members_dist is None:
      min_members_dist = members_dist
    if members_dist > max_members_dist:
      max_members_dist = members_dist
  
  for i,g in enumerate(groups):
    if g[3] is 0: continue
    members_dist = g[3]
    scaled_members_dist = (members_dist - min_members_dist) / (max_members_dist - min_members_dist) * 0.99 + 0.01
    groups[i][3] = scaled_members_dist
    
  print "n groups: {0}".format(len(groups))
  headers = ('n_members','permissions','distance','member_distance')
  write_csv('mbga_groups.csv', headers, groups)

def meta_parser(path, data):
  meta = re.findall("<li>([^<]+)</li>", data)
  meta = map(lambda x: x.split("：")[1], meta)
  # return [number of members, permissions]
  return int(meta[0].split("人")[0]), PERMISSIONS[meta[2]]

def analyze_people():
  ids = people_ids()
  mins = {'diary':None, 'greet':None, 'disc':None, 'test':None}
  maxs = {'diary':0, 'greet':0, 'disc':0, 'test':0}
  people = []
  for i,id in enumerate(ids):
    # gather all data files associated with a specific person ID
    p_files = files('person', '*_{0}_*.data'.format(id))
    data = {}
    for f in p_files:
      ftype = f.split("_")[-1].split(".")[0]
      if ftype == "demo":
        data['age'] = parse(f, demographics_parser)
      elif ftype in ["diary","greet","disc","test"]:
        dist = parse(f, time_dist_parser)
        data[ftype] = dist
        if dist and (mins[ftype] is None or dist < mins[ftype]):
          mins[ftype] = dist
        if dist and dist > maxs[ftype]:
          maxs[ftype] = dist
    people.append(data)
  
  people_csv = []
  for i,person in enumerate(people):
    person_csv = []
    for dtype,value in person.items():
      if dtype == "age" or not value:
        if not value: value = 0
        person_csv.append((dtype, value))
        continue
      dist = float(value)
      scaled_dist = 1 - ((dist - mins[dtype])/(maxs[dtype] - mins[dtype])*0.99)
      person_csv.append((dtype, scaled_dist))
    person_csv.sort()
    people_csv.append(map(lambda x: x[-1], person_csv))
  headers = ('age', 'diary', 'disc', 'greet', 'intro')
  write_csv('mbga_people.csv', headers, people_csv)

def people_ids():
  people_files = files('person', '*.data')
  n_people = len(people_files)/7
  people_ids = []
  id_regex = re.compile("[0-9]+_([0-9]+)_[0-9]+")
  for f in people_files:
    m = id_regex.search(f)
    people_ids.append(m.group(1))
  return set(people_ids)

def demographics_parser(path, data):
  data = data.split("<dt>")
  age = -1
  for d in data:
    if d.startswith ("誕生日(年齢)"): # birthdate (age)
      age = re.findall("[0-9]+", re.findall("<dd>([^<]+)</dd>", d)[0])[-1]
  return age

def time_dist_parser(path, data):
  dist = False
  extracted = path.split("/")[-1].split("_")[0]
  time_extracted = datetime.strptime(extracted, "%Y%m%d%H%M%S") 
  dates = re.findall("[0-9]{4}/[0-9]+/[0-9]+ [0-9]+:[0-9]+", data)
  if dates:
    oldest = datetime.strptime(dates[-1], "%Y/%m/%d %H:%M")
    dist = time_extracted - oldest
    dist = (dist.days * 86400) + dist.seconds
  return dist

def analyze_avatars():
  avatars = files('avatar', '*.png')
  data = []
  for i,a in enumerate(avatars):
    pic = numpy.array(Image.open(a))
    num_black_pixels = len(numpy.where(pic[0:1][0:1] == 0)[0])
    bg_mod = 0 if num_black_pixels == 150 else 1
    emotion = a.split("/")[-1].split("_")[-1].split(".")[0]
    data.append([EMOTIONS[emotion], bg_mod])
  headers = ("emotion", "bg_mod")
  write_csv('mbga_avatars.csv', headers, data)
    
def parse(data_path, parser):
  f = open(data_path, 'r').read()
  return parser(data_path, f)
  
def files(folder, pattern):
  return glob.glob(os.path.join(DATA_PATH.format(folder), pattern))
  
def write_csv(fname, headers, list_of_lists):
  f = open(fname, 'wb')
  writer = csv.writer(f)
  writer.writerow(headers)
  for l in list_of_lists:
    writer.writerow(l)
  f.close()
  
if __name__=="__main__":
  #analyze_groups()
  #analyze_people()
  analyze_avatars()
