#!/usr/bin/env python

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET

if __name__=="__main__":
    parser  = argparse.ArgumentParser(description='Build maps of Texas with facts')
    parser.add_argument('-o', '--output', help="The name of the output file", required=True)
    parser.add_argument('-i', '--info', help="Which set of facts to export", required=True)
    parser.add_argument('-t', '--title', help="Optional title")

    args        = parser.parse_args()

    TXML        = ET.parse("Texas-Counties.svg")
    SVG         = TXML.getroot()
    JSON        = json.loads(open("Texas-Counties.json").read())
    Style       = SVG.findall('.//{http://www.w3.org/2000/svg}style')[0]
    years       = [info['county-wide-polling'] for key,info in JSON.items() if 'county-wide-polling' in info.keys()]
    minY        = min(years)
    maxY        = max(years)
    mapTitle    = args.title if args.title is not None else ' '.join([X.capitalize() for X in args.info.replace('-', ' ').replace('_', ' ').split(' ')])
    mTElt       = SVG.findall('.//{http://www.w3.org/2000/svg}text[@id="map_title"]')[0]
    mTElt.text  = mapTitle
    for county,info in JSON.items():
        if args.info in info.keys():
            path_id         = 'TX_%s'%(county.replace(' ', '_'))
            Style.text      += '        #'+path_id+'{ fill:#%02X%02X%02X;fill-opacity:1;stroke:#000000;stroke-width:0.3; }\n'%(0x60, 0xB3, 0xDC)
            Style.text      += '        #'+path_id+':hover { fill:#0061B6;fill-opacity:1;stroke:#000000;stroke-width:0.3; }\n'
            itsText         = SVG.findall('.//{http://www.w3.org/2000/svg}text[@id="text_%s"]'%path_id)[0]
            itsText.text    = county + ' ' + str(info[args.info])
    TXML.write(args.output)
