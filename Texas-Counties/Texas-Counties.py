#!/usr/bin/env python

import argparse
import json
import re
import sys
import textwrap
import xml.etree.ElementTree as ET

if __name__=="__main__":
    parser  = argparse.ArgumentParser(description='Build maps of Texas with facts')
    parser.add_argument('-o', '--output', help="The name of the output file", required=True)
    parser.add_argument('-i', '--info', help="Which set of facts to export", required=True)
    parser.add_argument('-t', '--title', help="Optional title")
    parser.add_argument('-a', '--auto-format-contact', action='store_true', help="Whether or not to automatically format the contact info")

    args        = parser.parse_args()

    ET.register_namespace('svg', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
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
            #Style.text      += '        #'+path_id+'{ fill:#%02X%02X%02X;fill-opacity:1;stroke:#000000;stroke-width:0.3; }\n'%(0x60, 0xB3, 0xDC)
            #Style.text      += '        #'+path_id+':hover { fill:#0061B6;fill-opacity:1;stroke:#000000;stroke-width:0.3; }\n'
            itsText         = SVG.findall('.//{http://www.w3.org/2000/svg}g[@id="fact_%s"]'%path_id)[0]
            theText         = ET.Element("{http://www.w3.org/2000/svg}text")
            xlink           = ET.Element("{http://www.w3.org/2000/svg}a")
            theText.set('x', '600')
            theText.set('y', '384')
            xlink.set('xlink:href', info['url'])
            xlink.text      = county
            xlink.set('text-decoration', 'underline')
            theText.append(xlink)
            itsText.append(theText)

            if args.auto_format_contact:
                paragraph   = [ ]
                opara       = info['contact'].split('\n')
                for para in opara:
                    para    = textwrap.wrap(para, width=36)
                    paragraph.extend(para)
            else:
                paragraph   = info['contact'].split('\n')
            instrs          = info['instructions'].replace('\n', ' ')
            instrs          = textwrap.wrap(instrs, width=36)
            paragraph       += ['']
            paragraph       += instrs

            for II,subcontact in enumerate(paragraph):
                theContact      = ET.Element("{http://www.w3.org/2000/svg}text")
                theContact.text = subcontact
                theContact.set('x', '600')
                theContact.set('y', '%s'%(400+10*II))
                itsText.append(theContact)
            #itsText.text    = county + ' ' + str(info[args.info])
    TXML.write(args.output)

    FEH     = open(args.output).read()
    with open(args.output, 'w') as feh:
        FEH = FEH.replace('xmlns:svg="http://www.w3.org/2000/svg"', 'xmlns:svg="http://www.w3.org/2000/svg"  xmlns:xlink="http://www.w3.org/1999/xlink"')
        print >> feh, FEH

