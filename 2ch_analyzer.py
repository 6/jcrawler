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

  name_by_year(messages)

def name_by_year(messages):
  name_year_totals = {}
  for m in messages:
    if m["year"] not in name_year_totals:
      name_year_totals[m["year"]] = {"count": 0, "with_name": 0}
    if m["name"] == 1:
      name_year_totals[m["year"]]["with_name"] += 1
    name_year_totals[m["year"]]["count"] += 1
  
  data = []
  for year in name_year_totals:
    totals = name_year_totals[year]
    data.append([year, float(totals["with_name"]) / totals["count"]])
  
  write_csv("2ch_name_year.csv", ("year", "%name"), data)
  
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
