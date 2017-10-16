# EnsClus
EnsClus is a cluster analysis tool, based on the k-means algorithm, for ensembles of climate model simulations.
The aim is to group ensemble members according to similar characteristics and to select the most representative member for each cluster.

The user choose which feature of the data is used to group the ensemble members by the clustering: the time mean, the maximum or a certain percentile over the time period.
Therefore, for each ensemble member this value is computed obtaining N lat-lon maps, where N is the number of ensemble members.
The anomaly is computed subtracting the ensemble mean of these maps to each of the single maps. The anomaly is therefore computed with respect to the ensemble members (and not with respect to the time) and the Empirical Orthogonal Function (EOF) analysis is applied to these anomaly maps.
Regarding the EOF analysis, the user can choose either how many Principal Components (PCs) the user wants to retain or the percentage of explained variance the user wants to keep.
After reducing dimensionality via EOF analysis, k-means analysis is applied using the desired subset of PCs.

The major final outputs are the classification in clusters, i.e. which member belongs to which cluster (in k-means analysis the number k of clusters needs to be defined prior to the analysis) and the most representative member for each cluster, which is the closest member to the cluster centroid.
Other outputs refer to the statistics of clustering: in the PC space, the minumum and the maximum distance between a member in a cluster and the cluster centroid (i.e. the closest and the furthest member), the intra-cluster standard deviation for each cluster (i.e. how much the cluster is compact).
