# It turns out that 2,400,000 cells is too large for Google Docs & Excel.
import csv
import argparse

def analyze(csv_file):
  f = open(csv_file)
  lines = f.readlines()
  f.close()
  headers = lines.pop(0)
  messages = []
  for line in lines:
    name, email, year, age, replies, length = map(int, line.split(","))
    messages.append({"name": name, "email": email, "year": year, "age": age, "replies": replies, "length": length})
  print "Done parsing CSV {0} messages".format(len(messages))

  x_by_y(messages, "name", "year")
  x_by_y(messages, "email", "year")
  x_by_y(messages, "length", "year")
  x_by_y(messages, "name", "replies", 5)
  x_by_y(messages, "email", "replies", 5)
  x_by_y(messages, "length", "replies", 5)

def x_by_y(messages, x, y, max_y=None):
  x_totals = {}
  for m in messages:
    new_y = m[y]
    if max_y and new_y > max_y:
      new_y = max_y + 1
    if new_y not in x_totals:
      x_totals[new_y] = {"count": 0, "val": 0}
    x_totals[new_y]["val"] += m[x]
    x_totals[new_y]["count"] += 1

  data = []
  total_x, total_count = 0, 0
  for y_val in x_totals:
    totals = x_totals[y_val]
    data.append([y_val, float(totals["val"]) / totals["count"]])
    total_x += totals["val"]
    total_count += totals["count"]
  
  print "{0} total={1}, avg={2}".format(x, total_x, float(total_x)/total_count)
  write_csv("2ch_{0}_{1}.csv".format(x, y), (y, x), data)
  
def write_csv(fname, headers, list_of_lists):
  f = open(fname, 'wb')
  writer = csv.writer(f)
  writer.writerow(headers)
  for l in list_of_lists:
    writer.writerow(l)
  f.close()

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="2ch CSV analyzer")
  parser.add_argument('-c', '--csv-path', required=True)
  args = parser.parse_args()
  analyze(args.csv_path)
