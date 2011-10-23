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

def url_opener(username, password):
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  #opener.addheaders = [('User-agent', 'Mozilla/5.0 ABCDEF')]
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
  return {
    "length": xml_txt(dom, "length")
    , "comment_count": xml_txt(dom, "comment_num")
    , "view_count": xml_txt(dom, "view_counter")
    , "mylist_count": xml_txt(dom, "mylist_counter")
    , "tags": tags_txt
    , "title": xml_txt(dom, "title")
    , "description": xml_txt(dom, "description")
    , "upload_date": xml_txt(dom, "first_retrieve")
  }
    
def thread_info(opener, v_id):
  res = opener.open("http://www.nicovideo.jp/api/getflv.php?v=sm%s" % str(v_id))
  doc = res.read()
  #コメントダウンロード用のurl (エスケープされている)
  _tmp =re.findall("((?<=ms=)http.*?api)", doc)
  return {
    "id": re.findall("(?<=thread_id=)[0-9]+",doc)[0]
    , "ms_num": re.findall(r"(?<=2F)[0-9]+",_tmp[0])[0]
  }

def comments(opener, thread_info):
  send_xml = '<thread res_from="-300" version="20061206" thread="%s" />'% thread_info["id"]
  url="http://msg.nicovideo.jp/%s/api/" % thread_info["ms_num"]
  res = opener.open(url,data=send_xml)
  doc = res.read()
  
  comments = []
  for i in re.findall("<chat.*?>.*?</chat>",doc):
    raw_comment = re.sub("<.*?>","",i)
    comments.append(raw_comment)
  return comments

def random_id_not_in(list):
  rand = False
  while not rand:
    rand = random.randrange(1, 15970606, 1)
    if rand in list:
      rand = False
  return rand

def main(howmany, email, password):
  opener = url_opener(email, password)
  tried_videos = [] # includes deleted/invalid videos
  visited_videos = []
  while len(visited_videos) < howmany:
    id = random_id_not_in(tried_videos)
    info = video_info(opener, id)
    print id, info
    if info:
      t_info = thread_info(opener, id)
      c = comments(opener, t_info)
      visited_videos.append(id)
    tried_videos.append(id)
    sleep(random.randrange(3, 8, 1))

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="Nico Nico Douga crawler")
  parser.add_argument('-e','--email', required=True)
  parser.add_argument('-p', '--password', required=True)
  parser.add_argument('-n', '--howmany', required=True, type=int)
  args = parser.parse_args()
  main(args.howmany, args.email, args.password)