import argparse
import csv
import MySQLdb
import subprocess
import urllib.request
import yaml

from collections import defaultdict

LEGISLATORS_URL = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml'

def main(dbname, dbuser, dbpasswd):
    mysqladmin = ['mysqladmin', '-u', dbuser, '-p'+dbpasswd]

    subprocess.run(mysqladmin + ['drop', dbname])
    subprocess.run(mysqladmin + ['create', dbname], check=True)
    with open('SD_DB_Setup.sql') as sql:
        subprocess.run(['mysql', '-u', dbuser, '-p'+dbpasswd, dbname], stdin=sql, check=True)

    with urllib.request.urlopen(LEGISLATORS_URL) as l:
        legislators = yaml.load(l)

    state_districts = defaultdict(list)
    for rep in legislators:
        term = rep['terms'][-1]
        if term['type'] == 'rep':
            state_districts[term['state']].append(term['district'])

    states = list(state_districts.keys())
    states.sort()
    ndtuples = []
    for state in states:
        districts = state_districts[state]
        districts.sort()
        for district in districts:
            ndtuples.append((1 + len(ndtuples), state, district, '%s-%s' % (state, district)))

    # TODO: read the values directly from the spreadsheet at
    # https://docs.google.com/spreadsheets/d/1jJs9h9ljSwp2VndX4lKztUBe3p4F6sGJV6TRrKSZuck/edit#gid=1538272940
    with open('voting_rights/voting_rights_2016.csv') as v:
        vr = csv.reader(v)
        header = next(vr)
        cols = str.join(', ', header)
        vrtuples = [row for row in vr]

    db = MySQLdb.connect(db=dbname, user=dbuser, passwd=dbpasswd, charset='utf8')
    cur = db.cursor()

    cur.execute('DELETE FROM national_districts')
    sql = ('INSERT INTO national_districts ' +
           ' (id, state, district, district_abbr) ' +
           ' VALUES (%s, %s, %s, %s)')
    cur.executemany(sql, ndtuples)

    cur.execute('DELETE FROM voting_rights')
    sql = ('INSERT INTO voting_rights (%s) VALUES (%s)' %
           (cols, str.join(', ', ('%s',) * len(header))))
    cur.executemany(sql, vrtuples)

    cur.execute('DELETE FROM pres_races')
    sql = ('INSERT INTO pres_races ' +
           ' (race_year, dem_candidate, rep_candidate, winning_party) ' +
           ' VALUES (%s, %s, %s, %s)')
    cur.executemany(sql,
                    [(2016,"Hillary Clinton","Donald Trump","R"),
                     (2012,"Barack Obama","Mitt Romney","D"),
                     (2008,"Barack Obama","John McCain","D"),
                     (2004,"John Kerry","George W. Bush","R"),
                     (2000,"Al Gore","George W. Bush","R"),
                     (1996,"Bill Clinton","Bob Dole","D"),
                     (1992,"Bill Clinton","George H. W. Bush","D"),
                     (1988,"Michael Dukakis","George H. W. Bush","R"),
                     (1984,"Walter Mondale","Ronald Reagan","R"),
                     (1980,"Jimmy Carter","Ronald Reagan","R")])

    db.commit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbname', default='SisterDistrict_dev')
    parser.add_argument('--dbuser', default='root')
    parser.add_argument('--dbpasswd')
    args = parser.parse_args()
    main(args.dbname, args.dbuser, args.dbpasswd)
