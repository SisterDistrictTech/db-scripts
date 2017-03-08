import argparse
import MySQLdb
import subprocess

from sdlib.national_districts import NationalDistricts
from sdlib.pres_races import PresRaces
from sdlib.voting_rights import VotingRights


def main(dbname, dbuser, dbpasswd, googcreds):
    createdb(dbname, dbuser, dbpasswd)

    db = MySQLdb.connect(db=dbname, user=dbuser, passwd=dbpasswd, charset='utf8')
    cur = db.cursor()

    NationalDistricts.populate(cur, reset=True)
    VotingRights.populate(cur, googcreds, reset=True)
    PresRaces.populate(cur, reset=True)

    db.commit()


def createdb(dbname, dbuser, dbpasswd):
    mysql_args = ['-u', dbuser]
    if dbpasswd:
        # The -p argument needs to have the password attached to it or
        # else mysql and mysqladmin will try to prompt for the
        # password interactively.
        mysql_args.append('-p'+dbpasswd)

    # Delete the database first, if it exists. Failures here are ignored.
    subprocess.run(['mysqladmin'] + mysql_args + ['-f', 'drop', dbname])

    # Create the database.
    subprocess.run(['mysqladmin'] + mysql_args + ['create', dbname], check=True)

    # Set up the database schema.
    with open('SD_DB_Setup.sql') as sql:
        subprocess.run(['mysql'] + mysql_args + [dbname], stdin=sql, check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbname', default='SisterDistrict_dev',
                        help='Name for the MySQL database.')
    parser.add_argument('--dbuser', default='root',
                        help='MySQL username.')
    parser.add_argument('--dbpasswd',
                        help='MySQL password for the MySQL user.')
    parser.add_argument('--googcreds',
                        help='Path to JSON file containing Google service-account credentials.')
    args = parser.parse_args()
    main(args.dbname, args.dbuser, args.dbpasswd, args.googcreds)
