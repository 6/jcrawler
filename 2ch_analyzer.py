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
  print "Done parsing CSV"

  x_by_year(messages, "name")
  x_by_year(messages, "email")
  x_by_year(messages, "length")

def x_by_year(messages, x):
  x_year_totals = {}
  for m in messages:
    if m["year"] not in x_year_totals:
      x_year_totals[m["year"]] = {"count": 0, "val": 0}
    x_year_totals[m["year"]]["val"] += m[x]
    x_year_totals[m["year"]]["count"] += 1
  
  data = []
  total_x, total_count = 0, 0
  for year in x_year_totals:
    totals = x_year_totals[year]
    data.append([year, float(totals["val"]) / totals["count"]])
    total_x += totals["val"]
    total_count += totals["count"]
  
  print "{0} total={1}, avg={2}".format(x, total_x, float(total_x)/total_count)
  write_csv("2ch_{0}_year.csv".format(x), ("year", x), data)
  
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
