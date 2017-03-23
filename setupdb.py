import argparse
import MySQLdb
import platform
import subprocess

from sdlib.national_districts import NationalDistricts
from sdlib.pres_races import PresRaces
from sdlib.voting_rights import VotingRights


def main(dbname, dbuser, dbpasswd, googcreds, dbhost=None, dbport=None):
    createdb(dbname, dbuser, dbpasswd, dbhost=dbhost, dbport=dbport)

    db = MySQLdb.connect(db=dbname, user=dbuser, passwd=dbpasswd, charset='utf8')
    cur = db.cursor()

    NationalDistricts.populate(cur, reset=True)
    VotingRights.populate(cur, googcreds, reset=True)
    PresRaces.populate(cur, reset=True)

    db.commit()


def createdb(dbname, dbuser, dbpasswd, dbhost=None, dbport=None):
    mysql_args = ['-u', dbuser]
    if dbpasswd:
        # The -p argument needs to have the password attached to it or
        # else mysql and mysqladmin will try to prompt for the
        # password interactively.
        mysql_args.append('-p'+dbpasswd)

    if dbhost:
        mysql_args.extend(['-h', dbhost])
    if dbport:
        mysql_args.extend(['-P', str(dbport)])

    shell = platform.system() == 'Windows'

    # Delete the database first, if it exists. Failures here are ignored.
    subprocess.run(['mysqladmin'] + mysql_args + ['-f', 'drop', dbname], shell=shell)

    # Create the database.
    subprocess.run(['mysqladmin'] + mysql_args + ['create', dbname], shell=shell, check=True)

    # Set up the database schema.
    with open('SD_DB_Setup.sql') as sql:
        subprocess.run(['mysql'] + mysql_args + [dbname], stdin=sql, shell=shell, check=True)


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
    parser.add_argument('--dbhost',
                        help='MySQL server host.')
    parser.add_argument('--dbport', type=int,
                        help='MySQL server port.')
    args = parser.parse_args()
    main(args.dbname, args.dbuser, args.dbpasswd, args.googcreds,
         dbhost=args.dbhost, dbport=args.dbport)
