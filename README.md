# db-scripts
These are the setup scripts required to fill data into the internal database.

## Dev Setup
To create a dev copy of the database SisterDistrict_dev run the following command in your local environment.

```
mysqladmin -u root -p drop SisterDistrict_dev
mysqladmin -u root -p create SisterDistrict_dev
mysql -u root -p SisterDistrict_dev < SD_DB_Setup.sql
```

Swapping out the root use if you have a different super user.

## Main scripts

### Main database setup

```
mysqladmin -u root -p drop SisterDistrict
mysqladmin -u root -p create SisterDistrict
mysql -u root -p SisterDistrict < SD_DB_Setup.sql
```

* Troubleshooting tips
=======
### national_districts/national_districts.py
Parses current legislator data from https://github.com/unitedstates/congress-legislators/blob/master/legislators-current.yaml into federal districts and outputs them as MySQL inserts for the national_districts table with deterministic ids.

**Usage:**

```
cd national_districts
pip3 install -r requirments.txt
python3 national_districts.py > national_districts.sql
mysql -u root -p SisterDistrict_dev < national_districts.sql
```

### voting_rights/voting_rights.py
Parses our compilation of voting laws from voting_rights/voting_rights_2016.csv and outputs SQL file voting_rights/voting_rights.sql which can be executed to truncate and repopulate the voting_rights MySQL table.

**Usage (from db-scripts directory):**

```
cd voting_rights
python3 voting_rights.py
mysql -u root -p SisterDistrict_dev < voting_rights.sql
```

### pres_races/pres_races.py

Inserts the results of the last 10 presidential elections.

**Usage:**

```
cd pres_races
mysql -u root -p SisterDistrict_dev < pres_races.sql
```

