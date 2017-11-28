# Ensemble Clustering (EnsClus)
October 2017
by Irene Mavilia (ISAC-CNR, i.mavilia@isac.cnr.it)

## Overview
**EnsClus** is a cluster analysis tool in Python, based on the k-means algorithm, for ensembles of climate model simulations. The aim is to group ensemble members according to similar characteristics and to select the most representative member for each cluster. The user choose which feature of the data is used to group the ensemble members by the clustering: time mean, maximum, a certain percentile (75% in the examples below), standard deviation and trend over the time period.
For each ensemble member this value is computed at each grid point, obtaining N lat-lon maps, where N is the number of ensemble members.
The anomaly is computed subtracting the ensemble mean of these maps to each of the single maps. The anomaly is therefore computed with respect to the ensemble members (and not with respect to the time) and the Empirical Orthogonal Function (EOF) analysis is applied to these anomaly maps.
Regarding the EOF analysis, the user can choose either how many Principal Components (PCs) the user want to retain or the percentage of explained variance the user want to keep.
After reducing dimensionality via EOF analysis, k-means analysis is applied using the desired subset of PCs.
The major final outputs are the classification in clusters, i.e. which member belongs to which cluster (in k-means analysis the number k of clusters needs to be defined prior to the analysis) and the most representative member for each cluster, which is the closest member to the cluster centroid.
Other outputs refer to the statistics of clustering: in the PC space, the minimum and the maximum distance between a member in a cluster and the cluster centroid (i.e. the closest and the furthest member), the intra-cluster standard deviation for each cluster (i.e. how much the cluster is compact).

## Details
Two equivalent wrappers, a shell wrapper (mainCLUStool.sh) and a Python wrapper (mainCLUStool.py), are provided to launch the tool. Note that only the Python wrapper creates a Log folder with a text file of all the printed messages, so far. The wrappers accept and pass the set of parameters required by the EnsClus tool.

Use either ```./mainCLUStool.sh``` command or ```./mainCLUStool.py``` command to launch the tool.
### Input
One directory should contain a single NetCDF file (time, lat, lon) for each ensemble member.
The list of input files are retrieved by the tool from the data directory path and from a common string included in all and only the ensemble member file names the user want to use.
Input parameters are: variable name, as in the NetCDF data file, model name, if all members belong to the same model, total number of ensemble members, season (DJF, DJFM, NDJFM, JJA so far) if the seasonal average is needed, area (EAT, PNA, NH so far) is selecting a box region is needed, kind of simulations (historical, scenario), value to investigate (??th_percentile, mean, maximum, standard deviation, trend), number of clusters, either set percentage of variance explained by PCs or directly the number of PC to retain (cluster analysis is applied on such subset of PCs).
### Modules
* *ens_anom.py*

The module computes the ensemble anomalies based on the desired value from the input variable (percentile, mean, maximum, standard deviation or trend): the anomalies are computed subtracting the ensemble mean of the N maps of chosen value, from each map.
* *ens_eof_kmeans.py*

The module reads the netCDF file of anomalies, saved by ens_anom.py and computes the Empirical Orthogonal Function (EOF) analysis of the input file. The K-means cluster analysis is then applied to the retained Principal Components (PCs) and each member is assigned to a cluster. Frequency of occurrence and belonging members of the clusters are given. In order to find the most representative ensemble member for each cluster, which is the closest member to the cluster centroid, the Euclidean distance between cluster centroids and each ensemble member is computed in the PC space. Statistics of clustering as the minimum, the maximum and the standard deviation of the distances between each member in a cluster and the cluster centroid are computed.
### Output
The ens_anom.py module provides three NetCDF files of dimension (N, lat, lon) that are the maps of climatology, selected value and anomaly for the N members. A vector of N cluster labels, the most representative ensemble member for each cluster and statistics of clusters are saved in text files by the ens_eof_kmeans.py module. Specifically, the file containing statistcs of clusters includes, for each cluster, the Euclidean distances in PC space between the members belonging to that cluster and the cluster centroid, the maximum and minimum distances, the standard deviation of intra-cluster distances and the frequency of that cluster.

## References
Straus et al. 2007 (Straus, D. M., S. Corti, and F. Molteni, 2007: Circulation regimes: Chaotic variability vs. SST forced predictability. J. Climate, 20, 2251–2272).

## Examples
![magic_example1](https://user-images.githubusercontent.com/29089954/31949406-8a651110-b8d9-11e7-8b0d-11a1c5a0fc9b.png)



![magic_example2](https://user-images.githubusercontent.com/29089954/31949425-92250004-b8d9-11e7-9468-18e7bceb9f8d.png)
