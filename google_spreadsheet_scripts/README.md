
# Google Spreadsheet Scripts

A set of scripts used to fetch data from Google Spreadsheets and insert it into our mysql database. 

# Auth

To connect to Google Spreadsheets, you will need access to our shared service key. This is located in the main Data and Research Google Drive folder.

An easy way to get this key locally (and automatically keep it up to date) is to install the Google Drive application which synchronizes your data locally - https://tools.google.com/dlpage/drive. 

Add the "Research and Data" folder to your drive and all these files will be available locally. 

# Installation

```
pip3 install -r requirements.txt
```

# swing_left_district_finder

```
SDSERVICEKEY="/Users/yourusername/Google Drive/Data and Research/read-only-google-account.json"
python3 swing_left_district_finder.py "${SDSERVICEKEY}"
```

## Notes

We use http://gspread.readthedocs.io/en/latest/ to connect to Google Spreadsheets.