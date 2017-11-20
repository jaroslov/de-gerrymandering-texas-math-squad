var CWIDTH          = 512;
var CHEIGHT         = 512;
var CRADIUS         = 3;
var ERADIUS         = 15;
var DISTRICTCOLOR   = "#999999";
var FEDCOLOR        = "#555555";
var FEDBORDERCLR    = "#111111";
var D_RCOLOR        = "#00ACEE";
var D_RBORDERCLR    = "#00008F";
var FEDNAME         = 'Feds';
var D_RNAME         = 'D_Rs';
var Paths           = [];
var Painting        = false;
var TheContext;
var ThePopulation   = [];
var TheReflector    = [...Array(CHEIGHT)].map(i => Array(CWIDTH));
var FedRndRange     = 10;
var FedRndBase      = 10;
var D_RRndRange     = 10;
var D_RRndBase      = 10;
var DRAWCOLOR       = DISTRICTCOLOR;
var BKGDCOLOR       = "#FFFFFF";

function GenerateRandomPopulation()
{
    var NumFeds     = Math.floor(Math.random() * FedRndRange) + FedRndBase;
    var NumD_Rs     = Math.floor(Math.random() * D_RRndRange) + D_RRndBase;

    for (i = 0; i < NumFeds; ++i)
    {
        ThePopulation.push({
            'Party' : FEDNAME,
            'x'     : Math.floor(Math.random() * CWIDTH),
            'y'     : Math.floor(Math.random() * CHEIGHT),
        });
    }

    for (i = 0; i < NumD_Rs; ++i)
    {
        ThePopulation.push({
            'Party' : D_RNAME,
            'x'     : Math.floor(Math.random() * CWIDTH),
            'y'     : Math.floor(Math.random() * CHEIGHT),
        });
    }
}

function GenerateEasyPopulation()
{
    ThePopulation.push({'Party':FEDNAME, 'x':55, 'y':15});
    ThePopulation.push({'Party':FEDNAME, 'x':55, 'y':30});
    ThePopulation.push({'Party':FEDNAME, 'x':55, 'y':45});
    ThePopulation.push({'Party':FEDNAME, 'x':55, 'y':60});
    ThePopulation.push({'Party':FEDNAME, 'x':55, 'y':75});
    ThePopulation.push({'Party':FEDNAME, 'x':95, 'y':15});
    ThePopulation.push({'Party':FEDNAME, 'x':95, 'y':30});
    ThePopulation.push({'Party':FEDNAME, 'x':95, 'y':45});
    ThePopulation.push({'Party':FEDNAME, 'x':95, 'y':60});
    ThePopulation.push({'Party':FEDNAME, 'x':95, 'y':75});

    ThePopulation.push({'Party':FEDNAME, 'x':415, 'y':15});
    ThePopulation.push({'Party':FEDNAME, 'x':415, 'y':30});
    ThePopulation.push({'Party':FEDNAME, 'x':415, 'y':45});
    ThePopulation.push({'Party':D_RNAME, 'x':415, 'y':60});
    ThePopulation.push({'Party':D_RNAME, 'x':415, 'y':75});
    ThePopulation.push({'Party':D_RNAME, 'x':445, 'y':15});
    ThePopulation.push({'Party':D_RNAME, 'x':445, 'y':30});
    ThePopulation.push({'Party':D_RNAME, 'x':445, 'y':45});
    ThePopulation.push({'Party':D_RNAME, 'x':445, 'y':60});
    ThePopulation.push({'Party':D_RNAME, 'x':445, 'y':75});

    ThePopulation.push({'Party':FEDNAME, 'x':55, 'y':415});
    ThePopulation.push({'Party':FEDNAME, 'x':55, 'y':430});
    ThePopulation.push({'Party':FEDNAME, 'x':55, 'y':445});
    ThePopulation.push({'Party':FEDNAME, 'x':55, 'y':460});
    ThePopulation.push({'Party':D_RNAME, 'x':55, 'y':475});
    ThePopulation.push({'Party':D_RNAME, 'x':95, 'y':415});
    ThePopulation.push({'Party':D_RNAME, 'x':95, 'y':430});
    ThePopulation.push({'Party':D_RNAME, 'x':95, 'y':445});
    ThePopulation.push({'Party':D_RNAME, 'x':95, 'y':460});
    ThePopulation.push({'Party':D_RNAME, 'x':95, 'y':475});

    ThePopulation.push({'Party':FEDNAME, 'x':415, 'y':415});
    ThePopulation.push({'Party':FEDNAME, 'x':415, 'y':430});
    ThePopulation.push({'Party':FEDNAME, 'x':415, 'y':445});
    ThePopulation.push({'Party':D_RNAME, 'x':415, 'y':460});
    ThePopulation.push({'Party':D_RNAME, 'x':415, 'y':475});
    ThePopulation.push({'Party':D_RNAME, 'x':445, 'y':415});
    ThePopulation.push({'Party':D_RNAME, 'x':445, 'y':430});
    ThePopulation.push({'Party':D_RNAME, 'x':445, 'y':445});
    ThePopulation.push({'Party':D_RNAME, 'x':445, 'y':460});
    ThePopulation.push({'Party':D_RNAME, 'x':445, 'y':475});
}

function loader(setup)
{
    if (setup['width'])
    {
        CWIDTH      = setup['width'];
    }
    if (setup['height'])
    {
        CHEIGHT     = setup['height'];
    }
    if (setup['radius'])
    {
        CRADIUS     = setup['radius'];
    }
    if (setup['FedRndRange'])
    {
        FedRndRange = setup['FedRndRange'];
    }
    if (setup['FedRndBase'])
    {
        FedRndBase  = setup['FedRndBase'];
    }
    if (setup['D_RRndRange'])
    {
        D_RRndRange = setup['D_RRndRange'];
    }
    if (setup['D_RRndBase'])
    {
        D_RRndBase  = setup['D_RRndBase'];
    }
    if (setup['population'])
    {
        switch (setup['population'])
        {
        case 'random'   :
            GenerateRandomPopulation();
            break;
        case 'easy'     :
        default         :
            GenerateEasyPopulation();
            break;
        }
    }

    var gcvs        = document.getElementById('gerrycanvas');
    gcvs.setAttribute('style', 'border: 1px solid black');
    gcvs.setAttribute('width',  CWIDTH);
    gcvs.setAttribute('height', CHEIGHT);

    TheContext      = gcvs.getContext("2d");

    gcvs.addEventListener('mousedown',  Press,      false);
    gcvs.addEventListener('mousemove',  Drag,       false);
    gcvs.addEventListener('mouseup',    Release);
    gcvs.addEventListener('mouseout',   Cancel,     false);

    var legfed      = document.getElementById('legend-feds');
    legfed.setAttribute('style', 'background-color:' + FEDCOLOR + '; border: 1px solid ' + FEDBORDERCLR + ';');
    var legd_r      = document.getElementById('legend-d_rs');
    legd_r.setAttribute('style', 'background-color:' + D_RCOLOR + '; border: 1px solid ' + D_RBORDERCLR + ';');

    Redraw();
}

function AddLocation(mX, mY, dragging)
{
    var drawTool    = document.getElementById("boundary").checked;
    Paths.push({'x':mX, 'y':mY, 'drag':dragging, 'color': drawTool});
}

function Press(e)
{
    var mouseX      = e.changedTouches
                    ? e.changedTouches[0].pageX
                    : e.pageX
                    ;
    mouseX          -= this.offsetLeft;
    var mouseY      = e.changedTouches
                    ? e.changedTouches[0].pageY
                    : e.pageY
                    ;
    mouseY          -= this.offsetTop;
    Painting        = true;
    AddLocation(mouseX, mouseY, false);
    Redraw();
}

function Drag(e)
{
    var mouseX      = e.changedTouches
                    ? e.changedTouches[0].pageX
                    : e.pageX
                    ;
    mouseX          -= this.offsetLeft;
    var mouseY      = e.changedTouches
                    ? e.changedTouches[0].pageY
                    : e.pageY
                    ;
    mouseY          -= this.offsetTop;
    if (Painting)
    {
        AddLocation(mouseX, mouseY, true);
        Redraw();
    }

    e.preventDefault();
}

function Release()
{
    Painting    = false;
    Redraw();
}

function Cancel()
{
    Painting    = false;
}

function Clear()
{
    TheContext.clearRect(0, 0, CWIDTH, CHEIGHT);
}

function Population()
{
    for (i = 0; i < ThePopulation.length; i++)
    {
        TheContext.beginPath();
        TheContext.arc(ThePopulation[i]['x'], ThePopulation[i]['y'],5,0,6.2830);
        if (ThePopulation[i]['Party'] == FEDNAME)
        {
            TheContext.strokeStyle  = FEDBORDERCLR;
            TheContext.fillStyle    = FEDCOLOR;
        }
        else
        {
            TheContext.strokeStyle  = D_RBORDERCLR;
            TheContext.fillStyle    = D_RCOLOR;
        }
        TheContext.lineWidth    = 1;
        TheContext.fill();
        TheContext.stroke();
    }
}

function Redraw()
{
    for (i = 0; i < Paths.length; i++)
    {
        TheContext.beginPath();
        if (Paths[i]['drag'] && i)
        {
            TheContext.moveTo(Paths[i-1]['x'], Paths[i-1]['y']);
        }
        else
        {
            TheContext.moveTo(Paths[i]['x'], Paths[i]['y']);
        }
        TheContext.lineTo(Paths[i]['x'], Paths[i]['y']);
        TheContext.lineCap      = 'round';
        TheContext.lineJoin     = 'round';
        TheContext.lineWidth    = Paths[i]['color'] ? CRADIUS : ERADIUS;
        TheContext.strokeStyle  = Paths[i]['color'] ? DISTRICTCOLOR : BKGDCOLOR;
        TheContext.stroke();
    }

    TheContext.closePath();

    Population();
}

function SimulateElection()
{
    var TheRawData              = TheContext.getImageData(0, 0, CWIDTH, CHEIGHT);

    var BORDER                  = 1;
    var DISTRICTNAME            = 2;

    var UnusedElements          = [];

    // First, we copy over all of the canvas' #dddddd data!
    for (YY = 0, MM = 0; YY < CHEIGHT; YY++)
    {
        for (XX = 0; XX < CWIDTH; XX++, MM+=4)
        {
            if ((TheRawData.data[MM+0] == 0x99)  &&
                (TheRawData.data[MM+1] == 0x99)  &&
                (TheRawData.data[MM+2] == 0x99)  &&
                (TheRawData.data[MM+3] == 0xFF)  &&
                1)
            {
                TheReflector[YY][XX]    = 1;
            }
            else
            {
                TheReflector[YY][XX]    = 0;
            }
        }
    }

    // Now, we flood-fill the entire image.
    var TheDistrict = DISTRICTNAME;
    var DISTRICTS   = {};
    var BailOut     = false;

    for (RY = 0; (RY < CHEIGHT) && !BailOut; RY++)
    {
        for (RX = 0; (RX < CWIDTH) && !BailOut; RX++)
        {
            if (TheReflector[RY][RX] != 0)
            {
                continue;
            }

            var Exemplar    = {'y':RY, 'x':RX};

            var WorkList    = [Exemplar];
            var NumVals     = 0;
            while (WorkList.length > 0)
            {
                var Item    = WorkList.pop();
                for (YY = -1; YY <= 1; YY++)
                {
                    for (XX = -1; XX <= 1; XX++)
                    {
                        if ((YY == 0) && (XX == 0))
                        {
                            continue;
                        }
                        var whereY  = Item['y'] + YY;
                        var whereX  = Item['x'] + XX;
                        if ((whereY < 0) || (whereY >= CHEIGHT))
                        {
                            continue;
                        }
                        if ((whereX < 0) || (whereX >= CWIDTH))
                        {
                            continue;
                        }
                        if (TheReflector[whereY][whereX] > 0)
                        {
                            continue;
                        }
                        NumVals += 1;
                        TheReflector[whereY][whereX]    = TheDistrict;
                        WorkList.push({'x':whereX, 'y':whereY});
                    }
                }
            }
            DISTRICTS[TheDistrict]  = { 'People' : [] };
            TheDistrict     += 1;
        }
    }

    for (PP = 0; PP < ThePopulation.length; PP++)
    {
        var Person  = ThePopulation[PP];
        var PInfo   = TheReflector[Person['y']][Person['x']]
        if (PInfo < 2)
        {
            // Someone drew a line on top of this person!
            continue;
        }
        DISTRICTS[PInfo]['People'].push(Person);
    }

    var DistrictsWon        = {};
    DistrictsWon[FEDNAME]   = [];
    DistrictsWon[D_RNAME]   = [];

    var TheDistrictResults  = document.getElementById('results-table');
    while (TheDistrictResults.children.length > 1)
    {
        TheDistrictResults.removeChild(TheDistrictResults.children[TheDistrictResults.children.length-1]);
    }

    for (var key in DISTRICTS)
    {
        var NumFeds         = 0;
        var NumD_Rs         = 0;
        if (DISTRICTS[key]['People'].length == 0)
        {
            continue;
        }
        for (PP = 0; PP < DISTRICTS[key]['People'].length; PP++)
        {
            if (DISTRICTS[key]['People'][PP]['Party'] == 'Feds')
            {
                NumFeds     += 1;
            }
            else
            {
                NumD_Rs     += 1;
            }
        }
        var tr              = document.createElement('TR');

        var disNum          = document.createElement('TD');
        disNum.innerHTML    = key - 2;
        tr.appendChild(disNum);

        var numFeds         = document.createElement('TD');
        numFeds.innerHTML   = NumFeds;
        tr.appendChild(numFeds);

        var numD_Rs         = document.createElement('TD');
        numD_Rs.innerHTML   = NumD_Rs;
        tr.appendChild(numD_Rs);

        var numTotal        = document.createElement('TD');
        numTotal.innerHTML  = NumFeds + NumD_Rs;
        tr.appendChild(numTotal);

        var expected        = document.createElement('TD');
        if (NumFeds > NumD_Rs)
        {
            expected.innerHTML  = 'Feds';
            DistrictsWon[FEDNAME].push(key);
        }
        else if (NumFeds < NumD_Rs)
        {
            expected.innerHTML  = 'D-Rs';
            DistrictsWon[D_RNAME].push(key);
        }
        else
        {
            expected.innerHTML  = 'tie';
        }
        tr.appendChild(expected);

        TheDistrictResults.appendChild(tr);
    }

    //TheDistrictResults
    var footR                   = document.createElement('TFOOT');
    var footRow                 = document.createElement('TR');
    footR.appendChild(footRow);
    var emptyTD                 = document.createElement('TD');
    emptyTD.setAttribute('colspan', '3');
    footRow.appendChild(emptyTD);
    var totalName               = document.createElement('TD');
    totalName.innerHTML         = 'Total:';
    footRow.appendChild(totalName);
    var result                  = document.createElement('TD');
    if (DistrictsWon[FEDNAME].length > DistrictsWon[D_RNAME].length)
    {
        result.innerHTML        = 'Feds won.';
    }
    else if (DistrictsWon[FEDNAME].length < DistrictsWon[D_RNAME].length)
    {
        result.innerHTML        = 'D-Rs won.';
    }
    else
    {
        result.innerHTML        = 'Tie.';
    }
    footRow.appendChild(result);
    TheDistrictResults.appendChild(footR);
}
