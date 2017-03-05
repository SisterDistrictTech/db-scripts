import argparse
import MySQLdb
import subprocess

from lib.national_districts import NationalDistricts
from lib.pres_races import PresRaces
from lib.voting_rights import VotingRights


def main(dbname, dbuser, dbpasswd, googcreds):
    mysqladmin = ['mysqladmin', '-u', dbuser, '-p'+dbpasswd]

    subprocess.run(mysqladmin + ['-f', 'drop', dbname])
    subprocess.run(mysqladmin + ['create', dbname], check=True)
    with open('SD_DB_Setup.sql') as sql:
        subprocess.run(['mysql', '-u', dbuser, '-p'+dbpasswd, dbname], stdin=sql, check=True)

    db = MySQLdb.connect(db=dbname, user=dbuser, passwd=dbpasswd, charset='utf8')
    cur = db.cursor()

    NationalDistricts.setup(cur)
    VotingRights.setup(cur, googcreds)
    PresRaces.setup(cur)

    db.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbname', default='SisterDistrict_dev',
                        help='Name for the MySQL database')
    parser.add_argument('--dbuser', default='root',
                        help='MySQL username')
    parser.add_argument('--dbpasswd',
                        help='MySQL password for the MySQL user')
    parser.add_argument('--googcreds',
                        help='Path to JSON file containing Google service-account credentials.')
    args = parser.parse_args()
    main(args.dbname, args.dbuser, args.dbpasswd, args.googcreds)
