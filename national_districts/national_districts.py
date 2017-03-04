import sys
import yaml

# TODO: read the latest legislators-current.yaml from
# https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml

data = yaml.load(sys.stdin)

state_districts = {}

for rep in data:
    term = rep['terms'][-1]
    if term['type'] == 'rep':
        if term['state'] in state_districts:
          state_districts[term['state']].append(term['district'])
        else:
          state_districts[term['state']] = [term['district']]

id = 1
states = list(state_districts.keys())
states.sort()
for state in states:
    districts = list(state_districts[state])
    districts.sort()
    for district in districts:
        print('INSERT INTO national_districts (id, state, district, district_abbr) VALUES ({0}, \'{1}\', {2}, \'{1}-{2}\');'.format(id, state, district))
        id += 1
