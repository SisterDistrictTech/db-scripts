import gspread
import argparse
from oauth2client.service_account import ServiceAccountCredentials

parser = argparse.ArgumentParser()
parser.add_argument("servicekey", help="path to service key with permissions to access Sister District Google Spreadsheets")
args = parser.parse_args()

# Configuration. This will change if you want to connect to a different spreadsheet.
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1y2BGrzw8wDSIyjqBgir31z7Oj7AcX7eFjZmO8y4fcQc/edit#gid=426322475'
sheet_name = 'Swing Left District Finder-filtered.csv'

# Connect to the specific sheet
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(args.servicekey, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(spreadsheet_url).worksheet(sheet_name)

# Do stuff with the values in the sheet. WIP.
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)