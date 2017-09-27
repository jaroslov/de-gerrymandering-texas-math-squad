#!/usr/bin/env python

import json
import os
import subprocess
import sys

einfo   = json.loads(open('election-info.json').read())

years   = einfo.keys()
years.sort()

BCOUNT          = 40

bucketsPre2004  = [0 for i in xrange(BCOUNT)]
bucketsPost2004 = [0 for i in xrange(BCOUNT)]
bucketsPost2010 = [0 for i in xrange(BCOUNT)]
bucketsIs2016   = [0 for i in xrange(BCOUNT)]

for year in years:
    districts   = einfo[year]
    dnums       = districts.keys()
    dnums       = [int(d) for d in dnums]
    dnums.sort()
    for district in dnums:
        candidates  = districts[str(district)]
        REP     = 0
        DEM     = 0
        for candidate in candidates:
            if candidate['party'] == 'REP':
                REP = candidate['count']
            if candidate['party'] == 'DEM':
                DEM = candidate['count']
        if 0 in [REP, DEM]:
            continue
        diff    = float(DEM - REP) / float(REP + DEM)
        if int(year) < 2004:
            bucketsPre2004[int(round(BCOUNT * ((diff + 1) / 2)))] += 1
        if int(year) >= 2004:
            bucketsPost2004[int(round(BCOUNT * ((diff + 1) / 2)))] += 1
        if int(year) > 2010:
            bucketsPost2010[int(round(BCOUNT * ((diff + 1) / 2)))] += 1
        if int(year) == 2016:
            bucketsIs2016[int(round(BCOUNT * ((diff + 1) / 2)))] += 1

print '<2004'
print '\n'.join([str(x) for x in bucketsPre2004])
print '>=2004'
print '\n'.join([str(x) for x in bucketsPost2004])
print '>2010'
print '\n'.join([str(x) for x in bucketsPost2010])
print '=2016'
print '\n'.join([str(x) for x in bucketsIs2016])
