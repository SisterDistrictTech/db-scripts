# Logic relating to the voting_rights db table.

import gspread
import oauth2client
import re

from oauth2client.service_account import ServiceAccountCredentials


VOTING_RIGHTS_SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1jJs9h9ljSwp2VndX4lKztUBe3p4F6sGJV6TRrKSZuck/edit#gid=1538272940'
VOTING_RIGHTS_EXPORT_WORKSHEET_NAME = 'Voter ID For Export'


class VotingRights:
    @staticmethod
    def populate(cur, googcreds, reset=False):
        """
        Load data into the voting_rights table.

        Args:
          cur: a database cursor
          googcreds: path to a JSON file containing Google service-account credentials
          reset: whether to empty the table before populating it (warning!)
        """
        creds = ServiceAccountCredentials.from_json_keyfile_name(googcreds,
                                                                 ['https://spreadsheets.google.com/feeds'])
        client = gspread.authorize(creds)
        ss = client.open_by_url(VOTING_RIGHTS_SPREADSHEET_URL)
        s = ss.worksheet(VOTING_RIGHTS_EXPORT_WORKSHEET_NAME)
        all_values = s.get_all_values()

        # all_values[0] is the header row, from which we draw the db column names.
        # all_values[1:] are the data rows.

        header = all_values[0]

        # Check that the column names are valid SQL identifiers and
        # not some injection attack a la https://xkcd.com/327/
        if any(re.search(r'\W', colname) for colname in header):
            raise 'Illegal SQL column name found among %r' % header

        if reset:
            cur.execute('DELETE FROM voting_rights')

        sql = ('INSERT INTO voting_rights (%s) VALUES (%s)' %
               (str.join(', ', header),
                str.join(', ', ('%s',) * len(header))))
        cur.executemany(sql, all_values[1:])
