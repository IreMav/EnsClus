#!/usr/bin/env python3 

'''
;;#############################################################################
;; Ensemble Clustering Diagnostics
;; Author: Irene Mavilia (ISAC-CNR, Italy)
;; Copernicus C3S 34a lot 2 (MAGIC)
;;#############################################################################
;; Description
;;    Cluster analysis tool based on the k-means algorithm 
;;    for ensembles of climate model simulations
;;
;; Modules called: ens_anom.py and ens_eof_kmeans.py
;;
;; Modification history
;;    20170905-A_mavi_ir: stand-alone version of the ESMValTool diagnostic.
;;
;;#############################################################################
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
from ens_eof_kmeans import ens_eof_kmeans

#-------------------------------about data-------------------------------------------
# Write only letters or numbers, no punctuation marks!
# If you want to leave the field empty write 'no' 
varname='pr'                #variable name in the file
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
perc=80                #cluster analysis is applied on a number of PCs such as they explain
                       #'perc' of total variance
numpcs='no'            #number of PCs

#____________Building the name of output files
s = "_";
seq = (varname,model,str(numens)+'ens',season,area,kind)
name_outputs=s.join(seq)
#print('The name of the output files will be <variable>_{0}.ext'.format(name_outputs))

# Creating the log file in the Log directory
if not os.path.exists(dir_OUTPUT+'Log'):
    os.mkdir(dir_OUTPUT+'Log')
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()

f = open(dir_OUTPUT+'Log/Printed_messages.txt', 'w')
original = sys.stdout
sys.stdout = Tee(sys.stdout, f)


#____________Building the array of file names
fn = [i for i in os.listdir(INPUT_PATH) \
    if os.path.isfile(os.path.join(INPUT_PATH,i)) and string in i]
filenames=[os.path.join(INPUT_PATH,i) for i in fn]

print('\n***********************************INPUT***********************************')
print('Input file names contain the string: {0}'.format(string))
print('_____________________________\nARRAY OF {0} INPUT FILES:'.format(len(filenames)))
for i in filenames:
    print(i)
print('_____________________________\n')

####################### PRECOMPUTATION #######################
#____________run ens_anom as a module
ens_anom(filenames,dir_OUTPUT,name_outputs,varname,numens,season,area,extreme)

####################### EOF AND K-MEANS ANALYSES #######################
#____________run ens_eof_kmeans as a module
ens_eof_kmeans(dir_OUTPUT,name_outputs,numens,numpcs,perc,numclus)

print('\n>>>>>>>>>>>> ENDED SUCCESSFULLY!! <<<<<<<<<<<<\n')

sys.stdout = original
f.close()


