#*********************************
#        ens_eof_kmeans          *
#*********************************

# Standard packages
import numpy as np
import sys
import os
from sklearn.cluster import KMeans
import datetime
from numpy import linalg as LA

def ens_eof_kmeans(dir_OUTPUT,dir_CLUStool,name_outputs,varunits,numpcs,perc,numclus):
    '''
    \nGOAL:
    Find the most representative ensemble member for each cluster.
    METHODS:
    - Empirical Orthogonal Function (EOF) analysis of the input file
    - K-means cluster analysis applied to the retained Principal Components (PCs)
    OUTPUT: 
    '''
    print(name_outputs)
    varname=name_outputs.split("_")[0]
    print('variable name: {0} ({1})'.format(varname,varunits))
    model=name_outputs.split("_")[1]
    print('model: {0}'.format(model))
    
    numens=int(name_outputs.split("_")[2][:-3].upper())
    print('number of ensemble members: {0}'.format(numens))

    if numpcs!='no':
        numpcs=int(numpcs)
        print('number of principal components: {0}'.format(numpcs))
    
    if perc!='no':
        perc=int(perc)
        print('percentage of explained variance: {0}%'.format(perc))
    
    if (perc=='no' and numpcs=='no') or (perc!='no' and numpcs!='no'):
        raise ValueError('You have to specify either "perc" or "numpcs".')
    
    print('number of clusters: {0}'.format(numclus))
    
    # User-defined libraries
    sys.path.insert(0,dir_CLUStool)
    from read_netcdf import read_N_2Dfields
    from eof_tool import eof_computation
    
    # OUTPUT DIRECTORY
    OUTPUTdir=dir_OUTPUT+'OUTPUT/'
    if not os.path.exists(OUTPUTdir):
        os.mkdir(OUTPUTdir)
        print('The output directory {0} is created'.format(OUTPUTdir))
    else:
        print('The output directory {0} already exists'.format(OUTPUTdir))

    #____________Reading the netCDF file of N 2Dfields of anomalies, saved by ensemble_anomalies.py
    ifile=os.path.join(OUTPUTdir,'ens_anomalies_{0}.nc'.format(name_outputs))
    var, lat, lon = read_N_2Dfields(ifile)
    print('var shape: (numens x lat x lon)={0}'.format(var.shape))
    
    
    #____________Compute EOFs (Empirical Orthogonal Functions)
    #____________and PCs (Principal Components) with respect to ensemble memeber
    print('____________________________________________________________________________________________________________________')
    print('EOF analysis')
    #----------------------------------------------------------------------------------------
    solver, pcs_scal1, eofs_scal2, pcs_unscal0, eofs_unscal0, varfrac = eof_computation(var,varunits,lat,lon)
        
    acc=np.cumsum(varfrac*100)
    if perc!='no':
        # Find how many PCs explain a certain percentage of variance
        # (find the mode relative to the percentage closest to perc, but bigger than perc)
        numpcs=min(enumerate(acc), key=lambda x: x[1]<=perc)[0]+1
        print('\nThe number of PCs that explain the percentage closest to {0}% of variance (but grater than {0}%) is {1}'.format(perc,numpcs))
        exctperc=min(enumerate(acc), key=lambda x: x[1]<=perc)[1]
    if numpcs!='no':
        exctperc=acc[numpcs-1]
    print('(the first {0} PCs explain exactly the {1}% of variance)'.format(numpcs,"%.2f" %exctperc))
    

    #____________Compute k-means analysis using a subset of PCs
    print('____________________________________________________________________________________________________________________')
    print('k-means analysis using a subset of PCs')
    #----------------------------------------------------------------------------------------
    PCs=pcs_unscal0[:,:numpcs]
    
    clus=KMeans(n_clusters=numclus, n_init=600, max_iter=1000)
    
    start = datetime.datetime.now()
    clus.fit(PCs)
    end = datetime.datetime.now()
    print('k-means algorithm took me %s seconds' %(end-start))
    
    centroids=clus.cluster_centers_          # shape---> (numclus,numpcs)
    labels=clus.labels_                      # shape---> (numens,)
    
    print('\nClusters are identified for {0} PCs (explained variance {1}%)'.format(numpcs, "%.2f" %exctperc))
    print('Centroids shape: {0}, labels shape: {1}\n'.format(centroids.shape,labels.shape))
    print('PC shape: {0}, EOF shape: {1}\n'.format(pcs_unscal0[:,:numpcs].shape,eofs_unscal0[:numpcs].shape))
    
    #____________Save labels
    namef=os.path.join(OUTPUTdir,'frequency_index_{0}.txt'.format(name_outputs))
    np.savetxt(namef,labels,fmt='%d')
    
    #____________Compute cluster patterns
    cluspattern=np.empty([numclus,var.shape[1],var.shape[2]])
    L=[]
    for nclus in range(numclus):
        cl=list(np.where(labels==nclus)[0])
        fr=len(cl)*100/len(labels)
        cluspattern[nclus,:,:]=np.mean(var[cl,:,:],axis=0)
        L.append([nclus,fr,cl])
    print('[[cluster, frequency (%), [members belonging to that cluster]]]:\n{0}'.format(L))
    print('\nCluster patterns shape: {0}'.format(cluspattern.shape))
    
    print('Cluster labels')
    print(L[0][0],L[1][0],L[2][0],L[3][0])
    print('Cluster frequencies')
    print(L[0][1],L[1][1],L[2][1],L[3][1]) 
    print('Cluster members')
    print(L[0][2],L[1][2],L[2][2],L[3][2])
    
    #____________Find the most representative ensemble memeber for each cluster
    print('____________________________________________________________________________________________________________________')
    print('Compute distance between cluster centroids and each ensemble member,\nin order to find the most representative ensemble memeber for each cluster')
    print('____________________________________________________________________________________________________________________')
    print('Compute centroid-PC norm')
    # 1)
    print('DIM cluster 1 centroid: {0}'.format(centroids[1,:].shape))
    print('DIM ensemble member 1 PC: {0}'.format(PCs[1,:].shape))
    #print('\nIn the PC space, the distance between:')
    norm=np.empty([numclus,numens])
    finalOUTPUT=[]
    for nclus in range(numclus):
        for ens in range(numens):
            normens=LA.norm(centroids[nclus,:]-PCs[ens,:])
            #print('centroid of cluster {0} and ensemble memeber {1} is {2}'.format(nclus,ens,normens))
            norm[nclus,ens]=normens
        print('MINIMUM FOR CLUS {0} IS {1}'.format(nclus,norm[nclus].min()))
        print('ARG MINIMUM FOR CLUS {0} IS {1}'.format(nclus,list(np.where(norm[nclus] == norm[nclus].min())[0])))
        txt='Closest ensemble member/members to centroid of cluster {0} is/are {1}\n'.format(nclus,list(np.where(norm[nclus] == norm[nclus].min())[0]))
        finalOUTPUT.append(txt)
        repres=list(np.where(norm[nclus] == norm[nclus].min())[0])
        #____________Save the most representative ensemble members
        namef=os.path.join(OUTPUTdir,'repr_ens_{0}.txt'.format(name_outputs))
        with open(namef,'ab') as f_handle:
            np.savetxt(f_handle,repres,fmt='%i')
    
    with open(OUTPUTdir+'RepresentativeEnsembleMembers_{0}.txt'.format(name_outputs), "w") as text_file:
        text_file.write(''.join(str(e) for e in finalOUTPUT))
    
    print('\nIn the PC space, the distance between each ensemble in a cluster and its centroid:')
    norm=np.empty([numclus,numens])
    for nclus in range(numclus):
        for ens in range(numens):
            normens=LA.norm(centroids[nclus,:]-PCs[ens,:])
            norm[nclus,ens]=normens
        print('MAXIMUM FOR CLUS {0} IS {1}'.format(nclus,norm[nclus].max()))
        print('ARG MAXIMUM FOR CLUS {0} IS {1}'.format(nclus,list(np.where(norm[nclus] == norm[nclus].max())[0])))
        txt='Furthest ensemble member/members to centroid of cluster {0} is/are {1}\n'.format(nclus,list(np.where(norm[nclus] == norm[nclus].max())[0]))
        print(txt)
        print('==============================================================')
        print('INTRA-CLUSTER STANDARD DEVIATION FOR CLUS {0} IS {1}'.format(nclus,norm[nclus].std()))
    
    
    ## 2)
    #norm=[]
    #p_centroid=np.empty([numclus,numpcs])
    #for nclus in range(numclus):
    #    p_centroid[nclus,:] = solver.projectField(cluspattern[nclus],neofs=numpcs, eofscaling=0, weighted=True)
    #    for ens in range(numens):
    #        norm.append(LA.norm(p_centroid[nclus,:]-PCs[ens,:]))
    #print('DIM cluster projection 1 centroid: {0}'.format(p_centroid[1,:].shape))
    #print('DIM ensemble member 1 PC: {0}'.format(PCs[1,:].shape))
    #print('\nnorm=',norm)
    
    return


#========================================================

if __name__ == '__main__':
    print('This program is being run by itself')
    
    print('**************************************************************')
    print('Running {0}'.format(sys.argv[0]))
    print('**************************************************************')
    dir_OUTPUT    = sys.argv[1]  # OUTPUT DIRECTORY
    dir_CLUStool  = sys.argv[2]  # CLUS_tool DIRECTORY
    name_outputs  = sys.argv[3]  # name of the outputs
    varunits      = sys.argv[4]  # variable units
    numpcs        = sys.argv[5]  # number of retained PCs
    perc          = sys.argv[6]  # percentage of explained variance by PCs
    numclus       = int(sys.argv[7])  # number of clusters
    
    ens_eof_kmeans(dir_OUTPUT,dir_CLUStool,name_outputs,varunits,numpcs,perc,numclus)
    
else:
    print('I am being imported from another module')
