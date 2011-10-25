"""
Download the MBGA avatar images from links in the data directory.
"""
from time import sleep
from random import randrange
import os
import sys
import glob
import argparse

def avatar_info(path='data/mbga/person/'):
  info = []
  for f in glob.glob(os.path.join(path, '*_img.data')):
    name_parts = f.split("/")[-1].split("_")
    datetime, user_id = name_parts[0], name_parts[1]
    info.append({
      "save": "data/mbga/avatar/{0}_{1}.gif".format(datetime, user_id)
      , "url": open(f, 'r').read()
    })
  return info
  
def fetch(avatars, ua):
  total = len(avatars)
  for i, info in enumerate(avatars):
    os.system("curl -A \"{0}\" -o {1} {2}".format(ua,info["save"],info["url"]))
    print "{0} of {1}".format(i+1, total)
    sleep(randrange(2,4))

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="MBGA avatar fetcher")
  parser.add_argument('--useragent', required=True)
  args = parser.parse_args()
  fetch(avatar_info(), args.useragent)
