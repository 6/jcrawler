#/usr/bin/python
#-*- encoding:utf-8 -*-
"""
Heavily based off code from: https://gist.github.com/405010 by Koutarou Chikuba
API docs: http://dic.nicovideo.jp/a/%E3%83%8B%E3%82%B3%E3%83%8B%E3%82%B3%E5%8B%95%E7%94%BBapi
"""
import argparse
import cgi
import cookielib
import urllib
import urllib2
import re
import sys
import random
from time import sleep
from xml.dom.minidom import parseString

def url_opener(username, password, ua):
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  opener.addheaders = [('User-agent', ua)]
  req = urllib2.Request("https://secure.nicovideo.jp/secure/login?site=niconico")
  account = {"mail": username, "password": password}
  req.add_data(urllib.urlencode(account.items()))
  opener.open(req)
  return opener

def xml_txt(dom, tag_name):
  return dom.getElementsByTagName(tag_name)[0].childNodes[0].nodeValue

def video_info(opener, v_id):
  res = opener.open("http://ext.nicovideo.jp/api/getthumbinfo/sm%s" % str(v_id))
  doc = res.read()
  dom = parseString(doc)
  status = dom.getElementsByTagName("nicovideo_thumb_response")[0].getAttribute("status")
  if status == "fail":
    return False # deleted/invalid video
  tags = dom.getElementsByTagName("tags")[0].getElementsByTagName("tag")
  tags_txt = [tag.childNodes[0].nodeValue for tag in tags]
  return [
    xml_txt(dom, "length")
    , xml_txt(dom, "first_retrieve")
    , int(xml_txt(dom, "comment_num"))
    , int(xml_txt(dom, "view_counter"))
    , int(xml_txt(dom, "mylist_counter"))
    , int(len(tags_txt))
  ]

def random_id_not_in(list):
  rand = False
  while not rand:
    rand = random.randrange(1, 15970606, 1)
    if rand in list:
      rand = False
  return rand

def main(howmany, email, password, ua):
  opener = url_opener(email, password, ua)
  tried_videos = [] # includes deleted/invalid videos
  visited_videos = []
  while len(visited_videos) < howmany:
    id = random_id_not_in(tried_videos)
    info = video_info(opener, id)
    print len(visited_videos), "ID:", id, "INFO:", info
    if info:
      info = map(str, info)
      with open("data/nico/{0}.data".format(id), 'w') as f:
        f.write('\n'.join(info))
      visited_videos.append(id)
    tried_videos.append(id)
    sleep(random.randrange(3, 8, 1))

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="Nico Nico Douga crawler")
  parser.add_argument('-e','--email', required=True)
  parser.add_argument('-p', '--password', required=True)
  parser.add_argument('-n', '--howmany', required=True, type=int)
  parser.add_argument('--useragent', required=True)
  args = parser.parse_args()
  main(args.howmany, args.email, args.password, args.useragent)
