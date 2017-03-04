import csv
import sys

out = open("voting_rights.sql", "w+")

print("TRUNCATE TABLE voting_rights;")

voting_rights_2016 = csv.reader(sys.stdin)
voting_rights_2016_header = next(voting_rights_2016)

columns = ",".join(voting_rights_2016_header)
for row in voting_rights_2016:
  values = ",".join(['"' + col.replace('"', '\\"') + '"' for col in row])
  # TODO: sanitize db input. remember little bobby tables...
  print("INSERT INTO voting_rights (%s) VALUES (%s)" % (columns, values))
