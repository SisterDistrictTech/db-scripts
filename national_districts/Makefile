LEGISLATORS_URL = https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml
LEGISLATORS_FILE = legislators-current.yaml

unused:
	@echo Please specify a Make target.

setup: national_districts.sql
	pip3 install -r requirements.txt
	mysql -u $(MYSQLUSER) -p $(MYSQLDB) < national_districts.sql

national_districts.sql: $(LEGISLATORS_FILE)
	-rm -f $@
	python3 national_districts.py < $< > $@

$(LEGISLATORS_FILE): fetch_legislators

fetch_legislators:
	if test -f $(LEGISLATORS_FILE); \
		then curl -z $(LEGISLATORS_FILE) -s -o $(LEGISLATORS_FILE) $(LEGISLATORS_URL); \
		else curl -s -o $(LEGISLATORS_FILE) $(LEGISLATORS_URL); \
	fi
