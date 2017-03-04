unused:
	@echo Please specify a Make target.

setup: voting_rights.sql
	mysql -u $(MYSQLUSER) -p $(MYSQLDB) < $<

voting_rights.sql: voting_rights_2016.csv
	-rm -f $@
	python3 voting_rights.py < $< > $@
