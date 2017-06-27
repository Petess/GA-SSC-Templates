"""GA AEM Ross Brodie 20160606 """ 

####### Do not change anything below this line #######
 
import os
import subprocess
import sys
import re

# Set parameters
DATA_FILE       = 'frome-tempest.dat'
CONTROL_FILE    = '2'
STM_FILE        = '2'
ALTERATIONS_    = '0'
LINE_NUMBER     =  '0'
EASTING_        = '0'
NORTHING_       = 'undefined'
GROUND_ELEVATION = '0'
ALTIMETER_       = '0'
SECONDARY_X      = '0'
Z_COMPONENT_SECONDARY  = '0'
FID_          = '0'
TX_HEIGHT     = '0'
TX_ROLL       = '0'
TX_PITCH      = '0'
TX_YAW        = '0'
TX_RX_DX      = '0'
TX_RX_DY      = '0'
TX_RX_DZ      = '0'
RX_ROLL       = '0'
RX_PITCH      = '0'
RX_YAW        = '0'
POS_LAYER_BOTTOM = '0'
NEG_LAYER_BOTTOM = '0'
INTERFACE_ELEVATION   = '0'
PARAMETER_SENSITIVITY = '0'
PARAMETER_UNCERTAINTY = '0'
PREDICTED_DATA        = '0'
MAXIMUM_ITERATIONS    = '0'
SUBSAMPLE_            = '0'

# Control variables to control the iterations and sampling - allows the runs to be shortened
SUBSAMPLE_ = 'undefined'
MAXIMUM_ITERATIONS = 'undefined'

def findOccurrence( linelist, searchString):
    for x, line in enumerate(linelist):
        if searchString in line:
            return x
    return -1

def replaceInt( lines, entry, number ):
    if ( int( number ) == 0 ):
        return
    lineOccurence = findOccurrence( lines, entry )
    if ( (-1) == lineOccurence ):
        eprint( "entry: ", entry, "not found" )
    else:
        lines[lineOccurence] = \
        re.sub( r"\d+", str(number), lines[lineOccurence] )

def replaceColumnNumber( lines, entry, number ):
    if ( int( number ) == 0 ):
         return
    lineOccurence = findOccurrence( lines, entry )
    if ( (-1) == lineOccurence ):
        eprint( "entry: ", entry, "not found" )
    else:
        lines[lineOccurence] = \
        re.sub( r"Column \d+", "Column " + str(number), lines[lineOccurence] )

def replaceBoolean( lines, entry, number ):
    if ( int( number ) == 0 ):
        return
    replaceString = "yes" if ( int(number) > 0 ) else "no"
    lineOccurence = findOccurrence( lines, entry )
    if ( (-1) == lineOccurence ):
        eprint( "entry: ", entry, "not found" )
    else:
        lines[lineOccurence] = \
        re.sub( r"= yes|= no", "= " + replaceString, lines[lineOccurence] )

def replaceString( lines, entry, string ):
    lineOccurence = findOccurrence( lines, entry )
    if ( (-1) == lineOccurence ):
        eprint( "entry: ", entry, "not found" )
    else:
        parts = lines[lineOccurence].split( "=" )
        lines[lineOccurence] = parts[0] + "= " + string + "\n"

# Zcomponent may or usually has a - sign in front of it
# This function replaces the number with a sign in front of 'Column' if required
def replaceSignedColumn( lines, entry, number ):
    if ( int( number ) == 0 ):
        return
    lineOccurence = findOccurrence( lines, entry )
    if ( (-1) == lineOccurence ):
        print( "entry: ", entry, "not found" )
    else:
        if ( int( number ) < 0 ):
            lines[lineOccurence] = \
                re.sub( r"(-)?Column \d+", "-Column " + str(abs(int(number))), lines[lineOccurence] )
                # Make the number itself positive, insert - before column
        else:
            # Just insert the number
            lines[lineOccurence] = \
                re.sub( r"(-)?Column \d+", "Column " + str(number), lines[lineOccurence] )


# Set the control and stm files
controlFileDir = '/home/admin/AEMControlSTMFiles/'

# Heliborn ones
# controlFiles = [ 'Skytem_lm.con', 'Skytem_lm.con', 'VTEM-plus-7.3ms.con', 'XTEM.con' ]
# stmFiles     = [ 'Skytem-LM.stm', 'Skytem-HM.stm', 'VTEM-plus-7.3ms.stm', 'XTEM.stm' ] 
# Fixed wing
controlFiles = [ 'Geotem-ppm.con', 'Spectrum11_Z.con', 'Tempest-galeisbstdem-do-not-solve-geometry.con' ]
stmFiles = [ 'Geotem-ppm.stm', 'Spectrem-ppm-11windows.stm', ' Tempest-standard.stm' ]

controlFileBaseFileName = '/home/admin/aem/ga-aem/examples/thomson-vtem/galeisbstdem/galeisbstdem.con'
stmFile='/home/admin/aem/ga-aem/examples/thomson-vtem/stmfiles/VTEM-plus-7.3ms-pulse-southernthomson.stm'

# Set the system file 
if ( CONTROL_FILE in range(1,3) ):
    controlFileBaseFileName = controlFileDir + controlFiles[ CONTROL_FILE - 1]
else:
    print "Control File out of Range"

if ( STM_FILE in range(1,3) ):
    stmFile = controlFileDir + stmFiles[ STM_FILE - 1]
else:
    print "STM File out of Range" 

finput = open( controlFileBaseFileName,'r')
lines = finput.readlines()

columnsToReplace = [ ["LineNumber", LINE_NUMBER], ["Easting", EASTING_ ], ["Northing", NORTHING_],
                     [ "GroundElevation", GROUND_ELEVATION ], [ "Altimeter", ALTIMETER_ ], 
                     [ "FidNumber", FID_], [ "TX_Height", TX_HEIGHT], [ "TX_Pitch", TX_PITCH ],
                     [ "TX_Yaw", TX_YAW ], [ "TXRX_DX", TX_RX_DX ] , [ "TXRX_DY", TX_RX_DY ],
                     [ "TXRX_DZ", TX_RX_DZ ], [ "RX_Roll", RX_ROLL ], ["RX_Pitch", RX_PITCH ],
                     [ "RX_Yaw", RX_YAW ] ]

BoolsToReplace = [ ["PositiveLayerBottomDepths", POSITIVE_LAYER_BOTTOM_DEPTH],
                   [ "NegativeLayerBottomDepths", NEGATIVE_LAYER_BOTTOM_DEPTH],
                   [ "InterfaceElevations", INTERFACE_ELEVATIONS ],
                   [ "ParameterSensitivity", PARAMETER_SENSITIVITY ],
                   [ "ParameterUncertainty", PARAMETER_UNCERTAINTY ], [ "PredictedData", PREDICTED_DATA ] ]

replaceSignedColumn( lines, "ZComponentSecondary", Z_COMPONENT_SECONDARY )

if ALTERATIONS != 0:
    for item in columnsToReplace:
        replaceColumnNumber( lines, item[0], item[1] )

    for elBulli in BoolsToReplace:
        replaceBoolean( lines, elBulli[0], elBulli[1] )

    replaceInt( lines, "MaximumIterations", MAXIMUM_ITERATIONS )
    replaceInt( lines, "Subsample", SUBSAMPLE_ )

replaceString( lines, "DataFile", INPUT_FILE )
replaceString( lines, "SystemFile", stmFile ) 

foutputfileName = 'OutControlFile.con'
foutput = open( foutputfileName, 'w' )
foutput.write( "".join( lines ))
foutput.close()

os.path.getsize( foutputfileName )
subprocess.call(["cloud", "upload", foutputfileName, foutputfileName, "--set-acl=public-read"])

subprocess.call(["galeisbstdem.exe",foutputfileName])

subprocess.call(["cloud", "upload", "inversion.output.0000.asc", "inversion.output.0000.asc", "--set-acl=public-read"])
subprocess.call(["cloud", "upload", "inversion.output.0000.dfn", "inversion.output.0000.dfn", "--set-acl=public-read"])
