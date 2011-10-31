#-*- encoding:utf-8 -*-
"""
Parse MBGA data to generate statistics.
"""
import glob
import os
import re
import csv
from datetime import datetime
DATA_PATH = "data/mbga/{0}/"
PERMISSIONS = {
  "メンバー全員": 1 # all members
  ,"主催者+副管理": 2 # sponsors and moderators
  ,"主催者のみ": 3 # sponsors
}

def analyze_groups():
  group_files = files('group', '*.data')
  groups = []
  min_dist, max_dist = None, 0
  for i in range(1, len(group_files), 2):
    n_members, permissions = parse(group_files[i-1], meta_parser)
    dist = parse(group_files[i], msg_parser)
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
    print members_dist,"->",scaled_members_dist
    groups[i][3] = scaled_members_dist
    
  print "n groups: {0}".format(len(groups))
  headers = ('n_members','permissions','distance','member_distance')
  write_csv('mbga_groups.csv', headers, groups)

def meta_parser(path, data):
  meta = re.findall("<li>([^<]+)</li>", data)
  meta = map(lambda x: x.split("：")[1], meta)
  # return [number of members, permissions]
  return int(meta[0].split("人")[0]), PERMISSIONS[meta[2]]

def msg_parser(path, data):
  dist = False # default if no messages posted
  msg = re.findall("<span class=\"timealert\"><span>([^>]+)</span>", data)
  if msg:
    extracted = path.split("/")[-1].split("_")[0]
    time_extracted = datetime.strptime(extracted, "%Y%m%d%H%M%S")
    oldest = datetime.strptime(msg[-1], "%Y/%m/%d %H:%M")
    dist = time_extracted - oldest #TODO to seconds
    dist = (dist.days * 86400) + dist.seconds
  return dist

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
  analyze_groups()
