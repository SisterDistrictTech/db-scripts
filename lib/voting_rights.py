# Logic relating to the voting_rights db table.

import gspread
import oauth2client
import re

from oauth2client.service_account import ServiceAccountCredentials


VOTING_RIGHTS_SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1jJs9h9ljSwp2VndX4lKztUBe3p4F6sGJV6TRrKSZuck/edit#gid=1538272940'
VOTING_RIGHTS_EXPORT_WORKSHEET_NAME = 'Voter ID For Export'


class VotingRights:
    @staticmethod
    def setup(cur, googcreds):
        """
        Initial setup of the voting_rights table.
        WARNING: destroys any data present in voting_rights.

        Args:
          cur: a database cursor
          googcreds: path to a JSON file containing Google service-account credentials
        """
        creds = ServiceAccountCredentials.from_json_keyfile_name(googcreds,
                                                                 ['https://spreadsheets.google.com/feeds'])
        client = gspread.authorize(creds)
        ss = client.open_by_url(VOTING_RIGHTS_SPREADSHEET_URL)
        s = ss.worksheet(VOTING_RIGHTS_EXPORT_WORKSHEET_NAME)
        all_values = s.get_all_values()

        header = all_values[0]
        if any(re.search(r'\W', colname) for colname in header):
            raise 'Illegal SQL column name found among %r' % header

        cur.execute('DELETE FROM voting_rights')
        sql = ('INSERT INTO voting_rights (%s) VALUES (%s)' %
               (str.join(', ', header),
                str.join(', ', ('%s',) * len(header))))
        cur.executemany(sql, all_values[1:])
