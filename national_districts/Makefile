unused:
	@echo Please specify a Make target.

setup: national_districts.sql
	pip3 install -r requirments.txt
	mysql -u $(MYSQLUSER) -p $(MYSQLDB) < national_districts.sql

national_districts.sql: legislators-current.yaml
	-rm -f $@
	python3 national_districts.py < $< > $@
