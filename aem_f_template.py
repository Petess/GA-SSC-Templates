"""GA AEM Ross Brodie 20160606 """ 

####### Do not change anything below this line #######
 
import os
import subprocess
import sys
import re

# Set parameters
DATA_FILE       = '${aem_f_data_file}'
CONTROL_FILE    = '${aem_f_control_file}'
STM_FILE        = '${aem_f_stm_file}'
ALTERATIONS_    = '${aem_f_alterations}'
LINE_NUMBER     =  '${aem_f_line_number}'
EASTING_        = '${aem_f_easting}'
NORTHING_       = '${aem_f_northing}'
GROUND_ELEVATION = '${aem_f_ground_elevation}'
ALTIMETER_       = '${aem_f_altimeter}'
SECONDARY_X      = '${aem_f_Secondary_X}'
Z_COMPONENT_SECONDARY  = '${aem_f_Z_Component_Secondary}'
FID_          = '${aem_f_FID}'
TX_HEIGHT     = '${aem_f_tx_height}'
TX_ROLL       = '${aem_f_tx_roll}'
TX_PITCH      = '${aem_f_tx_pitch}'
TX_YAW        = '${aem_f_tx_yaw}'
TX_RX_DX      = '${aem_f_txrx_dx}'
TX_RX_DY      = '${aem_f_txrx_dy}'
TX_RX_DZ      = '${aem_f_txrx_dz}'
RX_ROLL       = '${aem_f_rx_roll}'
RX_PITCH      = '${aem_f_rx_pitch}'
RX_YAW        = '${aem_f_rx_yaw}'
POS_LAYER_BOTTOM = '${aem_f_p_ve_layer_bottom}'
NEG_LAYER_BOTTOM = '${aem_f_n_ve_layer_bottom}'
INTERFACE_ELEVATION   = '${aem_f_interface_elevation}'
PARAMETER_SENSITIVITY = '${aem_f_parameter_sensitivity}'
PARAMETER_UNCERTAINTY = '${aem_f_parameter_uncertainty}'
PREDICTED_DATA        = '${aem_f_predicted_data}'
MAXIMUM_ITERATIONS    = '${aem_f_maximumIterations}'
SUBSAMPLE_            = '${aem_f_subsample}'

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
stmFiles = [ 'Geotem-ppm.stm', 'Spectrem-ppm-11windows.stm', 'Tempest-standard.stm' ]

controlFileBaseFileName = '/home/admin/aem/ga-aem/examples/thomson-vtem/galeisbstdem/galeisbstdem.con'
stmFile='/home/admin/aem/ga-aem/examples/thomson-vtem/stmfiles/VTEM-plus-7.3ms-pulse-southernthomson.stm'

# Set the system file 
if ( int( CONTROL_FILE ) in range(1,4) ):
    controlFileBaseFileName = controlFileDir + controlFiles[ int( CONTROL_FILE ) - 1]
else:
    print "Control File out of Range"

if ( int( STM_FILE ) in range(1,4) ):
    stmFile = controlFileDir + stmFiles[ int ( STM_FILE ) - 1]
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

BoolsToReplace = [ ["PositiveLayerBottomDepths", POS_LAYER_BOTTOM ],
                   [ "NegativeLayerBottomDepths", NEG_LAYER_BOTTOM ],
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

# Always need to update the data and system files
replaceString( lines, "DataFile", DATA_FILE )
replaceString( lines, "SystemFile", stmFile ) 

foutputfileName = 'OutControlFile.con'
foutput = open( foutputfileName, 'w' )
foutput.write( "".join( lines ))
foutput.close()

os.path.getsize( foutputfileName )
subprocess.call(["cloud", "upload", foutputfileName, foutputfileName, "--set-acl=public-read"])

# subprocess.call(["galeisbstdem.exe",foutputfileName])

# subprocess.call(["cloud", "upload", "inversion.output.0000.asc", "inversion.output.0000.asc", "--set-acl=public-read"])
# subprocess.call(["cloud", "upload", "inversion.output.0000.dfn", "inversion.output.0000.dfn", "--set-acl=public-read"])
