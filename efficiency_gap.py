#!/usr/bin/env python

#
# Created by Jacob N. Smith on 21 March 2017.
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import argparse
import json
import math
import sys
try:
    import scipy
    import scipy.stats
except:
    print "Install homebrew:"
    print "    https://brew.sh"
    print "Then, install scipy:"
    print "    brew install scipy"
    sys.exit(1)
hasPyLab        = False
try:
    import pylab
    hasPyLab    = True
except:
    print "Install homebrew:"
    print "    https://brew.sh"
    print "Then, install pylab:"
    print "    brew install pylab"

DATA = {
    2012            : {
    },
    2014            : {
    },
    2016            : {
        'CD'        : [
            #   DEM         REP             IND
            [   62847,      192434,         5128    ],
            [   100231,     168692,         9313    ],
            [   109420,     193684,         13363   ],
            [   None,       216643,         29577   ],
            [   None,       155469,         37406   ],
            [   106667,     159444,         7185    ],
            [   111991,     143542,         None    ],
            [   None,       236379,         None    ],
            [   152032,     36491,          None    ],
            [   120170,     179221,         13209   ],
            [   None,       201871,         23677   ],
            [   76029,      196482,         10604   ],
            [   None,       199050,         22192   ],
            [   99054,      160631,         None    ],
            [   101712,     66877,          8890    ],
            [   150228,     None,           25001   ],
            [   86603,      149417,         9708    ],
            [   150157,     48306,          5845    ],
            [   None,       176314,         27161   ],
            [   149640,     None,           38029   ],
            [   129765,     202967,         23299   ],
            [   123679,     181864,         None    ],
            [   107526,     110577,         10862   ],
            [   108389,     154845,         12401   ],
            [   117073,     180988,         12135   ],
            [   94507,      211730,         12843   ],
            [   88329,      142251,         None    ],
            [   122086,     57740,          4616    ],
            [   95649,      31646,          4687    ],
            [   170502,     41518,          6806    ],
            [   103852,     166060,         14676   ],
            [   None,       162868,         66303   ],
            [   93147,      33222,          None    ],
            [   104638,     62323,          None    ],
            [   124612,     62384,          10580   ],
            [   None,       193675,         24890   ],
        ],
        'house'     : [
        ],
        'senate'    : [
        ]
    }
}

JHOUSE_DATA         = json.loads(open("state-rep-analysis/election-info.json").read())
JHD_2016            = JHOUSE_DATA["2016"]
JHD_2016_ARR        = [[None,None,None] for _ in xrange(150)]
for district,values in JHD_2016.items():
    for value in values:
        if value['party'] == 'DEM':
            JHD_2016_ARR[int(district)-1][0] = value['count']
        elif value['party'] == 'REP':
            JHD_2016_ARR[int(district)-1][1] = value['count']
        elif value['party'] in ['IND', 'LIB', 'GRN', 'W']:
            JHD_2016_ARR[int(district)-1][2] = value['count']
        else:
            print value
            assert False
DATA[2016]['house'] = JHD_2016_ARR

def LikeMcGhee(D, R, I):
    '''
    XXX: Ignore independents, entirely.
    '''
    return math.floor(float(D + R) / 2)

def PluralityDiff(D, R, I):
    '''
    XXX: In Texas, the candidate with the *most* votes, wins. This means
    it's possible for (very close) races to have a candidate that doesn't
    get a clear majority. We have to look for those cases and make sure
    we don't assign 'negative' wasted votes to that winning candidate.

    District 23: I'm lookin' at you, bro.
    '''
    allVotes    = [D, R, I, 0]
    allVotes.sort()
    allVotes.reverse()
    minToWin    = allVotes[1]+1
    return minToWin

def EfficiencyGap(data, year, kind, ComputeType=None, Regress=None):
    '''
        Compute the efficiency gap. Arguments are:

            data        -- the raw data to use
            year        -- which year to compute the gap for
            kind        -- which legislative branch to compute the gap for
            Regress     -- method for computing the votes in uncontested races
    '''

    if Regress is None:
        return [None for x in len(data[year][kind])]

    newDistrictData = Regress(data, year, kind)

    perDistrictGap  = []

    for D,R,I in newDistrictData:
        minToWin    = ComputeType(D, R, I)
        Dwasted     = D if D < R else D - minToWin
        Rwasted     = R if R < D else R - minToWin
        perDistrictGap.append({'D':D, 'R':R, 'I':I, 'Dwasted':Dwasted, 'Rwasted':Rwasted})

    return  {
                'perDistrictGap'    : perDistrictGap,
                'totalVotes'        :   (
                                            sum([D for D,_,_ in newDistrictData])
                                        +   sum([R for _,R,_ in newDistrictData])
                                        +   sum([I for _,_,I in newDistrictData])
                                        ),
                'Dtotal'            : sum([D for D,_,_ in newDistrictData]),
                'Rtotal'            : sum([R for _,R,_ in newDistrictData]),
                'Itotal'            : sum([I for _,_,I in newDistrictData]),
            }


def Ignore(data, year, kind):
    '''
        Give the uncontested loser 0 votes.
    '''

    return [(D if D is not None else 0, R if R is not None else 0, I if I is not None else 0) for D,R,I in data[year][kind]]

def LinearRegressInverse(data, year, kind):
    '''
        Use the linear regression of the ratio of the winner's votes to the loser's votes.
    '''

    Dcontested      = []
    Rcontested      = []

    for D,R,I in data[year][kind]:
        if D is None or R is None:
            continue
        if D > R:
            Dcontested.append((D,R,I))
        else:
            Rcontested.append((D,R,I))

    Dinverse        = [(D,float(D)/R) for D,R,_ in Dcontested]
    Rinverse        = [(R,float(R)/D) for D,R,_ in Rcontested]

    Da_s,Db_s,Dr,Dtt,Derr   = scipy.stats.linregress([V for V,R in Dinverse], [R for V,R in Dinverse])
    Deval                   = scipy.polyval([Da_s, Db_s], [V for V,R in Dinverse])
    Ra_s,Rb_s,Rr,Rtt,Rerr   = scipy.stats.linregress([V for V,R in Rinverse], [R for V,R in Rinverse])
    Reval                   = scipy.polyval([Ra_s, Rb_s], [V for V,R in Rinverse])

    if hasPyLab:
        pylab.title('Inverse regression')
        pylab.plot([V for V,R in Dinverse], [R for V,R in Dinverse], 'b.')
        pylab.plot([V for V,R in Dinverse], Deval, 'b-')
        pylab.plot([V for V,R in Rinverse], [R for V,R in Rinverse], 'r.')
        pylab.plot([V for V,R in Rinverse], Reval, 'r-')
        pylab.legend(['D ratio', 'D l-r', 'R ratio', 'R l-r'])
        pylab.show()

    results     = []
    for D,R,I in data[year][kind]:
        Ik      = I if I is not None else 0
        if D is None:
            Dk  = .75 * R / scipy.polyval([Ra_s, Rb_s], R)
        else:
            Dk  = D
        if R is None:
            Rk  = .75 * D / scipy.polyval([Da_s, Db_s], D)
        else:
            Rk  = R
        results.append((Dk,Rk,Ik))

    return results


#
# XXX: The available methods for performing regression analysis of missing districts.
#
Methods     = {
    'ignore-uncontested'        : Ignore,
    'linear-regress-inverse'    : LinearRegressInverse,
}

GapType     = {
    'like-mcghee'               : LikeMcGhee,
    'plurality-diff'            : PluralityDiff,
}

################################################
def GenReport(results):
    '''
        Pretty print a table for the user.
    '''

    perDistrictGap  = results['perDistrictGap']
    totalVotes      = results['totalVotes']
    Dwasted,Rwasted = sum([P['Dwasted'] for P in perDistrictGap]), sum([P['Rwasted'] for P in perDistrictGap])
    totalWasted     = Dwasted + Rwasted
    Dtotal          = results['Dtotal']
    Rtotal          = results['Rtotal']
    Itotal          = results['Itotal']

    print '  #    %-10s  %-10s  %-10s | %-10s  %-10s'%('D', 'R', 'I', 'Dw', 'Rw')
    print '+-----'+'-'*(12 * 5)+'-+'
    for Npre,P in enumerate(perDistrictGap):
        N           = Npre + 1
        D,R,I,Dw,Rw = P['D'],P['R'],P['I'],P['Dwasted'],P['Rwasted']
        print '| %2d | %-10d  %-10d  %-10d | %-10d  %-10d |'%(N, D, R, I, Dw, Rw)

    print '+-----'+'-'*(12 * 5)+'-+'
    print '       %-10d  %-10d  %-10d  %-10d  %-10d'%(Dtotal, Rtotal, Itotal, Dwasted, Rwasted)

    Wasted          = None
    Loser           = None
    if Dwasted > Rwasted:
        Loser       = "D"
        Wasted      = Dwasted - Rwasted
    else:
        Loser       = "R"
        Wasted      = Rwasted - Dwasted
    print
    print "Wasted %d of %d (%s) : %4.2f%%"%(Wasted, totalVotes, Loser, float(Wasted) / totalVotes * 100)





if __name__=='__main__':
    parser  = argparse.ArgumentParser()
    parser.add_argument('-y', '--year', default=2016, help="Which year to analyze.")
    parser.add_argument('-k', '--kind', default='CD', help="Which legislative branch to analyze: US congressional = 'CD'; TX House = 'house'; TX Senate = 'senate'.")
    parser.add_argument('-m', '--method', default='ignore-uncontested', help="Which method to use to analyze uncontested races: "+', '.join(Methods.keys()))
    parser.add_argument('-c', '--gap-type', default='like-mcghee', help="Which method to use to compute the wasted votes: "+', '.join(GapType.keys()))

    args    = parser.parse_args()

    assert int(args.year) in DATA.keys(), "I'm sorry, I don't have data for the year " + str(args.year)
    assert args.kind in DATA[int(args.year)].keys(), "I'm sorry, I don't know the legislative branch " + args.kind
    assert args.method in Methods.keys(), "I'm sorry, I don't know the method " + args.method

    print "   Year :", args.year
    print "   Kind :", args.kind
    print " Method :", args.method
    print

    results = EfficiencyGap(DATA, int(args.year), args.kind, GapType[args.gap_type], Methods[args.method])

    GenReport(results)


