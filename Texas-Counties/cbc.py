#!/usr/bin/env python

import csv
import json

oldTCJ  = json.loads(open('Texas-Counties.json').read())

with open('cbc2.csv', 'rb') as csvfile:
    rd = csv.reader(csvfile)
    for row in rd:
        theCounty   = ' '.join(row[0].split(' ')[:-1])
        print theCounty
        newData = '%(link)s"'%{
                            'link'      : row[1],
                        }
        oldTCJ[theCounty]['url']            = newData
        oldTCJ[theCounty]['contact']        = row[2]
        oldTCJ[theCounty]['instructions']   = row[3]

with open('Texas-Counties2.json', 'w') as tcj:
    print >> tcj, json.dumps(oldTCJ, indent=4, sort_keys=True)