"""
Parse MBGA data to generate statistics.
"""
import glob
import os
DATA_PATH = "data/mbga/{0}/"

def analyze_groups():
  group_files = glob.glob(os.path.join(DATA_PATH.format('group'), '*.data'))
  groups = []
  for i in range(1, len(group_files), 2):
    meta = parse(group_files[i-1], meta_parser)
    msg = parse(group_files[i], msg_parser)
    groups.append({"meta":meta, "msg":msg})
  print "n groups: {0}".format(len(groups))

def meta_parser(data):
  return [] # TODO

def msg_parser(data):
  return [] # TODO

def parse(data_path, parser):
  f = open(data_path, 'r').read()
  return parser(f)
  
if __name__=="__main__":
  analyze_groups()
