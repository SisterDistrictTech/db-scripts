# db-scripts
These are the setup scripts required to fill data into the internal database.

## Main scripts
### national_districts.py
Parses our compilation of voting laws from voting_rights/voting_rights_2017.csv and outputs SQL file voting_rights/voting_rights.sql which can be executed to truncate and repopulate the voting_rights MySQL table.
**Usage:**
(From db-scripts directory.)
pip3 install -r voting_rights/requirements.txt
python3 voting_rights/voting_rights.py