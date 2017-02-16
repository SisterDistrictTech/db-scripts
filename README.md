# db-scripts
These are the setup scripts required to fill data into the internal database.

## Main scripts
### national_districts.py
Parses current legislator data from https://github.com/unitedstates/congress-legislators/blob/master/legislators-current.yaml into federal districts and outputs them as MySQL inserts for the national_districts table with deterministic ids.

**Usage:**

pip3 install -r requirments.txt

python3 national_districts.py > national_districts.sql

### voting_rights/voting_rights.py
Parses our compilation of voting laws from voting_rights/voting_rights_2016.csv and outputs SQL file voting_rights/voting_rights.sql which can be executed to truncate and repopulate the voting_rights MySQL table.

**Usage (from db-scripts directory):**

python3 voting_rights/voting_rights.py