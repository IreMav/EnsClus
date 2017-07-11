'''
PYTHON WRAPPER ensemble clustering
    It provides input for the following modules: ens_anom.py ens_eof_kmeans.py
    and it executes them
'''
# Standard packages
import os
import sys

# Information required by the CLUStool:
#-------------------------------about paths------------------------------------------
# Input data directory:
INPUT_PATH='/home/mavilia/DATA/historical/prRegrid/'
string='pr_Amon'

# OUTPUT directory
dir_OUTPUT='/home/mavilia/MAGIC/'

# CLUStool directory
dir_CLUStool='/home/mavilia/MAGIC/EnsClus/clus/'

# User-defined packages
sys.path.insert(0,dir_CLUStool)
from ens_anom import ens_anom
from ens_of_kmeans import ens_eof_kmeans

#-------------------------------about data-------------------------------------------
# Write only letters or numbers, no punctuation marks!
# If you want to leave the field empty write 'no' 
varname='pr'                #variable name in the file
varunits="kg m-2 s-1"       #variable units (K, 'kg m-2 s-1')
model='ECEARTH31'           #model name ECEARTH31 NCEPNCAR ERAInterim


numens=60                   #total number of ensemble members
season='JJA'                #seasonal average
area='Eu'                   #regional average (examples:'EAT':Euro-Atlantic
                            #                           'PNA': Pacific North American
                            #                           'NH': Northern Hemisphere)
                            #                           'Eu': Europe)
kind='hist'                 #hist: historical, scen:scenario
extreme='75th_percentile'   #75th_percentile, mean, maximum

#---------------------about cluster analysis------------------------------------------
numclus=6              #number of clusters
#Either set perc or numpcs:
perc=80               #cluster analysis is applied on a number of PCs such as they explain
                       #'perc' of total variance
numpcs='no'               #number of PCs

s = "_";
seq = (varname,model,str(numens)+'ens',season,area,kind)
name_outputs=s.join(seq)
print(name_outputs)

#____________Building the array of file names
fn = [i for i in os.listdir(INPUT_PATH) \
    if os.path.isfile(os.path.join(INPUT_PATH,i)) and string in i]
filenames=[os.path.join(INPUT_PATH,i) for i in fn]
print(string)
print('_______________________\nARRAY OF {0} FILE NAMES:'.format(len(filenames)))
for i in filenames:
    print(i)

####################### PRECOMPUTATION #######################
#____________run ens_anom as a module
ens_anom(filenames,dir_OUTPUT,dir_CLUStool,name_outputs,varunits,string,extreme)


####################### EOF AND K-MEANS ANALYSES #######################
#____________run ens_anom as a module
ens_eof_kmeans(dir_OUTPUT,dir_CLUStool,name_outputs,varunits,numpcs,perc,numclus)


