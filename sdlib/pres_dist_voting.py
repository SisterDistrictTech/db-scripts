# Logic relating to the pres_dist_voting db table.

import gspread
import oauth2client

from oauth2client.service_account import ServiceAccountCredentials


DAILY_KOS_MEMBER_GUIDE_SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1NEs7XIHMFNIuXq4JknF67Krdz0LksrEtRG9F2HgIxmU/edit#gid=2132957126'
DAILY_KOS_MEMBER_GUIDE_EXPORT_WORKSHEET_NAME = 'House'

# Note - The Spreadsheet used here is a copy of the original that's been added to the Sister District Data and Research folder.
# The original spreadsheet is here - https://docs.google.com/spreadsheets/d/1oRl7vxEJUUDWJCyrjo62cELJD2ONIVl-D9TSUKiK9jk.


def toFloat(str):
  return float(str.replace(',',''))

# 'Daily Kos uses -AL to refer to At Large Districts. Sister District uses -00'
def normalizeDistrictAbbreviations(str):
  if str[-2:] == 'AL':
      return str[:-2] + '00'
  else:
      return str

# The structure of the Daily Kos spreadsheet isn't very normalized. I've decided to use the hardcoded column
# indexes. Before processing the spreadsheet, I confirm that the column labels haven't changed.
relevant_columns = {
    'CODE': {'row_0_idx': 1, 'row_0_lbl': 'Code', 'row_1_idx': 1, 'row_1_lbl': ''},
    'DEM_PCT_16': {'row_0_idx': 18, 'row_0_lbl': '2016 President', 'row_1_idx': 18, 'row_1_lbl': 'Clinton'},
    'REP_PCT_16': {'row_0_idx': 18, 'row_0_lbl': '2016 President', 'row_1_idx': 19, 'row_1_lbl': 'Trump'},
    'DEM_NUM_16': {'row_0_idx': 59, 'row_0_lbl': '2016 President', 'row_1_idx': 60, 'row_1_lbl': 'Clinton'},
    'REP_NUM_16': {'row_0_idx': 59, 'row_0_lbl': '2016 President', 'row_1_idx': 61, 'row_1_lbl': 'Trump'},
    'DEM_PCT_12': {'row_0_idx': 22, 'row_0_lbl': '2012 President', 'row_1_idx': 22, 'row_1_lbl': 'Obama'},
    'REP_PCT_12': {'row_0_idx': 22, 'row_0_lbl': '2012 President', 'row_1_idx': 23, 'row_1_lbl': 'Romney'},
    'DEM_NUM_12': {'row_0_idx': 62, 'row_0_lbl': '2012 President', 'row_1_idx': 63, 'row_1_lbl': 'Obama'},
    'REP_NUM_12': {'row_0_idx': 62, 'row_0_lbl': '2012 President', 'row_1_idx': 64, 'row_1_lbl': 'Romney'},
    'DEM_PCT_08': {'row_0_idx': 26, 'row_0_lbl': '2008 President', 'row_1_idx': 26, 'row_1_lbl': 'Obama'},
    'REP_PCT_08': {'row_0_idx': 26, 'row_0_lbl': '2008 President', 'row_1_idx': 27, 'row_1_lbl': 'McCain'},
    'DEM_NUM_08': {'row_0_idx': 65, 'row_0_lbl': '2008 President Two-Party', 'row_1_idx': 66, 'row_1_lbl': 'Obama'},
    'REP_NUM_08': {'row_0_idx': 65, 'row_0_lbl': '2008 President Two-Party', 'row_1_idx': 67, 'row_1_lbl': 'McCain'}
}

class PresDistVoting:
    @staticmethod
    def populate(cur, googcreds, reset=False):
        """
        Load data into the pres_dist_voting table.

        Args:
          cur: a database cursor
          googcreds: path to a JSON file containing Google service-account credentials
          reset: whether to empty the table before populating it (warning!)
        """
        creds = ServiceAccountCredentials.from_json_keyfile_name(googcreds,
                                                                 ['https://spreadsheets.google.com/feeds'])
        client = gspread.authorize(creds)
        ss = client.open_by_url(DAILY_KOS_MEMBER_GUIDE_SPREADSHEET_URL)
        s = ss.worksheet(DAILY_KOS_MEMBER_GUIDE_EXPORT_WORKSHEET_NAME)
        all_values = s.get_all_values()

        # Ensure that the column headers in the spreadsheet are what we expect.
        for key, val in relevant_columns.items():
            if (all_values[0][val['row_0_idx']] != val['row_0_lbl'] or
              all_values[1][val['row_1_idx']] != val['row_1_lbl']):
                raise ValueError('Structure of spreadsheet has changed. Script needs modification')

        # Retrieve the indexes that will be used to extract data from the spreadsheet.
        district_col_index = relevant_columns['CODE']['row_1_idx']
        dem_pct_16_col_index = relevant_columns['DEM_PCT_16']['row_1_idx']
        rep_pct_16_col_index = relevant_columns['REP_PCT_16']['row_1_idx']
        dem_num_16_col_index = relevant_columns['DEM_NUM_16']['row_1_idx']
        rep_num_16_col_index = relevant_columns['REP_NUM_16']['row_1_idx']
        dem_pct_12_col_index = relevant_columns['DEM_PCT_12']['row_1_idx']
        rep_pct_12_col_index = relevant_columns['REP_PCT_12']['row_1_idx']
        dem_num_12_col_index = relevant_columns['DEM_NUM_12']['row_1_idx']
        rep_num_12_col_index = relevant_columns['REP_NUM_12']['row_1_idx']
        dem_pct_08_col_index = relevant_columns['DEM_PCT_08']['row_1_idx']
        rep_pct_08_col_index = relevant_columns['REP_PCT_08']['row_1_idx']
        dem_num_08_col_index = relevant_columns['DEM_NUM_08']['row_1_idx']
        rep_num_08_col_index = relevant_columns['REP_NUM_08']['row_1_idx']

        # Build an array of values to insert into the database.
        pres_dist_votes = []
        for row in all_values[3:]:
            pres_dist_votes.append((2016,
                                    normalizeDistrictAbbreviations(row[district_col_index]),
                                    toFloat(row[dem_pct_16_col_index]),
                                    toFloat(row[rep_pct_16_col_index]),
                                    toFloat(row[dem_num_16_col_index]),
                                    toFloat(row[rep_num_16_col_index])))
            pres_dist_votes.append((2012,
                                    normalizeDistrictAbbreviations(row[district_col_index]),
                                    toFloat(row[dem_pct_12_col_index]),
                                    toFloat(row[rep_pct_12_col_index]),
                                    toFloat(row[dem_num_12_col_index]),
                                    toFloat(row[rep_num_12_col_index])))
            pres_dist_votes.append((2008,
                                    normalizeDistrictAbbreviations(row[district_col_index]),
                                    toFloat(row[dem_pct_08_col_index]),
                                    toFloat(row[rep_pct_08_col_index]),
                                    toFloat(row[dem_num_08_col_index]),
                                    toFloat(row[rep_num_08_col_index])))

        if reset:
            cur.execute('DELETE FROM pres_dist_voting')

        # insert the contents of pres_dist_votes into the pres_dist_votes table.
        sql = "CALL insert_into_pres_dist_voting(%s, %s, %s, %s, %s, %s);"
        cur.executemany(sql, pres_dist_votes)
