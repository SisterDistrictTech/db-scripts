# db-scripts
These are the setup scripts required to fill data into the internal database.

## Main scripts
### voting_rights/voting_rights.py
Parses our compilation of voting laws from voting_rights/voting_rights_2016.csv and outputs SQL file voting_rights/voting_rights.sql which can be executed to truncate and repopulate the voting_rights MySQL table.

**Usage (from db-scripts directory):**
* python3 voting_rights/voting_rights.py
