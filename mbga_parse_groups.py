#-*- encoding:utf-8 -*-
"""
Parse MBGA data to generate statistics.
"""
import glob
import os
import re
from datetime import datetime
DATA_PATH = "data/mbga/{0}/"
PERMISSIONS = {
  "メンバー全員": 1 # all members
  ,"主催者+副管理": 2 # sponsors and moderators
  ,"主催者のみ": 3 # sponsors
}

def analyze_groups():
  group_files = glob.glob(os.path.join(DATA_PATH.format('group'), '*.data'))
  groups = []
  for i in range(1, len(group_files), 2):
    meta = parse(group_files[i-1], meta_parser)
    msg = parse(group_files[i], msg_parser)
    groups.append({"meta":meta, "msg":msg})
  print "n groups: {0}".format(len(groups))

def meta_parser(data):
  meta = re.findall("<li>([^<]+)</li>", data)
  meta = map(lambda x: x.split("：")[1], meta)
  # return [number of members, permissions]
  return meta[0].split("人")[0], PERMISSIONS[meta[2]]

def msg_parser(data):
  messages = []
  msg = re.findall("<span class=\"timealert\"><span>([^>]+)</span>", data)
  for m in msg:
    messages.append(datetime.strptime(m, "%Y/%m/%d %H:%M"))
  return messages

def parse(data_path, parser):
  f = open(data_path, 'r').read()
  return parser(f)
  
if __name__=="__main__":
  analyze_groups()
