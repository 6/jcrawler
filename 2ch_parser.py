import glob
import os
import re
import csv
import operator
from datetime import datetime
# Source: http://stackoverflow.com/questions/3217682/checking-validity-of-email-in-django-python
REGEX_EMAIL = re.compile("[\w\.-]+@[\w\.-]+\.\w{2,4}")

def analyze_2ch():
  files = glob.glob(os.path.join("data/2ch/", "*.data"))
  messages = {}
  num_messages = 0
  for i,fpath in enumerate(files):
    thread_id = fpath.split("_")[-1].split(".")[0]
    extracted_on = fpath.split("/")[-1].split("_")[0]
    extracted_on = datetime.strptime(extracted_on, "%Y%m%d%H%M%S")
    print i+1,"of",len(files),fpath
    f = open(fpath, 'r').read()
    messages[thread_id] = thread_parser(f, extracted_on)
    num_messages += len(messages[thread_id])
  print "Analyzed {0} messages".format(num_messages)
  
  visited = []
  for fpath in files:
    # determine default "anonymous" name (varies by board/subdomain)
    key = fpath.split("_")
    key = "{0}_{1}".format(key[1], key[2])
    if key in visited:
      continue
    visited.append(key)
    threads = glob.glob(os.path.join("data/2ch/", "*_{0}_*.data".format(key)))
    names = {}
    for t in threads:
      thread_id = t.split("_")[-1].split(".")[0]
      for m in messages[thread_id]:
        if m["name"] not in names:
          names[m["name"]] = 1
        else:
          names[m["name"]] += 1
    sorted_names = sorted(names.iteritems(), key=operator.itemgetter(1))
    default_name = sorted_names[-1][0]
    
    # convert name string --> bool: if user has custom name or just "anonymous"
    for t in threads:
      thread_id = t.split("_")[-1].split(".")[0]
      for i,m in enumerate(messages[thread_id]):
        has_custom_name = 0 if m["name"] == default_name else 1
        messages[thread_id][i]["name"] = has_custom_name
  
  # convert dict into a list so can write to CSV
  message_data = []
  for thread_id in messages:
    for m in messages[thread_id]:
      message_data.append([m["name"], m["valid_email"], m["year"], m["age"], m["replies"], m["length"]])
  
  headers = ("name", "email", "year", "age", "replies", "length")
  write_csv("2ch.csv", headers, message_data)

def thread_parser(raw_data, extracted_on):
  thread = []
  messages = raw_data.split("<dt>")
  messages.pop(0) # this first item is not a message
  for m in messages:
    meta, msg = m.split("<dd>")
    meta_data = meta_parser(meta, extracted_on)
    if not meta_data:
      continue
    data, reply_to = message_parser(msg, meta_data)
    for message_id in reply_to:
      for i,msg in enumerate(thread):
        if msg["id"] == message_id:
          thread[i]["replies"] += 1
          break
    thread.append(data)
  return thread

# Parse message meta-data. Returns False if invalid.
def meta_parser(raw, extracted_on):
  meta = re.sub(r" (ID:[^<]+)?</dt>", "", raw)
  meta = meta.split("\x81F") # Shift-JIS colon character
  message_id = int(meta[0].strip())
  
  date = re.sub(r"\([^)]+\)", "", meta[-1]) # remove day of the week
  m = re.search("([0-9]{2,4})(/[0-9]{1,2}/[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2})", date)
  if m:
    date = m.group(0)
    if m.group(1).startswith("0"):
      # messages ~2005 and before have abbreviated year (ex: 05 instead of 2005)
      date = "20"+m.group(1)+m.group(2)
  else:
    # When message is deleted, the date is deleted as well.
    return False
  try:
    created_on = datetime.strptime(date, "%Y/%m/%d %H:%M")
  except ValueError:
    # In one case, messages have an invalid date of "2006/03/32".
    return False
    
  age = extracted_on - created_on
  est_jst_diff = 13*60*60 # time diff between EST and Japan time (13 hours)
  age = (age.days * 86400) + age.seconds + est_jst_diff
  if age < 0:
    # in one case, an invalid date lists the year as "2665"
    return False
  
  name_string = "".join(meta[1:-1])
  name = name_string.split("<b>")[1].split("</b>")[0]
  email = REGEX_EMAIL.search(name_string)
  has_email = 1 if email else 0

  return {
    "id": message_id
    ,"year": created_on.year
    ,"age": age
    ,"name": name
    ,"valid_email": has_email
    ,"replies": 0
  }

def message_parser(raw, data):
  msg = re.sub(r"<br><br> </dd>(</dl>)?", "", raw)
  msg = re.sub(r" <br> ", "", msg) # remove inline linebreaks
  msg = msg.strip()
  data["length"] = len(msg)  
  
  reply_to = re.findall("read.cgi/[^/]+/[0-9]+/([0-9]+)", msg)
  reply_to = map(int, list(set(reply_to)))
  # remove invalid replies to comments that haven't been posted yet
  reply_to = [r for r in reply_to if r < data["id"]]
  
  return [data, reply_to]

def write_csv(fname, headers, list_of_lists):
  f = open(fname, 'wb')
  writer = csv.writer(f)
  writer.writerow(headers)
  for l in list_of_lists:
    writer.writerow(l)
  f.close()
  
if __name__=="__main__":
  analyze_2ch()