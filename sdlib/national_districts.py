# Logic relating to the national_districts db table.

import urllib.request
import yaml

from collections import defaultdict

LEGISLATORS_URL = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml'

class NationalDistricts:
    @staticmethod
    def populate(cur, reset=False):
        """
        Load data into the national_districts table.

        Args:
          cur: a database cursor
          reset: whether to empty the table before populating it (warning!)
        """
        with urllib.request.urlopen(LEGISLATORS_URL) as l:
            legislators = yaml.load(l)

        state_districts = defaultdict(list)
        for rep in legislators:
            term = rep['terms'][-1]
            if term['type'] == 'rep':
                state_districts[term['state']].append(term['district'])

        states = list(state_districts.keys())
        states.sort()
        ndtuples = []
        for state in states:
            districts = state_districts[state]
            districts.sort()
            for district in districts:
                # Don't let MySQL assign AUTO_INCREMENT ids to the
                # rows, because we want them to start at 1
                id = 1 + len(ndtuples)
                district_abbr = '%s-%s' % (state, district)
                ndtuples.append((id, state, district, district_abbr))

        if reset:
            cur.execute('DELETE FROM national_districts')

        sql = ('INSERT INTO national_districts ' +
           ' (id, state, district, district_abbr) ' +
           ' VALUES (%s, %s, %s, %s)')
        cur.executemany(sql, ndtuples)
