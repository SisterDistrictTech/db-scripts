# Environment setup

You’ll need a Linux or Linux-like system with Python3 and the MySQL
server installed. To ensure you have the necessary Python modules for
the following steps, run this command:

```
pip3 install -r requirements.txt
```

# DB setup

To set up the Sister District database, run the following command:

```
python3 setupdb.py --dbname DBNAME --dbuser USER --dbpasswd PASSWD --googcreds CREDS
```

where DBNAME is the MySQL database name (default `SisterDistrict_dev`), USER is the MySQL user (default `root`), PASSWD is the user’s MySQL password, and CREDS is the path to a JSON file containing the Google service-account credentials (for accessing spreadsheets in the cloud). This JSON file can be downloaded from [the SisterDistrict Data and Research folder](https://drive.google.com/open?id=0B4PfgEkSv47QSy1qLUdIdEF0VTQ) in Google Drive. *Once downloaded please keep it secure.*

For the production database, use dbname `SisterDistrict`.
