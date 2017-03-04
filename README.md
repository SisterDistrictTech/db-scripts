# DB setup

To set up the Sister District database, run the following command:

```
python3 setupdb.py --dbname DBNAME --dbuser USER --dbpasswd PASSWD --googcreds CREDS
```

where DBNAME is the MySQL database name (default `SisterDistrict_dev`), USER is the MySQL user (default `root`), PASSWD is the user’s MySQL password, and CREDS is the path to a JSON file containing the Google service-account credentials (for accessing spreadsheets in the cloud).

For the production database, use dbname `SisterDistrict`.
