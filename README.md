# db-scripts
These are the setup scripts required to fill data into the internal database.

## Main scripts
### national_districts.py
Parses current legislator data from https://github.com/unitedstates/congress-legislators/blob/master/legislators-current.yaml into federal districts and outputs them as MySQL inserts for the national_districts table with deterministic ids.
**Usage:**
pip3 install -r requirments.txt
python3 national_districts.py > national_districts.sql
