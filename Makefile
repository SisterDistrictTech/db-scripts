export MYSQLUSER = root
export MYSQLDB = SisterDistrict_dev

unused:
	@echo Please specify a Make target.

setup:
	-mysqladmin -u $(MYSQLUSER) -p drop $(MYSQLDB)
	mysqladmin -u $(MYSQLUSER) -p create $(MYSQLDB)
	mysql -u $(MYSQLUSER) -p $(MYSQLDB) < SD_DB_Setup.sql
	cd national_districts; $(MAKE) setup
	cd voting_rights; $(MAKE) setup
	cd pres_races; $(MAKE) setup
