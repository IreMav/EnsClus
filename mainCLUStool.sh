#!/bin/bash

# Information required by the CLUStool:
#-------------------------------about paths------------------------------------------
# Input data directory:
INPUT_PATH=/home/mavilia/DATA/historical/prRegrid/

# Input file names strart from string:
string=pr_Amon

# OUTPUT directory
OUTPUT_PATH=/home/mavilia/MAGIC/

# CLUStool directory
CLUSTOOL_PATH=/home/mavilia/MAGIC/EnsClus/clus/
#-------------------------------about data-------------------------------------------
# Write only letters or numbers, no punctuation marks!
# If you want to leave the field empty write 'no' 
varname=pr                      #variable name in the file
varunits="kg m-2 s-1"           #variable units (K, 'kg m-2 s-1')
model=ECEARTH31                 #model name ECEARTH31 NCEPNCAR ERAInterim
numens=60                       #total number of ensemble members
season=JJA                      #seasonal average
area=Eu                         #regional average (examples:'EAT':Euro-Atlantic
                                #                           'PNA': Pacific North American
                                #                           'NH': Northern Hemisphere)
                                #                           'Eu': Europe)
kind=hist                       #hist: historical, scen:scenario
extreme=75th_percentile         #75th_percentile, mean, maximum, std, trend

#---------------------about cluster analysis------------------------------------------
numclus=6                       #number of clusters
#Either set perc or numpcs:
perc=80                         #cluster analysis is applied on a number of PCs such as they explain
                                #'perc' of total variance
numpcs=no                       #number of PCs

name_outputs="${varname}_${model}_${numens}ens_${season}_${area}_${kind}"

##PRECOMPUTATION
filenames=`grep -rnl $INPUT_PATH -e $string`
for word in $filenames; do
    echo $word
done

python ${CLUSTOOL_PATH}ens_anom.py "$filenames" "$OUTPUT_PATH" "$name_outputs" "$varname" "$numens" "$season" "$area" "$extreme"

##ENSEMBLE EOF and K-MEANS
python ${CLUSTOOL_PATH}ens_eof_kmeans.py "$OUTPUT_PATH" "$name_outputs" "$numens" "$numpcs" "$perc" "$numclus"

ls -lrt ../OUTPUT

echo ">>>>>>>> ENDED SUCCESSFULLY!! <<<<<<<<<<<<"
