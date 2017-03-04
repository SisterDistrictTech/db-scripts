# Setup

To create a dev copy of the database SisterDistrict_dev run the following command in your local environment.

```
make setup
```

This assumes you want to use the database name `SisterDistrict_dev` and the MySQL user `root`. One or both can be overridden as follows:

```
make setup MYSQLDB=dbname MYSQLUSER=username
```

As this runs, you will be prompted multiple times to enter the database password.

To set up the production copy of the database, use:

```
make setup MYSQLDB=SisterDistrict
```
