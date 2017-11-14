#!/usr/bin/env python

HELP    = """
    help        -- print this help message
    exit        -- exit the game (also: quit)

    The following games (from easiest to hardest) are available:

    unfair      -- try to build unfair districts
"""

PURPLE  = '\033[95m'
BLUE    = '\033[94m'
GREEN   = '\033[92m'
YELLOW  = '\033[93m'
RED     = '\033[91m'
ENDC    = '\033[0m'

def ShowUnfairMap(districtCount=None):
    AFval       = (PURPLE+'Fed:'+ENDC+' %2s')%str(districtCount['A']['Federalist'] )if districtCount is not None else '       '
    CFval       = (PURPLE+'Fed:'+ENDC+' %2s')%str(districtCount['C']['Federalist'] )if districtCount is not None else '       '
    ADval       = (GREEN +'D-R:'+ENDC+' %2s')%str(districtCount['A']['Democratic-Republican']) if districtCount is not None else '       '
    CDval       = (GREEN +'D-R:'+ENDC+' %2s')%str(districtCount['C']['Democratic-Republican']) if districtCount is not None else '       '
    BFval       = (PURPLE+'Fed:'+ENDC+' %2s')%str(districtCount['B']['Federalist'] )if districtCount is not None else '       '
    DFval       = (PURPLE+'Fed:'+ENDC+' %2s')%str(districtCount['D']['Federalist'] )if districtCount is not None else '       '
    BDval       = (GREEN +'D-R:'+ENDC+' %2s')%str(districtCount['B']['Democratic-Republican']) if districtCount is not None else '       '
    DDval       = (GREEN +'D-R:'+ENDC+' %2s')%str(districtCount['D']['Democratic-Republican']) if districtCount is not None else '       '
    print "                 +---------+---------+"
    print "                 |    A    |    B    |"
    print "                 | %s | %s |"%(AFval, BFval)
    print "                 | %s | %s |"%(ADval, BDval)
    print "                 |         |         |"
    print "                 +---------+---------+"
    print "                 |    C    |    D    |"
    print "                 | %s | %s |"%(CFval, DFval)
    print "                 | %s | %s |"%(CDval, DDval)
    print "                 |         |         |"
    print "                 +---------+---------+"

def UnfairGame():
    print "(*) The state Squarahoma has four districts A, B, C, and D:"
    ShowUnfairMap()
    print ""
    print "    There are 40 people who live in Squrahoma:"
    print "         20 of them are Federalists, and"
    print "         20 of them are Democratic-Republicans."
    findSide            = True
    while findSide:
        side            = raw_input(("    Do you want to play as a "+PURPLE+"Federalist"+ENDC+", or a "+GREEN+"Democratic-Republic?"+ENDC+" "))
        if side.upper() in ['F', 'FED', 'FEDERALIST']:
            side        = 'Federalist'
            findSide    = False
        elif side.upper() in ['D', 'R', 'DR', 'D-R', 'DEMOCRATIC-REPUBLICAN']:
            side        = 'Democratic-Republican'
            findSide    = False
        elif side in ['quit', 'exit']:
            findSide    = False
            return
        else:
            print (RED+"(!)"+ENDC+" I'm sorry, I don't know the political party '%s'.")%side
    print "(~) Now, we need to put about 10 people in each district..."
    districtCount       = {
        'A' : { 'Federalist' : '?', 'Democratic-Republican' : '?' },
        'B' : { 'Federalist' : '?', 'Democratic-Republican' : '?' },
        'C' : { 'Federalist' : '?', 'Democratic-Republican' : '?' },
        'D' : { 'Federalist' : '?', 'Democratic-Republican' : '?' },
    }
    parties         = ['Federalist', 'Democratic-Republican']
    partyCount      = [ 20, 20 ]
    partyColors     = [ PURPLE, GREEN ]
    for district in ['A', 'B', 'C', 'D']:
        districtTotal   = 0
        for pdx in xrange(len(parties)):
            partyColor          = partyColors[pdx]
            party               = parties[pdx]
            while True:
                numSideS        = raw_input(("    How many "+partyColor+"%ss"+ENDC+" do you want to put into district %s? ")%(party, district))
                if numSideS in ['exit', 'quit']:
                    return
                try:
                    numSide     = int(numSideS)
                except:
                    print (RED+"(!)"+ENDC+" I'm sorry, '%s' doesn't look like a number to me.")%numSideS
                    continue
                if numSide < 0 or numSide > 11:
                    print (RED+"(!)"+ENDC+" I'm sorry, I can't put that many %ss into district %s")%(party, district)
                    continue
                if numSide > partyCount[pdx]:
                    print (RED+"(!)"+ENDC+" I'm sorry, there aren't enough %ss; there's only %d left!")%(party, partyCount[pdx])
                    continue
                if districtTotal + numSide > 11:
                    print (RED+"(!)"+ENDC+" I'm sorry, there's now too many people in district %s: %d")%(district, districtTotal+numSide)
                    continue
                break
            districtTotal += numSide
            districtCount[district][parties[pdx]] = numSide
            ShowUnfairMap(districtCount)
            partyCount[pdx] -= numSide
    numFed  = sum([1 if districtCount[D]['Federalist'] > districtCount[D]['Democratic-Republican'] else 0 for D in ['A', 'B', 'C', 'D']])
    numDR   = sum([1 if districtCount[D]['Federalist'] < districtCount[D]['Democratic-Republican'] else 0 for D in ['A', 'B', 'C', 'D']])
    numTie  = 4 - (numFed + numDR)
    if (numFed > numDR and side == 'Federalist') or (numFed < numDR and side == 'Democratic-Republican'):
        print (GREEN+"(*)"+ENDC+" Great! Your side won, even though there should've been a tie!")
    elif numFed == numDR:
        print (YELLOW+"(~)"+ENDC+" It's ok; neither party has a majority in an even state...")
    else:
        print (RED+"(!)"+ENDC+" Uh oh! Looks like your party lost!")

def PlayGames():
    keepPlaying     = True
    while keepPlaying:
        user_input          = raw_input(">>> ")
        if user_input == 'help':
            print HELP
        elif user_input in ['quit', 'exit']:
            keepPlaying     = False
        elif user_input == 'unfair':
            UnfairGame()
        else:
            print "Type 'help' for help."

PlayGames()
