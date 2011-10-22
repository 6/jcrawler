#/usr/bin/python
#-*- encoding:utf-8 -*-
"""
Heavily based off code from: https://gist.github.com/405010 by Koutarou Chikuba
"""
import argparse
import cgi
import cookielib
import urllib
import urllib2
import re
import sys
from time import sleep

def url_opener(username, password):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #opener.addheaders = [('User-agent', 'Mozilla/5.0 ABCDEF')]
    req = urllib2.Request("https://secure.nicovideo.jp/secure/login?site=niconico");
    account = {"mail": username, "password": password}
    req.add_data(urllib.urlencode(account.items()))
    opener.open(req)
    return opener
    
def get_comments(opener, video_id):
    res = opener.open("http://www.nicovideo.jp/api/getflv.php?v=%s" % video_id)
    doc = res.read()

    #POSTするXMLを作る
    thread_id = re.findall("(?<=thread_id=)[0-9]+",doc)[0]
    send_xml = '<thread res_from="-300" version="20061206" thread="%s" />'% thread_id

    #コメントダウンロード用のurl (エスケープされている)
    _tmp =re.findall("((?<=ms=)http.*?api)",doc)
    ms_num = re.findall(r"(?<=2F)[0-9]+",_tmp[0])
    url="http://msg.nicovideo.jp/%s/api/" % ms_num[0]

    res = opener.open(url,data=send_xml )
    doc = res.read()
    print doc
    
    comments = []
    for i in re.findall("<chat.*?>.*?</chat>",doc):
        raw_comment = re.sub("<.*?>","",i)
        comments.append(raw_comment)
    return comments

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="Nico Nico Douga crawler")
  parser.add_argument('-e','--email', required=True)
  parser.add_argument('-p', '--password', required=True)
  args = parser.parse_args()
  print get_comments(url_opener(args.email, args.password), "sm1966768")