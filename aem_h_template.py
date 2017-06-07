"""GA AEM Ross Brodie 20160606 """ 

####### Do not change anything below this line #######
 
import os
import subprocess
import sys
import re

# Set parameters
DATA_FILE     = '${aem_h_data_file}'
CONTROL_FILE  = '${aem_h_control_file}'
STM_FILE      = '${aem_h_system_file}'
ALTERATIONS_  = '${aem_h_Alter_Values}'
LINE_NUMBER   = '${aem_h_line_number}'
EASTING_      = '${aem_h_easting}'
NORTHING_     = '${aem_h_northing}'
GROUND_ELEVATION = '${aem_h_ground_elevation}'
ALTIMETER_       = '${aem_h_altimeter}'
Z_COMPONENT_SECONDARY = '${aem_h_Z_Comp_Secondary}'
Z_COMPONENT_TERTIARY  = '${aem_h_Z_Comp_Tertiary}'
FID_          = '${aem_h_FID_Column}'
TX_HEIGHT     = '${aem_h_TX_Height}'
TX_ROLL       = '${aem_h_TX_Roll}'
TX_PITCH      = '${aem_h_TX_Pitch}'
TX_YAW        = '${aem_h_TX_Yaw}'
TX_RX_DX      = '${aem_h_TXRX_DX}'
TX_RX_DY      = '${aem_h_TXRX_DY}'
TX_RX_DZ      = '${aem_h_TXRX_DZ}'
RX_ROLL       = '${aem_h_RX_Roll}'
RX_PITCH      = '${aem_h_RX_Pitch}'
RX_YAW        = '${aem_h_RX_Yaw}'
POS_LAYER_BOTTOM    = '${aem_h_pve_bottom_layer_depth}'
NEG_LAYER_BOTTOM    = '${aem_h_nve_bottom_layer_depth}'
INTERFACE_ELEVATION = '${aem_h_interface_elevations}'
PARAMETER_SENSITIVITY  = '${aem_h_parameter_sensitivity}'
PARAMETER_UNCERTAINTY  = '${aem_h_parameter_uncertainty}'
PREDICTED_DATA         = '${aem_h_predicted_data}'
MAXIMUM_ITERATIONS     = '${aem_h_max_iterations}'
SUBSAMPLE_             = '${aem_h_subsample}'

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


finputfileName = '/home/admin/aem/ga-aem/examples/thomson-vtem/galeisbstdem/galeisbstdem.con'
stmFile='/home/admin/aem/ga-aem/examples/thomson-vtem/stmfiles/VTEM-plus-7.3ms-pulse-southernthomson.stm'
finput = open(finputfileName,'r')
lines = finput.readlines()


columnsToReplace = [ ["LineNumber", LINE_NUMBER], ["Easting", EASTING_ ], ["Northing", NORTHING_],
                     [ "GroundElevation", GROUND_ELEVATION ], [ "Altimeter", ALTIMETER_ ], 
                     ["FidNumber", FID_], ["TX_Height", TX_HEIGHT], [ "TX_Pitch", TX_PITCH ],
                     [ "TX_Yaw", TX_YAW ], [ "TXRX_DX", TX_RX_DX ] , 
                     [ "TXRX_DY", TX_RX_DY ], [ "TXRX_DZ", TX_RX_DZ ], [ "RX_Roll", RX_ROLL ],
                     ["RX_Pitch", RX_PITCH ] ,[ "RX_Yaw", RX_YAW ] ]

BoolsToReplace = [ ["PositiveLayerBottomDepths", POS_LAYER_BOTTOM],
                   [ "NegativeLayerBottomDepths", NEG_LAYER_BOTTOM],
                   [ "InterfaceElevations", INTERFACE_ELEVATION ],
                   [ "ParameterSensitivity", PARAMETER_SENSITIVITY ],
                   [ "ParameterUncertainty", PARAMETER_UNCERTAINTY ],
                   [ "PredictedData", PREDICTED_DATA ] ]

if int( ALTERATIONS_ ) != 0:
    replaceSignedColumn( lines, "ZComponentSecondary", Z_COMPONENT_SECONDARY )

    for item in columnsToReplace:
        replaceColumnNumber( lines, item[0], item[1] )

    for elBulli in BoolsToReplace:
        replaceBoolean( lines, elBulli[0], elBulli[1] )

    replaceInt( lines, "MaximumIterations", MAXIMUM_ITERATIONS )
    replaceInt( lines, "Subsample", SUBSAMPLE_ )

replaceString( lines, "DataFile", DATA_FILE )
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
