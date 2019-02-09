#!/usr/bin/env python

import json
import re
import sys
import xml.etree.ElementTree as ET

if __name__=="__main__":
    TXML    = ET.parse("Texas-Counties.svg")
    SVG     = TXML.getroot()
    JSON    = json.loads(open("Texas-Counties.json").read())
    Style   = SVG.findall('.//{http://www.w3.org/2000/svg}style')[0]
    years   = [info['county-wide-polling'] for key,info in JSON.items() if 'county-wide-polling' in info.keys()]
    minY    = min(years)
    maxY    = max(years)
    for key,info in JSON.items():
        if 'county-wide-polling' in info.keys():
            baseColor   = (0x20, 0x63, 0x9C)
            nextColor   = (0x80, 0xC3, 0xFC)
            yearInter   = (info['county-wide-polling'] - minY) / float(maxY - minY) # derp if maxY == minY
            colrInter   = tuple([int((nextC - baseC) * yearInter + baseC) for baseC,nextC in zip(baseColor, nextColor)])
            colrInter   = nextColor
            path_id     = 'TX_%s'%(key.replace(' ', '_'))
            Style.text  += '\n'
            Style.text  += '        #'+path_id+'{ fill:#%02X%02X%02X;fill-opacity:1;stroke:#000000;stroke-width:0.3; }\n'%colrInter
            Style.text  += '        #'+path_id+':hover { fill:#0061B6;fill-opacity:1;stroke:#000000;stroke-width:0.3; }\n'
    TXML.write('Texas-Counties-Mod.svg')
