#*********************************
#           ens_plots            *
#*********************************

# Standard packages
import os

# User-defined libraries
sys.path.insert(0,dir_CLUStool)
from eof_tool import eof_plots

def ens_plots(dir_OUTPUT,name_outputs,neof):
    '''
    \nGOAL:
    Plot the nth PCs and the EOFs
    NOTE:
    '''
    varname=name_outputs.split("_")[0]
    model=name_outputs.split("_")[1]

    neof=neof-1   # EOF to plot (neof starts from zero!)
    tit='{0} {1}'.format(varname,model)
    eof_plots(neof,pcs_scal1, eofs_scal2,lat,lon,tit,numens)

    # plot the PCs
    namef=os.path.join(OUTPUTdir,'PCs{0}_{1}.eps'.format(neof+1,name_outputs))
    figPC.savefig(namef)#bbox_inches='tight')
    
    # plot the EOFs
    namef=os.path.join(OUTPUTdir,'EOFs{0}_{1}.eps'.format(neof+1,name_outputs))
    figEOF.savefig(namef)#bbox_inches='tight')
    print('PCs and EOFs eps figure are saved in {0}'.format(OUTPUTdir))
    print('____________________________________________________________________________________________________________________')
