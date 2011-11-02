import glob
import os
import re
import csv
from datetime import datetime
# Source: http://stackoverflow.com/questions/3217682/checking-validity-of-email-in-django-python
REGEX_EMAIL = re.compile("[\w\.-]+@[\w\.-]+\.\w{2,4}")

def analyze_2ch():
  files = glob.glob(os.path.join("data/2ch/", "*.data"))
  messages = {}
  num_messages = 0
  for i,fpath in enumerate(files):
    thread_id = fpath.split("_")[-1].split(".")[0]
    extracted = fpath.split("/")[-1].split("_")[0]
    time_extracted = datetime.strptime(extracted, "%Y%m%d%H%M%S")
    print i+1,"of",len(files),fpath
    f = open(fpath, 'r').read()
    messages[thread_id] = thread_parser(f)
    num_messages += len(messages[thread_id])
  print "Analyzed {0} messages".format(num_messages)

def thread_parser(raw_data):
  thread = []
  messages = raw_data.split("<dt>")
  messages.pop(0) # this first item is not a message
  for m in messages:
    meta, msg = m.split("<dd>")
    meta_data = meta_parser(meta)
    if not meta_data:
      continue
    data = message_parser(msg, meta_data)
    thread.append(data)
  return thread

# Parse message meta-data. Returns False if invalid.
def meta_parser(raw):
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
  
  name_string = "".join(meta[1:-1])
  name = name_string.split("<b>")[1].split("</b>")[0]
  email = REGEX_EMAIL.search(name_string)
  has_email = 1 if email else 0

  try:
    return {
      "id": message_id
      ,"datetime": datetime.strptime(date, "%Y/%m/%d %H:%M")
      ,"name": name
      ,"valid_email": has_email
    }
  except ValueError:
    # In one case, messages have an invalid date of "2006/03/32".
    return False

def message_parser(raw, data):
  msg = re.sub(r"<br><br> </dd>(</dl>)?", "", raw)
  msg = re.sub(r" <br> ", "", msg) # remove inline linebreaks
  msg = msg.strip()
  # TODO
  return data

def write_csv(fname, headers, list_of_lists):
  f = open(fname, 'wb')
  writer = csv.writer(f)
  writer.writerow(headers)
  for l in list_of_lists:
    writer.writerow(l)
  f.close()
  
if __name__=="__main__":
  analyze_2ch()