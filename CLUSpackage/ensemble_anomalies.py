#*********************************
#      ensemble_anomalies        *
#*********************************

# Standard packages
import numpy as np
import sys
import os

def ensemble_anomaly(dir_DATA,dir_OUTPUT,dir_PYtool,name_outputs,varunits,string,extreme):
    '''
    '''
    #____________Reading the netCDF file of 3Dfield, for all the ensemble members
    fn = [i for i in os.listdir(dir_DATA) \
        if os.path.isfile(os.path.join(dir_DATA,i)) and string in i]
    fn.sort()
    var_ens=[]
    print(string)
    for fil in fn:
        print(fil)
    for ens in range(numens):
        ifile=dir_DATA+fn[ens]
        print('\n/////////////////////////////////////\nENSEMBLE MEMBER %s' %ens)
        var, lat, lon, dates, time_units = read3Dncfield(ifile)
    
        #____________Convertion from kg m-2 s-1 to mm/day
        if varunits=='kg m-2 s-1':
            var=var*86400  #there are 86400 seconds in a day
            print('____________________________________________________________________________________________________________________')
            print('Precipitation rate units are converted from kg m-2 s-1 to mm/day')
            varunitsnew='mm/day'
        else:
            varunitsnew=varunits
    
        #____________Selecting a season (DJF,DJFM,NDJFM,JJA)
        var_season,dates_season=sel_season(var,dates,season)
        
        #____________Selecting only [latS-latN, lonW-lonE] box region
        var_area,lat_area,lon_area=sel_area(lat,lon,var_season,area)
        
        var_ens.append(var_area)
    
    print('\n----------------------------------------')
    print('Original var shape: (time x lat x lon)={0}'.format(var.shape))
    print('var shape after selecting season {0}: (time x lat x lon)={1}'.format(season,var_season.shape))
    print('var shape after selecting season {0} and area {1}: (time x lat x lon)={2}'.format(season,area,var_area.shape))
    print('Check the number of ensemble members: {0}'.format(len(var_ens)))
    

    if extreme=='mean':
        #____________Compute the time mean over the entire period, for each ensemble member
        varextreme_ens=[np.mean(var_ens[i],axis=0) for i in range(numens)]
    elif extreme.split("_")[1]=='percentile':
        #____________Compute the time mean over the extremes, for each ensemble member
        # PERCENTILE
        q=int(extreme.partition("th")[0])
        varextreme_ens=[np.percentile(var_ens[i],q,axis=0) for i in range(numens)]
    elif extreme=='maximum':
        #____________Compute the time mean over the extremes, for each ensemble member
        # MAXIMUM
        varextreme_ens=[np.max(var_ens[i],axis=0) for i in range(numens)]
    
    print('\nanomalies respect to the {0}'.format(extreme))
    varextreme_ens_np=np.array(varextreme_ens)
    print('var shape: (numens x lat x lon)={0}'.format(varextreme_ens_np.shape))
    
    #____________Compute the anomalies with respect to the ensemble
    ens_anomalies=varextreme_ens_np-np.mean(varextreme_ens_np,axis=0)
    print('ens_anomalies shape: (numens x lat x lon)={0}'.format(ens_anomalies.shape))
    
    
    #____________Compute and save the climatology
    vartimemean_ens=[np.mean(var_ens[i],axis=0) for i in range(numens)]
    ens_climatologies=np.array(vartimemean_ens)
    varsave='ens_climatologies'
    ofile=os.path.join(OUTPUTdir,'ens_climatologies_{0}.nc'.format(name_outputs))
    print(ofile)
    save_N_2Dfields(lat_area,lon_area,ens_climatologies,varsave,varunitsnew,ofile)
    
    #____________Save the extreme
    ens_extreme=varextreme_ens_np
    varsave='ens_extreme'
    ofile=os.path.join(OUTPUTdir,'ens_extreme_{0}.nc'.format(name_outputs))
    print(ofile)
    save_N_2Dfields(lat_area,lon_area,ens_extreme,varsave,varunitsnew,ofile)
    
    
    #____________Save the anomalies
    varsave='ens_anomalies'
    ofile=os.path.join(OUTPUTdir,'ens_anomalies_{0}.nc'.format(name_outputs))
    print(ofile)
    save_N_2Dfields(lat_area,lon_area,ens_anomalies,varsave,varunitsnew,ofile)

    return

#========================================================

if __name__ == '__main__':
    print('This program is being run by itself')
    
    print('**************************************************************')
    print('Running {0}'.format(sys.argv[0]))
    print('**************************************************************')
    dir_DATA      = sys.argv[1]  # INPUT DIRECTORY
    dir_OUTPUT    = sys.argv[2]  # OUTPUT DIRECTORY
    dir_PYtool    = sys.argv[3]  # CLUS_tool DIRECTORY
    name_outputs  = sys.argv[4]  # name of the outputs
    varunits      = sys.argv[5]  # variable units
    string        = sys.argv[6]  # part of the input file name
    extreme       = sys.argv[7]  # chosen extreme to investigate
    
    print(name_outputs)
    varname=name_outputs.split("_")[0]
    print('variable name: {0} ({1})'.format(varname,varunits))
    numens=int(name_outputs.split("_")[2][:-3].upper())
    print('number of ensemble members: {0}'.format(numens))
    season=name_outputs.split("_")[3]          #seasonal average
    area=name_outputs.split("_")[4]            #regional average (examples:'EAT':Euro-Atlantic,'PNA': Pacific North American)
    
    # User-defined libraries
    sys.path.insert(0,dir_PYtool+'CLUSpackage/')
    from readNetCDF import read3Dncfield, save_N_2Dfields
    from sel_SeasonArea import sel_season, sel_area
    
    # OUTPUT DIRECTORY
    OUTPUTdir=dir_OUTPUT+'OUTPUT/'
    if not os.path.exists(OUTPUTdir):
        os.mkdir(OUTPUTdir)
        print('The output directory {0} is created'.format(OUTPUTdir))
    else:
        print('The output directory {0} already exists'.format(OUTPUTdir))

    ensemble_anomaly(dir_DATA,dir_OUTPUT,dir_PYtool,name_outputs,varunits,string,extreme)

else:
    print('I am being imported from another module')

