# Logic relating to the national_districts db table.

import urllib.request
import yaml

from collections import defaultdict

LEGISLATORS_URL = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml'

class NationalDistricts:
    @staticmethod
    def setup(cur):
        """
        Initial setup of the national_districts table.
        WARNING: destroys any data present in national_districts.

        Args:
          cur - a database cursor
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
                ndtuples.append((1 + len(ndtuples), state, district, '%s-%s' % (state, district)))

        cur.execute('DELETE FROM national_districts')
        sql = ('INSERT INTO national_districts ' +
           ' (id, state, district, district_abbr) ' +
           ' VALUES (%s, %s, %s, %s)')
        cur.executemany(sql, ndtuples)
