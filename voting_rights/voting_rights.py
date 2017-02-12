import csv

out = open("voting_rights/voting_rights.sql", "w+")

out.write("USE sisterdistrict_dev;\n")
out.write("TRUNCATE TABLE voting_rights;\n")

voting_rights_2017 = csv.reader(open("./voting_rights/voting_rights_2017.csv"))
voting_rights_2017_header = next(voting_rights_2017)

for row in voting_rights_2017:
  columns = ",".join(voting_rights_2017_header)
  values = ",".join(['"' + col.replace('"', '\\"') + '"' for col in row])
  out.write("INSERT INTO voting_rights (" + columns + ") VALUES (" + values + ");\n")

out.close()