#!/usr/bin/python3

import sys
import requests

LIST_REPOS = 'https://hub.docker.com/v2/repositories/%(org)s/'
GET_STATS = 'https://hub.docker.com/v2/repositories/%(namespace)s/%(name)s/'

counts = dict()
col_width = 0;

org = "edgexfoundry"
if len(sys.argv) > 1:
    org = sys.argv[1]

next_page = LIST_REPOS % {"org": org}

count = 0
while next_page is not None:
    resp = requests.get(next_page)
    count += 1
    next_page = None
    if resp.status_code == 200:
        data = resp.json()
        # Read project data
        for repo in data['results']:
            counts[repo['name']] = repo['pull_count']
            if len(repo['name']) > col_width:
                col_width = len(repo['name'])

        if data['next'] is not None:
            next_page = data['next']

total = 0
#header = "{0:<%d} : {1}" % col_width
#row = "{0:<%d} : {1:>9,}" % col_width
#print()
#print(header.format('Image', 'Downloads'))
#print('-'*(col_width+1) + ':' + '-'*10)
#for name, count in counts.items():
#    print(row.format(name, count))
#    total += count
#print('-'*(col_width+1) + ':' + '-'*10)
#print(row.format('Total', total))

print('Image\tDownloads')
for name, count in counts.items():
    print("%s\t%s" % (name, count))
    total += count

