#!/usr/bin/env python

from bs4 import BeautifulSoup
import json
import os
import re
import subprocess
import sys

import xml.etree.ElementTree as ET

GE      = re.compile('(\d\d\d\d) General Election')
SRD     = re.compile('State Representative District (\d+)')
PARTY   = re.compile('(\w+)')

RACES   = {}

for i in xrange(400):
    print i
    cmdline     = ['curl', '--fail', 'http://elections.sos.state.tx.us/elchist%d_state.htm'%i]
    p           = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    o,e         = p.communicate()
    if p.returncode == 0:
        soup = BeautifulSoup(o.strip(), 'html.parser')
        for h2 in soup.find_all('h2'):
            m   = GE.match(h2.text)
            if m is None:
                continue
            year = int(m.group(1))
            RACES[year] = {}
            allTrs  = soup.find_all('tr')
            for idx in xrange(len(allTrs)):
                theTr   = allTrs[idx]
                allTds  = theTr.find_all('td')
                if len(allTds) == 0:
                    continue
                m       = SRD.match(allTds[0].text)
                if m is None:
                    continue
                district    = int(m.group(1))
                if district not in RACES[year].keys():
                    RACES[year][district]   = []
                for candidate in xrange(12):
                    candTds     = allTrs[idx+1+candidate].find_all('td')
                    m           = PARTY.match(candTds[2].text)
                    if m is None:
                        break
                    count   = int(re.sub(',', '', candTds[3].text))
                    RACES[year][district].append({'candidate':candTds[1].text, 'party':m.group(1), 'count':count})

with open("election-info.json", "w") as ei:
    print >> ei, json.dumps(RACES, indent=2)
