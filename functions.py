# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:54:26 2024

@author: leool650

"""


#%% Libraries

from datetime import date, datetime
from plotnine import *
import pandas as pd
import patchworklib as pw
import geopandas as gpd
from scipy.stats import t
import statsmodels


#%% Data preparation 


def prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=None,lower_latitude=-90,upper_latitude=90, lower_longitude=-1, upper_longitude=361, operational_comp=True):
    
    
    
    
    if lower_latitude>upper_latitude:
        
        theoretical=theoretical.where(np.logical_or(theoretical['latitude'] >= lower_latitude, theoretical['latitude'] <= upper_latitude), drop=True)
        HRES_truth=HRES_truth.where(np.logical_or(HRES_truth['latitude'] >= lower_latitude, HRES_truth['latitude'] <= upper_latitude), drop=True)
        nwp_det=nwp_det.where(np.logical_or(nwp_det['latitude'] >= lower_latitude, nwp_det['latitude'] <= upper_latitude), drop=True)
        AI_det_1=AI_det_1.where(np.logical_or(AI_det_1['latitude'] >= lower_latitude, AI_det_1['latitude'] <= upper_latitude), drop=True)
        AI_det_2=AI_det_2.where(np.logical_or(AI_det_2['latitude'] >= lower_latitude, AI_det_2['latitude'] <= upper_latitude), drop=True)
        if operational_comp==False:
            AI_det_3=AI_det_3.where(np.logical_or(AI_det_3['latitude'] >= lower_latitude, AI_det_3['latitude'] <= upper_latitude), drop=True)
        
    else:
    
        theoretical=theoretical.where(np.logical_and(theoretical['latitude'] >= lower_latitude, theoretical['latitude'] <= upper_latitude), drop=True)
        HRES_truth=HRES_truth.where(np.logical_and(HRES_truth['latitude'] >= lower_latitude, HRES_truth['latitude'] <= upper_latitude), drop=True)
        nwp_det=nwp_det.where(np.logical_and(nwp_det['latitude'] >= lower_latitude, nwp_det['latitude'] <= upper_latitude), drop=True)
        AI_det_1=AI_det_1.where(np.logical_and(AI_det_1['latitude'] >= lower_latitude, AI_det_1['latitude'] <= upper_latitude), drop=True)
        AI_det_2=AI_det_2.where(np.logical_and(AI_det_2['latitude'] >= lower_latitude, AI_det_2['latitude'] <= upper_latitude), drop=True)
        if operational_comp==False:
            AI_det_3=AI_det_3.where(np.logical_and(AI_det_3['latitude'] >= lower_latitude, AI_det_3['latitude'] <= upper_latitude), drop=True)
        
    if lower_longitude>upper_longitude:
        
        theoretical=theoretical.where(np.logical_or(theoretical['longitude'] >= lower_longitude, theoretical['longitude'] <= upper_longitude), drop=True)
        HRES_truth=HRES_truth.where(np.logical_or(HRES_truth['longitude'] >= lower_longitude, HRES_truth['longitude'] <= upper_longitude), drop=True)
        nwp_det=nwp_det.where(np.logical_or(nwp_det['longitude'] >= lower_longitude, nwp_det['longitude'] <= upper_longitude), drop=True)
        AI_det_1=AI_det_1.where(np.logical_or(AI_det_1['longitude'] >= lower_longitude, AI_det_1['longitude'] <= upper_longitude), drop=True)
        AI_det_2=AI_det_2.where(np.logical_or(AI_det_2['longitude'] >= lower_longitude, AI_det_2['longitude'] <= upper_longitude), drop=True)
        if operational_comp==False:
            AI_det_3=AI_det_3.where(np.logical_or(AI_det_3['longitude'] >= lower_longitude, AI_det_3['longitude'] <= upper_longitude), drop=True)
        
    else:
        theoretical=theoretical.where(np.logical_and(theoretical['longitude'] >= lower_longitude, theoretical['longitude'] <= upper_longitude), drop=True)
        HRES_truth=HRES_truth.where(np.logical_and(HRES_truth['longitude'] >= lower_longitude, HRES_truth['longitude'] <= upper_longitude), drop=True)
        nwp_det=nwp_det.where(np.logical_and(nwp_det['longitude'] >= lower_longitude, nwp_det['longitude'] <= upper_longitude), drop=True)
        AI_det_1=AI_det_1.where(np.logical_and(AI_det_1['longitude'] >= lower_longitude, AI_det_1['longitude'] <= upper_longitude), drop=True)
        AI_det_2=AI_det_2.where(np.logical_and(AI_det_2['longitude'] >= lower_longitude, AI_det_2['longitude'] <= upper_longitude), drop=True)
        if operational_comp==False:
            AI_det_3=AI_det_3.where(np.logical_and(AI_det_3['longitude'] >= lower_longitude, AI_det_3['longitude'] <= upper_longitude), drop=True)
        
            
    if operational_comp==False:
        
        return theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3
        
    else:
    
        return theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2



def write_data (dat, operational_comp=True):

    theoretical=dat[0].values.flatten()
    HRES_truth=dat[1].values.flatten()
    nwp_det=dat[2].values.flatten()
    AI_det_1=dat[3].values.flatten()
    AI_det_2=dat[4].values.flatten()
    if operational_comp==False:
        AI_det_3=dat[5].values.flatten()
        
    if operational_comp==False:
        return theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3
    else:
        return theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2

    

def prep_all (theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=None, days_ahead=5, operational_comp=True):
    

    
    
    deltatime=days_ahead-1
    operational_comp=operational_comp
    start_theoretical= datetime(2020, 1, 1+deltatime+1, 00, 00, 00)
    end_theoretical=datetime(2020, 12, 16+deltatime+1, 12, 00, 00)
    
    theoretical=theoretical.sel( time=slice(start_theoretical,end_theoretical))
    HRES_truth=HRES_truth.sel( time=slice(start_theoretical,end_theoretical))
    
    nwp_det = nwp_det.isel(prediction_timedelta = deltatime)
    AI_det_1 = AI_det_1.isel(prediction_timedelta = deltatime)
    AI_det_2 = AI_det_2.isel(prediction_timedelta = deltatime)
    if operational_comp==False:
        AI_det_3 = AI_det_3.isel(prediction_timedelta = deltatime)
    
    dat_NH_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=20,
                             upper_latitude=91)
    dat_mem_NH_oper=write_data(dat_NH_oper, operational_comp=operational_comp)
    
    dat_SH_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=-91,
                             upper_latitude=-20)
    dat_mem_SH_oper=write_data(dat_SH_oper, operational_comp=operational_comp)

    dat_tropics_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=-20,
                             upper_latitude=20)
    dat_mem_tropics_oper=write_data(dat_tropics_oper, operational_comp=operational_comp)

    dat_EXTRA_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=20,
                             upper_latitude=-20)
    dat_mem_EXTRA_oper=write_data(dat_EXTRA_oper, operational_comp=operational_comp)

    dat_ARC_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=60,
                             upper_latitude=91)
    dat_mem_ARC_oper=write_data(dat_ARC_oper, operational_comp=operational_comp)

    dat_ANT_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=-91,
                             upper_latitude=-60)
    dat_mem_ANT_oper=write_data(dat_ANT_oper, operational_comp=operational_comp)


    dat_EU_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=35,
                             upper_latitude=75,lower_longitude=347.5, upper_longitude=42.5)
    dat_mem_EU_oper=write_data(dat_EU_oper, operational_comp=operational_comp)

    dat_NAM_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=25,
                             upper_latitude=60,lower_longitude=240, upper_longitude=285)
    dat_mem_NAM_oper=write_data(dat_NAM_oper, operational_comp=operational_comp)

    dat_NAT_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=25,
                             upper_latitude=60,lower_longitude=290, upper_longitude=340)
    dat_mem_NAT_oper=write_data(dat_NAT_oper, operational_comp=operational_comp)

    dat_NAP_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=25,
                             upper_latitude=60,lower_longitude=310, upper_longitude=145)
    dat_mem_NAP_oper=write_data(dat_NAP_oper, operational_comp=operational_comp)

    dat_EA_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=25,
                             upper_latitude=60,lower_longitude=102.5, upper_longitude=150)
    dat_mem_EA_oper=write_data(dat_EA_oper, operational_comp=operational_comp)

    dat_ANZ_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp, lower_latitude=-45,
                             upper_latitude=-12.5,lower_longitude=120, upper_longitude=175)
    dat_mem_ANZ_oper=write_data(dat_ANZ_oper, operational_comp=operational_comp)


    dat_world_oper=prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=AI_det_3, operational_comp=operational_comp)
    dat_mem_world_oper=write_data(dat_world_oper, operational_comp=operational_comp)


    
    return (dat_NH_oper, dat_mem_NH_oper, dat_SH_oper, dat_mem_SH_oper, dat_tropics_oper, dat_mem_tropics_oper, dat_EXTRA_oper, dat_mem_EXTRA_oper,
            dat_ARC_oper, dat_mem_ARC_oper, dat_ANT_oper, dat_mem_ANT_oper, dat_EU_oper, dat_mem_EU_oper, dat_NAM_oper, dat_mem_NAM_oper,
            dat_NAT_oper, dat_mem_NAT_oper, dat_NAP_oper, dat_mem_NAP_oper, dat_EA_oper, dat_mem_EA_oper, dat_ANZ_oper, dat_mem_ANZ_oper, 
            dat_world_oper, dat_mem_world_oper)


    
    
#%% RMSE computation




def comp_RMSE_tail(dat, dat_mem, operational_comp, greater, HRES_ground,quant=None, no_hedging=False, robust=True, proper=False):
#quant defines the quantile-based threshold
#no_hedging=True when selecting extremes based on IFS HRES fporeacsts, otherwise always false
#robust=True for using clustered standard errors. Use False only if you need to debug/test out the function
#proper=True only for the use of consistens scores as in Appendix B. Otheriwse false.
#Remmber to change the options of the plot functions accordingly

    theoretical=dat_mem[0]
    if HRES_ground==True:
        HRES_truth=dat_mem[1]
    nwp_det=dat_mem[2]
    AI_det_1=dat_mem[3]
    AI_det_2=dat_mem[4]
    if operational_comp==False:
        AI_det_3=dat_mem[5]
    
    cos_weights=np.cos(np.deg2rad(dat[0].latitude))
    cos_weights=np.tile(cos_weights/np.mean(cos_weights), len(dat[0].time)*len(dat[0].longitude))
    
    if robust==True:
        lat=np.tile(dat[0].latitude, len(dat[0].longitude)*len(dat[0].time))
        lon=np.tile(np.repeat(dat[0].longitude, len(dat[0].latitude)),len(dat[0].time))
        time=np.repeat(dat[0].time, len(dat[0].latitude)*len(dat[0].longitude)).values

    if quant==None:
        
        variable_quant=theoretical
        HRES_variable_quant=nwp_det
        cos_weights_quant=cos_weights
        
        if HRES_ground==True:
             HRES_truth_variable_quant=HRES_truth
        
        if operational_comp==False:    
            pangu_variable_quant=AI_det_1
            fuxi_variable_quant=AI_det_2
            graphcast_variable_quant=AI_det_3
        
        else:
            pangu_variable_quant=AI_det_1
            graphcast_variable_quant=AI_det_2
        
    else:
        if no_hedging==True:
            
            if greater==True:
                 variable_quant=theoretical[nwp_det>np.quantile(nwp_det,quant)]
                 cos_weights_quant=cos_weights[nwp_det>np.quantile(nwp_det,quant)]
                 
                 if robust==True:
                     lat=lat[nwp_det>np.quantile(nwp_det,quant)]
                     lon=lon[nwp_det>np.quantile(nwp_det,quant)]
                     time=time[nwp_det>np.quantile(nwp_det,quant)]
                     
                 
                 if HRES_ground==True:
                      HRES_truth_variable_quant=HRES_truth[nwp_det>np.quantile(nwp_det,quant)]
        
                 HRES_variable_quant=nwp_det[nwp_det>np.quantile(nwp_det,quant)]
                 
                 if operational_comp==False:    
                     pangu_variable_quant=AI_det_1[nwp_det>np.quantile(nwp_det,quant)]
                     fuxi_variable_quant=AI_det_2[nwp_det>np.quantile(nwp_det,quant)]
                     graphcast_variable_quant=AI_det_3[nwp_det>np.quantile(nwp_det,quant)]
                 
                 else:
                     pangu_variable_quant=AI_det_1[nwp_det>np.quantile(nwp_det,quant)]
                     graphcast_variable_quant=AI_det_2[nwp_det>np.quantile(nwp_det,quant)]
        
            else:
                 variable_quant=theoretical[nwp_det<np.quantile(nwp_det,quant)]
                 cos_weights_quant=cos_weights[nwp_det<np.quantile(nwp_det,quant)]
                 
                 if robust==True:
                     lat=lat[nwp_det<np.quantile(nwp_det,quant)]
                     lon=lon[nwp_det<np.quantile(nwp_det,quant)]
                     time=time[nwp_det<np.quantile(nwp_det,quant)]
                 
        
                 if HRES_ground==True:
                      HRES_truth_variable_quant=HRES_truth[nwp_det<np.quantile(nwp_det,quant)]
        
                 HRES_variable_quant=nwp_det[nwp_det<np.quantile(nwp_det,quant)]
                 
                 if operational_comp==False: 
                     pangu_variable_quant=AI_det_1[nwp_det<np.quantile(nwp_det,quant)]
                     fuxi_variable_quant=AI_det_2[nwp_det<np.quantile(nwp_det,quant)]
                     graphcast_variable_quant=AI_det_3[nwp_det<np.quantile(nwp_det,quant)]
                 else:
                     pangu_variable_quant=AI_det_1[nwp_det<np.quantile(nwp_det,quant)]
                     graphcast_variable_quant=AI_det_2[nwp_det<np.quantile(nwp_det,quant)]
                     
        else:
            if greater==True:
                 variable_quant=theoretical[theoretical>np.quantile(theoretical,quant)]
                 cos_weights_quant=cos_weights[theoretical>np.quantile(theoretical,quant)]
                 
                 if robust==True:
                     lat=lat[theoretical>np.quantile(theoretical,quant)]
                     lon=lon[theoretical>np.quantile(theoretical,quant)]
                     time=time[theoretical>np.quantile(theoretical,quant)]
                     
                 
                 if HRES_ground==True:
                      HRES_truth_variable_quant=HRES_truth[theoretical>np.quantile(theoretical,quant)]
        
                 HRES_variable_quant=nwp_det[theoretical>np.quantile(theoretical,quant)]
                 
                 if operational_comp==False:    
                     pangu_variable_quant=AI_det_1[theoretical>np.quantile(theoretical,quant)]
                     fuxi_variable_quant=AI_det_2[theoretical>np.quantile(theoretical,quant)]
                     graphcast_variable_quant=AI_det_3[theoretical>np.quantile(theoretical,quant)]
                 
                 else:
                     pangu_variable_quant=AI_det_1[theoretical>np.quantile(theoretical,quant)]
                     graphcast_variable_quant=AI_det_2[theoretical>np.quantile(theoretical,quant)]
        
            else:
                 variable_quant=theoretical[theoretical<np.quantile(theoretical,quant)]
                 cos_weights_quant=cos_weights[theoretical<np.quantile(theoretical,quant)]
                 
                 if robust==True:
                     lat=lat[theoretical<np.quantile(theoretical,quant)]
                     lon=lon[theoretical<np.quantile(theoretical,quant)]
                     time=time[theoretical<np.quantile(theoretical,quant)]
                 
        
                 if HRES_ground==True:
                      HRES_truth_variable_quant=HRES_truth[theoretical<np.quantile(theoretical,quant)]
        
                 HRES_variable_quant=nwp_det[theoretical<np.quantile(theoretical,quant)]
                 
                 if operational_comp==False: 
                     pangu_variable_quant=AI_det_1[theoretical<np.quantile(theoretical,quant)]
                     fuxi_variable_quant=AI_det_2[theoretical<np.quantile(theoretical,quant)]
                     graphcast_variable_quant=AI_det_3[theoretical<np.quantile(theoretical,quant)]
                 else:
                     pangu_variable_quant=AI_det_1[theoretical<np.quantile(theoretical,quant)]
                     graphcast_variable_quant=AI_det_2[theoretical<np.quantile(theoretical,quant)]
                     
    if operational_comp==False:
        
        
        if HRES_ground==True:
            
            sq_err_HRES=(HRES_variable_quant-HRES_truth_variable_quant)**2
            
            RMSE_tail_HRES=(sum(cos_weights_quant*(HRES_variable_quant-HRES_truth_variable_quant)**2)/len(variable_quant))**(1/2)
        else:

            sq_err_HRES=(HRES_variable_quant-variable_quant)**2
            
            RMSE_tail_HRES=(sum(cos_weights_quant*(HRES_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
            

        sq_err_pangu=(pangu_variable_quant-variable_quant)**2
        sq_err_graphcast=(graphcast_variable_quant-variable_quant)**2
        sq_err_fuxi=(fuxi_variable_quant-variable_quant)**2 
            
        RMSE_tail_pangu=(sum(cos_weights_quant*(pangu_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
        RMSE_tail_graphcast=(sum(cos_weights_quant*(graphcast_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
        RMSE_tail_fuxi=(sum(cos_weights_quant*(fuxi_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
        
         
        # Significance test vs HRES


        diff_pangu=sq_err_pangu-sq_err_HRES
        diff_graphcast=sq_err_graphcast-sq_err_HRES
        diff_fuxi=sq_err_fuxi-sq_err_HRES
        
            
        dat_pangu = pd.DataFrame({
        'Latitude': lat,
        'Longitude': lon,
        'Time':time,
        'Predicted': diff_pangu
        })
        
        dat_pangu['Latlon']=round(dat_pangu['Latitude'],2).astype(str)+round(dat_pangu['Longitude'],2).astype(str)
        
        #dat_pangu=pd.get_dummies(dat_pangu, columns=['Model'])

        model_cluster_pangu = lm.PanelOLS.from_formula(
          formula=("Predicted ~ 1"),
          data=dat_pangu.set_index(["Latlon", "Time"]),
        ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)


        test_st_pangu=model_cluster_pangu.tstats[0]
        
        
        del dat_pangu, model_cluster_pangu
        
        
        dat_graphcast = pd.DataFrame({
        'Latitude': lat,
        'Longitude': lon,
        'Time':time,
        'Predicted': diff_graphcast
        })
        
        dat_graphcast['Latlon']=round(dat_graphcast['Latitude'],2).astype(str)+round(dat_graphcast['Longitude'],2).astype(str)

        model_cluster_graphcast = lm.PanelOLS.from_formula(
          formula=("Predicted ~ 1"),
          data=dat_graphcast.set_index(["Latlon", "Time"]),
        ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)


        test_st_graphcast=model_cluster_graphcast.tstats[0]
        
        del dat_graphcast, model_cluster_graphcast
        
        
        dat_fuxi = pd.DataFrame({
        'Latitude': lat,
        'Longitude': lon,
        'Time':time,
        'Predicted': diff_fuxi
        })
        
        dat_fuxi['Latlon']=round(dat_fuxi['Latitude'],2).astype(str)+round(dat_fuxi['Longitude'],2).astype(str)

        model_cluster_fuxi = lm.PanelOLS.from_formula(
          formula=("Predicted ~ 1"),
          data=dat_fuxi.set_index(["Latlon", "Time"]),
        ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)


        test_st_fuxi=model_cluster_fuxi.tstats[0]
        
        del dat_fuxi, model_cluster_fuxi
            
                
        threshold_low=stats.t(df=len(variable_quant)).ppf((0.025))
        threshold_high=stats.t(df=len(variable_quant)).ppf((0.975))
        
        significant_pangu= np.where((test_st_pangu > threshold_high) | (test_st_pangu < threshold_low),1,0)
        significant_graphcast= np.where((test_st_graphcast > threshold_high) | (test_st_graphcast < threshold_low),1,0)
        significant_fuxi= np.where((test_st_fuxi > threshold_high) | (test_st_fuxi < threshold_low),1,0)
        

        
        #Best model significance test
        
        
        threshold_low_one=stats.t(df=len(variable_quant)).ppf((0.05))

        
        if ((RMSE_tail_pangu<RMSE_tail_HRES) and (RMSE_tail_pangu<RMSE_tail_graphcast) and (RMSE_tail_pangu<RMSE_tail_fuxi) ):
            
            if ((RMSE_tail_graphcast<RMSE_tail_HRES) and (RMSE_tail_graphcast<RMSE_tail_fuxi)):
            
                diff_pangu_graphcast=sq_err_pangu-sq_err_graphcast
                
                dat_pangu_graphcast = pd.DataFrame({
                'Latitude': lat,
                'Longitude': lon,
                'Time': time,
                'Predicted': diff_pangu_graphcast
                })
                
                dat_pangu_graphcast['Latlon']=round(dat_pangu_graphcast['Latitude'],2).astype(str)+round(dat_pangu_graphcast['Longitude'],2).astype(str)

                model_cluster_pangu_graphcast = lm.PanelOLS.from_formula(
                  formula=("Predicted ~ 1"),
                  data=dat_pangu_graphcast.set_index(["Latlon", "Time"]),
                ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)

                test_st_pangu_graphcast=model_cluster_pangu_graphcast.tstats[0]
                
                del dat_pangu_graphcast, model_cluster_pangu_graphcast

                significant_best=np.where((test_st_pangu_graphcast < threshold_low_one),1,0)
                
            elif ((RMSE_tail_fuxi<RMSE_tail_HRES) and (RMSE_tail_fuxi<RMSE_tail_graphcast)):
            
                diff_pangu_fuxi=sq_err_pangu-sq_err_fuxi
                
                dat_pangu_fuxi = pd.DataFrame({
                'Latitude': lat,
                'Longitude': lon,
                'Time': time,
                'Predicted': diff_pangu_fuxi
                })
                
                dat_pangu_fuxi['Latlon']=round(dat_pangu_fuxi['Latitude'],2).astype(str)+round(dat_pangu_fuxi['Longitude'],2).astype(str)
                

                model_cluster_pangu_fuxi = lm.PanelOLS.from_formula(
                  formula=("Predicted ~ 1"),
                  data=dat_pangu_fuxi.set_index(["Latlon", "Time"]),
                ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)

                test_st_pangu_fuxi=model_cluster_pangu_fuxi.tstats[0]
                
                del dat_pangu_fuxi, model_cluster_pangu_fuxi
                
                significant_best=np.where((test_st_pangu_fuxi < threshold_low_one),1,0)
                
            else:
                    
                significant_best=np.where((test_st_pangu < threshold_low_one),1,0)
                
        elif ((RMSE_tail_graphcast<RMSE_tail_HRES) and (RMSE_tail_graphcast<RMSE_tail_pangu) and (RMSE_tail_graphcast<RMSE_tail_fuxi)):
            
            if ((RMSE_tail_pangu<RMSE_tail_HRES) and (RMSE_tail_pangu<RMSE_tail_fuxi)):
            
                diff_graphcast_pangu=sq_err_graphcast-sq_err_pangu
                
                dat_graphcast_pangu = pd.DataFrame({
                'Latitude': lat,
                'Longitude': lon,
                'Time': time,
                'Predicted': diff_graphcast_pangu
                })
                
                dat_graphcast_pangu['Latlon']=round(dat_graphcast_pangu['Latitude'],2).astype(str)+round(dat_graphcast_pangu['Longitude'],2).astype(str)
                

                model_cluster_graphcast_pangu = lm.PanelOLS.from_formula(
                  formula=("Predicted ~ 1"),
                  data=dat_graphcast_pangu.set_index(["Latlon", "Time"]),
                ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)

                test_st_graphcast_pangu=model_cluster_graphcast_pangu.tstats[0]
                
                del dat_graphcast_pangu, model_cluster_graphcast_pangu
                
                significant_best=np.where((test_st_graphcast_pangu < threshold_low_one),1,0)
                
            elif ((RMSE_tail_fuxi<RMSE_tail_HRES) and (RMSE_tail_fuxi<RMSE_tail_pangu)):
                
                diff_graphcast_fuxi=sq_err_graphcast-sq_err_fuxi
                
                dat_graphcast_fuxi = pd.DataFrame({
                'Latitude': lat,
                'Longitude': lon,
                'Time': time,
                'Predicted': diff_graphcast_fuxi
                })
                
                dat_graphcast_fuxi['Latlon']=round(dat_graphcast_fuxi['Latitude'],2).astype(str)+round(dat_graphcast_fuxi['Longitude'],2).astype(str)

                model_cluster_graphcast_fuxi = lm.PanelOLS.from_formula(
                  formula=("Predicted ~ 1"),
                  data=dat_graphcast_fuxi.set_index(["Latlon", "Time"]),
                ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)

                test_st_graphcast_fuxi=model_cluster_graphcast_fuxi.tstats[0]
                
                del dat_graphcast_fuxi, model_cluster_graphcast_fuxi
                
                significant_best=np.where((test_st_graphcast_fuxi < threshold_low_one),1,0)
                
            else:
                    
                significant_best=np.where((test_st_graphcast < threshold_low_one),1,0)
                
                
        elif ((RMSE_tail_fuxi<RMSE_tail_HRES) and (RMSE_tail_fuxi<RMSE_tail_pangu) and (RMSE_tail_fuxi<RMSE_tail_graphcast)):
            
            if ((RMSE_tail_pangu<RMSE_tail_HRES) and (RMSE_tail_pangu<RMSE_tail_graphcast)):
            
                diff_fuxi_pangu=sq_err_fuxi-sq_err_pangu
                
                dat_fuxi_pangu = pd.DataFrame({
                'Latitude': lat,
                'Longitude': lon,
                'Time': time,
                'Predicted': diff_fuxi_pangu
                })
                
                dat_fuxi_pangu['Latlon']=round(dat_fuxi_pangu['Latitude'],2).astype(str)+round(dat_fuxi_pangu['Longitude'],2).astype(str)

                model_cluster_fuxi_pangu = lm.PanelOLS.from_formula(
                  formula=("Predicted ~ 1"),
                  data=dat_fuxi_pangu.set_index(["Latlon", "Time"]),
                ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)

                test_st_fuxi_pangu=model_cluster_fuxi_pangu.tstats[0]
                
                del dat_fuxi_pangu, model_cluster_fuxi_pangu
                
                significant_best=np.where((test_st_fuxi_pangu < threshold_low_one),1,0)
                
            elif ((RMSE_tail_graphcast<RMSE_tail_HRES) and (RMSE_tail_graphcast<RMSE_tail_pangu)):
                
                diff_fuxi_graphcast=sq_err_fuxi-sq_err_graphcast
                
                dat_fuxi_graphcast = pd.DataFrame({
                'Latitude': lat,
                'Longitude': lon,
                'Time': time,
                'Predicted': diff_fuxi_graphcast
                })
                
                dat_fuxi_graphcast['Latlon']=round(dat_fuxi_graphcast['Latitude'],2).astype(str)+round(dat_fuxi_graphcast['Longitude'],2).astype(str)

                model_cluster_fuxi_graphcast = lm.PanelOLS.from_formula(
                  formula=("Predicted ~ 1"),
                  data=dat_fuxi_graphcast.set_index(["Latlon", "Time"]),
                ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)

                test_st_fuxi_graphcast=model_cluster_fuxi_graphcast.tstats[0]
                
                del dat_fuxi_graphcast, model_cluster_fuxi_graphcast
                
                significant_best=np.where((test_st_fuxi_graphcast < threshold_low_one),1,0)
                
            else:
                    
                significant_best=np.where((test_st_fuxi < threshold_low_one),1,0)
                
            
        else: 
            
            if ((RMSE_tail_pangu<RMSE_tail_graphcast) and (RMSE_tail_pangu<RMSE_tail_fuxi)) : 
                
                significant_best=np.where(((-test_st_pangu) < threshold_low_one),1,0)
                
            elif ((RMSE_tail_graphcast <RMSE_tail_pangu) and (RMSE_tail_graphcast<RMSE_tail_fuxi)):
                
                significant_best=np.where(((-test_st_graphcast) < threshold_low_one),1,0)
                
            else:
                significant_best=np.where(((-test_st_fuxi) < threshold_low_one),1,0)
                
        

        return RMSE_tail_HRES, RMSE_tail_pangu, RMSE_tail_fuxi, RMSE_tail_graphcast, significant_pangu, significant_fuxi, significant_graphcast, significant_best
        
    else:

        if HRES_ground==True:
            
            sq_err_HRES=(HRES_variable_quant-HRES_truth_variable_quant)**2
            sq_err_pangu=(pangu_variable_quant-HRES_truth_variable_quant)**2
            sq_err_graphcast=(graphcast_variable_quant-HRES_truth_variable_quant)**2
            
            RMSE_tail_HRES=(sum(cos_weights_quant*(HRES_variable_quant-HRES_truth_variable_quant)**2)/len(variable_quant))**(1/2)
            RMSE_tail_pangu=(sum(cos_weights_quant*(pangu_variable_quant-HRES_truth_variable_quant)**2)/len(variable_quant))**(1/2)
            RMSE_tail_graphcast=(sum(cos_weights_quant*(graphcast_variable_quant-HRES_truth_variable_quant)**2)/len(variable_quant))**(1/2)
            
        else:
            
            sq_err_HRES=(HRES_variable_quant-variable_quant)**2
            sq_err_pangu=(pangu_variable_quant-variable_quant)**2
            sq_err_graphcast=(graphcast_variable_quant-variable_quant)**2
            
            RMSE_tail_HRES=(sum(cos_weights_quant*(HRES_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
            RMSE_tail_pangu=(sum(cos_weights_quant*(pangu_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
            RMSE_tail_graphcast=(sum(cos_weights_quant*(graphcast_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
            
            if proper==True:
                
                a_cut=np.quantile(theoretical,quant)
                first_term=sum(cos_weights[theoretical>a_cut]*(theoretical[theoretical>a_cut]-a_cut)**2)/len(theoretical)
                
                second_term_HRES=sum(cos_weights[nwp_det>a_cut]*(nwp_det[nwp_det>a_cut]-a_cut)**2)/len(theoretical)
                third_term_HRES=sum(2*cos_weights[nwp_det>a_cut]*(theoretical[nwp_det>a_cut]-nwp_det[nwp_det>a_cut])*(nwp_det[nwp_det>a_cut]-a_cut))/len(theoretical)
                
                second_term_pangu=sum(cos_weights[AI_det_1>a_cut]*(AI_det_1[AI_det_1>a_cut]-a_cut)**2)/len(theoretical)
                third_term_pangu=sum(2*cos_weights[AI_det_1>a_cut]*(theoretical[AI_det_1>a_cut]-AI_det_1[AI_det_1>a_cut])*(AI_det_1[AI_det_1>a_cut]-a_cut))/len(theoretical)
                
                second_term_graphcast=sum(cos_weights[AI_det_2>a_cut]*(AI_det_2[AI_det_2>a_cut]-a_cut)**2)/len(theoretical)
                third_term_graphcast=sum(2*cos_weights[AI_det_2>a_cut]*(theoretical[AI_det_2>a_cut]-AI_det_2[AI_det_2>a_cut])*(AI_det_2[AI_det_2>a_cut]-a_cut))/len(theoretical)
                
                S2_HRES=(first_term-second_term_HRES-third_term_HRES)
                S2_pangu=(first_term-second_term_pangu-third_term_pangu)
                S2_graphcast=(first_term-second_term_graphcast-third_term_graphcast)
                
                MSE_HRES=sum(cos_weights*(nwp_det-theoretical)**2)/len(theoretical)
                MSE_pangu=sum(cos_weights*(AI_det_1-theoretical)**2)/len(theoretical)
                MSE_graphcast=sum(cos_weights*(AI_det_2-theoretical)**2)/len(theoretical)
                
                S1_HRES=MSE_HRES-S2_HRES
                S1_pangu=MSE_pangu-S2_pangu
                S1_graphcast=MSE_graphcast-S2_graphcast
                
                if greater==True:
                
                    return S2_HRES, S2_pangu, S2_graphcast
                
                else:
                    return S1_HRES, S1_pangu, S1_graphcast
                
                
                if greater==True:
                     variable_quant=theoretical[theoretical>np.quantile(theoretical,quant)]
                     cos_weights_quant=cos_weights[theoretical>np.quantile(theoretical,quant)]
                     
                     if robust==True:
                         lat=lat[theoretical>np.quantile(theoretical,quant)]
                         lon=lon[theoretical>np.quantile(theoretical,quant)]
                         time=time[theoretical>np.quantile(theoretical,quant)]
                         
                     
                     if HRES_ground==True:
                          HRES_truth_variable_quant=HRES_truth[theoretical>np.quantile(theoretical,quant)]
            
                     HRES_variable_quant=nwp_det[theoretical>np.quantile(theoretical,quant)]
                     
                     if operational_comp==False:    
                         pangu_variable_quant=AI_det_1[theoretical>np.quantile(theoretical,quant)]
                         fuxi_variable_quant=AI_det_2[theoretical>np.quantile(theoretical,quant)]
                         graphcast_variable_quant=AI_det_3[theoretical>np.quantile(theoretical,quant)]
                     
                     else:
                         pangu_variable_quant=AI_det_1[theoretical>np.quantile(theoretical,quant)]
                         graphcast_variable_quant=AI_det_2[theoretical>np.quantile(theoretical,quant)]
            
                else:
                     variable_quant=theoretical[theoretical<np.quantile(theoretical,quant)]
                     cos_weights_quant=cos_weights[theoretical<np.quantile(theoretical,quant)]
                     
                     if robust==True:
                         lat=lat[theoretical<np.quantile(theoretical,quant)]
                         lon=lon[theoretical<np.quantile(theoretical,quant)]
                         time=time[theoretical<np.quantile(theoretical,quant)]
                     
            
                     if HRES_ground==True:
                          HRES_truth_variable_quant=HRES_truth[theoretical<np.quantile(theoretical,quant)]
            
                     HRES_variable_quant=nwp_det[theoretical<np.quantile(theoretical,quant)]
                     
                     if operational_comp==False: 
                         pangu_variable_quant=AI_det_1[theoretical<np.quantile(theoretical,quant)]
                         fuxi_variable_quant=AI_det_2[theoretical<np.quantile(theoretical,quant)]
                         graphcast_variable_quant=AI_det_3[theoretical<np.quantile(theoretical,quant)]
                     else:
                         pangu_variable_quant=AI_det_1[theoretical<np.quantile(theoretical,quant)]
                         graphcast_variable_quant=AI_det_2[theoretical<np.quantile(theoretical,quant)]
                
                
        # Significance test vs HRES

        diff_pangu=sq_err_pangu-sq_err_HRES
        diff_graphcast=sq_err_graphcast-sq_err_HRES
        
        if robust == False:
        
            var_cos_diff_pangu=(sum(cos_weights_quant*(diff_pangu-np.mean(diff_pangu))**2))/(len(diff_pangu)-1)
            var_cos_diff_graphcast=(sum(cos_weights_quant*(diff_graphcast-np.mean(diff_graphcast))**2))/(len(diff_graphcast)-1)
            
            mean_cos_diff_pangu=np.mean(cos_weights_quant*diff_pangu)
            mean_cos_diff_graphcast=np.mean(cos_weights_quant*diff_graphcast)
            
            test_st_pangu=(mean_cos_diff_pangu*len(diff_pangu)**(1/2))/(var_cos_diff_pangu)**(1/2)
            test_st_graphcast=(mean_cos_diff_graphcast*len(diff_graphcast)**(1/2))/(var_cos_diff_graphcast)**(1/2)
            
        else:
            
            dat_pangu = pd.DataFrame({
            'Latitude': lat,
            'Longitude': lon,
            'Time':time,
            'Predicted': diff_pangu
            })
            
            dat_pangu['Latlon']=round(dat_pangu['Latitude'],2).astype(str)+round(dat_pangu['Longitude'],2).astype(str)

            model_cluster_pangu = lm.PanelOLS.from_formula(
              formula=("Predicted ~ 1"),
              data=dat_pangu.set_index(["Latlon", "Time"]),
            ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)


            test_st_pangu=model_cluster_pangu.tstats[0]
            
            
            del dat_pangu, model_cluster_pangu
            
            
            dat_graphcast = pd.DataFrame({
            'Latitude': lat,
            'Longitude': lon,
            'Time':time,
            'Predicted': diff_graphcast
            })
            
            dat_graphcast['Latlon']=round(dat_graphcast['Latitude'],2).astype(str)+round(dat_graphcast['Longitude'],2).astype(str)

            model_cluster_graphcast = lm.PanelOLS.from_formula(
              formula=("Predicted ~ 1"),
              data=dat_graphcast.set_index(["Latlon", "Time"]),
            ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)


            test_st_graphcast=model_cluster_graphcast.tstats[0]
            
            del dat_graphcast, model_cluster_graphcast
            
                
        threshold_low=stats.t(df=len(variable_quant)).ppf((0.025))
        threshold_high=stats.t(df=len(variable_quant)).ppf((0.975))
        
        significant_pangu= np.where((test_st_pangu > threshold_high) | (test_st_pangu < threshold_low),1,0)
        significant_graphcast= np.where((test_st_graphcast > threshold_high) | (test_st_graphcast < threshold_low),1,0)
        
        # Best model significance test
        
        threshold_low_one=stats.t(df=len(variable_quant)).ppf((0.05))
        
        if ((RMSE_tail_pangu<RMSE_tail_HRES) and (RMSE_tail_pangu<RMSE_tail_graphcast)):
            
            if (RMSE_tail_graphcast<RMSE_tail_HRES):
                
                diff_pangu_graphcast=sq_err_pangu-sq_err_graphcast
            
                if robust==False:
                    
                    var_cos_diff_pangu_graphcast=(sum(cos_weights_quant*(diff_pangu_graphcast-np.mean(diff_pangu_graphcast))**2))/(len(diff_pangu_graphcast)-1)
                    
                    mean_cos_diff_pangu_graphcast=np.mean(cos_weights_quant*diff_pangu_graphcast)
                    
                    test_st_pangu_graphcast=(mean_cos_diff_pangu_graphcast*len(diff_pangu_graphcast)**(1/2))/(var_cos_diff_pangu_graphcast)**(1/2)
                    
                else: 
                     
                        dat_pangu_graphcast = pd.DataFrame({
                        'Latitude': lat,
                        'Longitude': lon,
                        'Time': time,
                        'Predicted': diff_pangu_graphcast
                        })
                        
                        dat_pangu_graphcast['Latlon']=round(dat_pangu_graphcast['Latitude'],2).astype(str)+round(dat_pangu_graphcast['Longitude'],2).astype(str)

                        model_cluster_pangu_graphcast = lm.PanelOLS.from_formula(
                          formula=("Predicted ~ 1"),
                          data=dat_pangu_graphcast.set_index(["Latlon", "Time"]),
                        ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)

                        test_st_pangu_graphcast=model_cluster_pangu_graphcast.tstats[0]
                        
                        del dat_pangu_graphcast, model_cluster_pangu_graphcast

                significant_best=np.where((test_st_pangu_graphcast < threshold_low_one),1,0)
                
            else:
                significant_best=np.where((test_st_pangu < threshold_low_one),1,0)
                
        elif ((RMSE_tail_graphcast<RMSE_tail_HRES) and (RMSE_tail_graphcast<RMSE_tail_pangu)):
            
            if (RMSE_tail_pangu<RMSE_tail_HRES):
                
                diff_graphcast_pangu=sq_err_graphcast-sq_err_pangu
                
                if robust==False:
                    
                    var_cos_diff_graphcast_pangu=(sum(cos_weights_quant*(diff_graphcast_pangu-np.mean(diff_graphcast_pangu))**2))/(len(diff_graphcast_pangu)-1)
                    
                    mean_cos_diff_graphcast_pangu=np.mean(cos_weights_quant*diff_graphcast_pangu)
                    
                    test_st_graphcast_pangu=(mean_cos_diff_graphcast_pangu*len(diff_graphcast_pangu)**(1/2))/(var_cos_diff_graphcast_pangu)**(1/2)

                else: 
                     
                        dat_graphcast_pangu = pd.DataFrame({
                        'Latitude': lat,
                        'Longitude': lon,
                        'Time': time,
                        'Predicted': diff_graphcast_pangu
                        })
                        
                        dat_graphcast_pangu['Latlon']=round(dat_graphcast_pangu['Latitude'],2).astype(str)+round(dat_graphcast_pangu['Longitude'],2).astype(str)

                        model_cluster_graphcast_pangu = lm.PanelOLS.from_formula(
                          formula=("Predicted ~ 1"),
                          data=dat_graphcast_pangu.set_index(["Latlon", "Time"]),
                        ).fit(cov_type="clustered", cluster_entity=True, cluster_time=True)

                        test_st_graphcast_pangu=model_cluster_graphcast_pangu.tstats[0]
                        
                        del dat_graphcast_pangu, model_cluster_graphcast_pangu
                
                significant_best=np.where((test_st_graphcast_pangu < threshold_low_one),1,0)
                
            else:
                    
                significant_best=np.where((test_st_graphcast < threshold_low_one),1,0)
                
        else: 
            
            if (RMSE_tail_pangu<RMSE_tail_graphcast): 
                
                significant_best=np.where(((-test_st_pangu) < threshold_low_one),1,0)
                
            else:
                
                significant_best=np.where(((-test_st_graphcast) < threshold_low_one),1,0)
                    

        return RMSE_tail_HRES, RMSE_tail_pangu, RMSE_tail_graphcast, significant_pangu, significant_graphcast, significant_best
    


def RMSE_all(dat_tot, greater=True, HRES_ground=False, operational_comp=True, no_hedging=False, quant=None, proper=False):
    
    
    
    RMSE_NH=comp_RMSE_tail(dat_tot[0], dat_tot[1], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    RMSE_SH=comp_RMSE_tail(dat_tot[2], dat_tot[3], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    RMSE_tropics=comp_RMSE_tail(dat_tot[4], dat_tot[5], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    RMSE_EXTRA=comp_RMSE_tail(dat_tot[6], dat_tot[7], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    RMSE_ARC=comp_RMSE_tail(dat_tot[8], dat_tot[9], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    RMSE_ANT=comp_RMSE_tail(dat_tot[10], dat_tot[11], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    
    
    RMSE_EU=comp_RMSE_tail(dat_tot[12], dat_tot[13], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    RMSE_NAM=comp_RMSE_tail(dat_tot[14], dat_tot[15], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    RMSE_NAT=comp_RMSE_tail(dat_tot[16], dat_tot[17], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    RMSE_NAP=comp_RMSE_tail(dat_tot[18], dat_tot[19], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    RMSE_EA=comp_RMSE_tail(dat_tot[20], dat_tot[21], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    RMSE_ANZ=comp_RMSE_tail(dat_tot[22], dat_tot[23], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    
    RMSE=comp_RMSE_tail(dat_tot[24], dat_tot[25], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant, no_hedging=no_hedging, proper=proper)
    
    RMSE=np.array([RMSE_NH, RMSE_SH,RMSE_tropics,RMSE_EXTRA,RMSE_ARC,RMSE_ANT,
                RMSE_EU,RMSE_NAM,RMSE_NAT,RMSE_NAP,RMSE_EA,RMSE_ANZ, RMSE])
    
    if operational_comp==True:
        
        if proper==False:
    
            RMSE= pd.DataFrame(RMSE, columns=['HRES', 'Pangu','Graphcast', 's Pangu', 's Graphcast', 's Best'], index=['Northern Hemisphere', 'Southern Hemisphere', 'Tropics', 'Extra-Tropics', 'Arctic', 'Antarctic', 
                                                                              'Europe', 'North America', 'North Atlantic', 'North Pacific', 'East Asia', 'AusNZ', 'Global'])
        else:
            
            RMSE= pd.DataFrame(RMSE, columns=['HRES', 'Pangu','Graphcast'], index=['Northern Hemisphere', 'Southern Hemisphere', 'Tropics', 'Extra-Tropics', 'Arctic', 'Antarctic', 
                                                                                  'Europe', 'North America', 'North Atlantic', 'North Pacific', 'East Asia', 'AusNZ', 'Global'])
            
    else:
        RMSE= pd.DataFrame(RMSE, columns=['HRES', 'Pangu','Fuxi','Graphcast', 's Pangu', 's Fuxi', 's Graphcast', 's Best'], index=['Northern Hemisphere', 'Southern Hemisphere', 'Tropics', 'Extra-Tropics', 'Arctic', 'Antarctic', 
                                                                                  'Europe', 'North America', 'North Atlantic', 'North Pacific', 'East Asia', 'AusNZ', 'Global'])
        
    return(RMSE)

#%% Plots


def plot_tile_depth (var_1, var_3, var_5, var_7, var_10, region, operational_comp=True, text_size_table=30, text_size_axis=28, abbreviation=True, robust=True):
    #Operational_comp=True when evaluatingsemi-/pre-operational models, False for comparison of reanalysis models
    
    if abbreviation==True:
       d = {'1 d': (var_1.loc[region]).values.squeeze(), '3 d': (var_3.loc[region]).values.squeeze() , '5 d': (var_5.loc[region]).values.squeeze(),
             '7 d': (var_7.loc[region]).values.squeeze(), '10 d': (var_10.loc[region]).values.squeeze()}
    else:
           
       d = {'1 day': (var_1.loc[region]).values.squeeze(), '3 days': (var_3.loc[region]).values.squeeze() , '5 days': (var_5.loc[region]).values.squeeze(),
         '7 days': (var_7.loc[region]).values.squeeze(), '10 days': (var_10.loc[region]).values.squeeze()}
       
    df = pd.DataFrame(data=d)
    
    
    if robust==True:
    
        df.loc[len(df)] = 0
    
        df_1=df[:round(len(df)/2)]
    
        df_zeros=pd.DataFrame(df.loc[len(df)-1])

        df_2=pd.concat([df_zeros.T,df.iloc[round(len(df)/2):round(len(df)-1),:]])

        if operational_comp==True:
            df_1.index = ['HRES', 'Pangu', 'Graphcast']
            df_2.index = ['HRES', 'Pangu', 'Graphcast' ]
        else:
            df_1.index = ['HRES', 'Pangu', 'Fuxi','Graphcast']
            df_2.index = ['HRES', 'Pangu', 'Fuxi','Graphcast' ]
    
        diff=(df_1-(df_1[0:1].values.squeeze()))/(df_1[0:1].values.squeeze())*100
        
        diff=diff.melt()
        
        df_1=((df_1.reset_index()).melt(id_vars='index'))
        df_2=((df_2.reset_index()).melt(id_vars='index'))
        
        df=pd.concat([df_1,df_2],axis=1)
        
        df_1=df_1.rename(columns={"index":"Model", "variable":"Days", "value":"RMSE"})
        
        df=df_1
        
        df['Difference']=diff['value']
        df['Significance']=(round(df_2['value']).astype('category'))
        
        del(df_1,df_2,df_zeros)
    
    else:
        
        if operational_comp==True:
            df.index = ['HRES', 'Pangu', 'Graphcast']
            
            diff=(df-(df[0:1].values.squeeze()))/(df[0:1].values.squeeze())*100
            
            diff=diff.melt()
            
            df=((df.reset_index()).melt(id_vars='index'))
            
            df=df.rename(columns={"index":"Model", "variable":"Days", "value":"RMSE"})
            
            
            df['Difference']=diff['value']
            
        else:
            df.index = ['HRES', 'Pangu', 'Fuxi','Graphcast']
            
    df['RMSE']=round(df['RMSE'], ndigits=2)
    
    
    if (operational_comp==True):
        df['Model']=(df['Model'].astype('category')).cat.reorder_categories(['Pangu', 'Graphcast', 'HRES'])
    else: 
        df['Model']=(df['Model'].astype('category')).cat.reorder_categories(['Fuxi','Pangu', 'Graphcast', 'HRES'])
        
    if abbreviation==True:
        df['Days']=(df['Days'].astype('category')).cat.reorder_categories(['1 d', '3 d', '5 d' , '7 d', '10 d'])
    else:
        df['Days']=(df['Days'].astype('category')).cat.reorder_categories(['1 day', '3 days', '5 days' , '7 days', '10 days'])
    
    if robust==True:
        pl=ggplot(df)+\
            geom_tile(aes(x='Days',y='Model', fill='Difference', color= 'Significance',width=0.9, height=0.9),size=4)+\
            scale_color_manual(values=["white","black"], guide=False)+\
            geom_text(aes(x='Days',y='Model',label='RMSE'), color='black', size=text_size_table)+\
            scale_fill_gradientn(colors=["#0B559F","#2B7BBA","#539ECD","#89BEDC", "#BAD6EB", "#DBE9F6", "#FFFFFF", "#FEDBCC", "#FCAF93", "#FC8161", "#F14E38", "#BD1E1D", "#A91016"],
                                 values=[0, 0.25,0.4167,0.4583,0.483,0.4916,0.50,0.5087,0.5117,0.5417,0.5833,0.75,1], breaks=[-60,-30, -10, 0, 10, 30, 60], limits=[-60,60], 
                                 name="% difference in RMSE vs IFS HRES"
        )+\
            theme_minimal()+\
            theme(plot_background=element_rect(fill='white'),
                  text=element_text(family='Verdana', color= 'black'),
                  axis_text=element_text(size=text_size_axis),
                  axis_title=element_text(size=32, face='bold'),
                  title=element_text(size=44, face='bold', hjust=0),
                  legend_title=element_text(size=34, face='bold'),
                  legend_text=element_text(size=28),
                  legend_key_width=20,
                  legend_key_height=150,
                  legend_position='bottom')
            
    else:
        
        pl=ggplot(df)+\
            geom_tile(aes(x='Days',y='Model', fill='Difference',width=0.9, height=0.9),size=4,color='white')+\
            geom_text(aes(x='Days',y='Model',label='RMSE'), color='black', size=text_size_table)+\
            scale_fill_gradientn(colors=["#0B559F","#2B7BBA","#539ECD","#89BEDC", "#BAD6EB", "#DBE9F6", "#FFFFFF", "#FEDBCC", "#FCAF93", "#FC8161", "#F14E38", "#BD1E1D", "#A91016"],
                                 values=[0, 0.25,0.4167,0.4583,0.483,0.4916,0.50,0.5087,0.5117,0.5417,0.5833,0.75,1], breaks=[-60,-30, -10, 0, 10, 30, 60], limits=[-60,60], 
                                 name="% difference vs IFS HRES"
        )+\
            theme_minimal()+\
            theme(plot_background=element_rect(fill='white'),
                  text=element_text(family='Verdana', color= 'black'),
                  axis_text=element_text(size=text_size_axis),
                  axis_title=element_text(size=32, face='bold'),
                  title=element_text(size=44, face='bold', hjust=0),
                  legend_title=element_text(size=34, face='bold'),
                  legend_text=element_text(size=28),
                  legend_key_width=20,
                  legend_key_height=150,
                  legend_position='bottom')
        
    return(pl)

def tile_depth_all(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, title_gl, operational_comp=True,robust=True):

    if robust==True: 
        pl_nh=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='Northern Hemisphere', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Northern Hemisphere')+theme(legend_position='none'))
        pl_sh=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='Southern Hemisphere', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Southern Hemisphere')+theme(legend_position='none'))
        pl_tr=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='Tropics', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Tropics')+theme(legend_position='none'))
        pl_ex=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='Extra-Tropics', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Extra-Tropics')+theme(legend_position='none'))
        pl_ar=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='Arctic', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Arcitc')+theme(legend_position='none'))
        pl_an=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='Antarctic', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Antarctic')+theme(legend_position='none'))
        pl_eu=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='Europe', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Europe')+theme(legend_position='none'))
        pl_nam=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='North America', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='North America')+theme(legend_position='none'))
        pl_nat=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='North Atlantic', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='North Atlantic')+theme(legend_position='none'))
        pl_np=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='North Pacific', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='North Pacific')+theme(legend_position='none'))
        pl_ea=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='East Asia', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='East Asia')+theme(legend_position='none'))
        pl_au=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='AusNZ', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='AusNZ')+theme(legend_position='none'))
        pl_gl=pw.load_ggplot(plot_tile_depth(RMSE_day_1.iloc[:,:-1], RMSE_day_3.iloc[:,:-1], RMSE_day_5.iloc[:,:-1], RMSE_day_7.iloc[:,:-1], RMSE_day_10.iloc[:,:-1], region='Global', operational_comp=operational_comp,robust=robust, text_size_table=40, text_size_axis=30, abbreviation=False)+
        labs(x= '', y='Global', title=title_gl ))
        
    else:
        
        pl_nh=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Northern Hemisphere', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Northern Hemisphere')+theme(legend_position='none'))
        pl_sh=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Southern Hemisphere', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Southern Hemisphere')+theme(legend_position='none'))
        pl_tr=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Tropics', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Tropics')+theme(legend_position='none'))
        pl_ex=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Extra-Tropics', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Extra-Tropics')+theme(legend_position='none'))
        pl_ar=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Arctic', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Arcitc')+theme(legend_position='none'))
        pl_an=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Antarctic', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Antarctic')+theme(legend_position='none'))
        pl_eu=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Europe', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='Europe')+theme(legend_position='none'))
        pl_nam=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='North America', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='North America')+theme(legend_position='none'))
        pl_nat=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='North Atlantic', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='North Atlantic')+theme(legend_position='none'))
        pl_np=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='North Pacific', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='North Pacific')+theme(legend_position='none'))
        pl_ea=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='East Asia', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='East Asia')+theme(legend_position='none'))
        pl_au=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='AusNZ', operational_comp=operational_comp,robust=robust)+
        labs(x= '', y='AusNZ')+theme(legend_position='none'))
        pl_gl=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Global', operational_comp=operational_comp,robust=robust, text_size_table=40, text_size_axis=30, abbreviation=False)+
        labs(x= '', y='Global', title=title_gl ))
    
    a=(pl_gl/(pl_nh|pl_sh)/(pl_tr|pl_ex)/(pl_ar|pl_an)/(pl_eu|pl_nam)/(pl_nat|pl_np)/(pl_ea|pl_au))


    return(a)




def tile_comp_plot(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, operational_comp=True):
    
    if operational_comp==True:
        
        pick_len=3    
        
    else: 
        pick_len=4

    a=pd.melt(((RMSE_day_1.iloc[:, :pick_len]).transpose()).reset_index(), id_vars='index')

    
    ids=a.groupby('variable', sort=False)['value'].idxmin()
    
    RMSE_1_95=(a.iloc[ids]).rename(columns = {'index':'Model', 'variable':'Region', 'value': 'Value'}) 
    RMSE_1_95['Day_quant']="1 day"
    
    RMSE_1_95=pd.concat([RMSE_1_95.reset_index(drop=True),RMSE_day_1.iloc[:,len(RMSE_day_1.columns)-1].reset_index(drop=True)], axis=1)
    
    a=pd.melt(((RMSE_day_3.iloc[:, :pick_len]).transpose()).reset_index(), id_vars='index')
    
    ids=a.groupby('variable', sort=False)['value'].idxmin()
    
    RMSE_3_95=(a.iloc[ids]).rename(columns = {'index':'Model', 'variable':'Region', 'value': 'Value'}) 
    RMSE_3_95['Day_quant']="3 days"
    
    RMSE_3_95=pd.concat([RMSE_3_95.reset_index(drop=True),RMSE_day_3.iloc[:,len(RMSE_day_3.columns)-1].reset_index(drop=True)], axis=1)
    
    
    a=pd.melt(((RMSE_day_5.iloc[:, :pick_len]).transpose()).reset_index(), id_vars='index')
    
    ids=a.groupby('variable', sort=False)['value'].idxmin()
    
    RMSE_5_95=(a.iloc[ids]).rename(columns = {'index':'Model', 'variable':'Region', 'value': 'Value'}) 
    RMSE_5_95['Day_quant']="5 days"
    
    RMSE_5_95=pd.concat([RMSE_5_95.reset_index(drop=True),RMSE_day_5.iloc[:,len(RMSE_day_5.columns)-1].reset_index(drop=True)], axis=1)
    
    
    a=pd.melt(((RMSE_day_7.iloc[:, :pick_len]).transpose()).reset_index(), id_vars='index')
    
    ids=a.groupby('variable', sort=False)['value'].idxmin()
    
    RMSE_7_95=(a.iloc[ids]).rename(columns = {'index':'Model', 'variable':'Region', 'value': 'Value'}) 
    RMSE_7_95['Day_quant']="7 days"
    
    a=pd.melt(((RMSE_day_10.iloc[:, :pick_len]).transpose()).reset_index(), id_vars='index')
    
    RMSE_7_95=pd.concat([RMSE_7_95.reset_index(drop=True),RMSE_day_7.iloc[:,len(RMSE_day_7.columns)-1].reset_index(drop=True)], axis=1)
    
    ids=a.groupby('variable', sort=False)['value'].idxmin()
    
    RMSE_10_95=(a.iloc[ids]).rename(columns = {'index':'Model', 'variable':'Region', 'value': 'Value'}) 
    RMSE_10_95['Day_quant']="10 days"
    
    RMSE_10_95=pd.concat([RMSE_10_95.reset_index(drop=True),RMSE_day_10.iloc[:,len(RMSE_day_10.columns)-1].reset_index(drop=True)], axis=1)
    
    tr=pd.concat([RMSE_1_95, RMSE_3_95, RMSE_5_95, RMSE_7_95, RMSE_10_95])
    
    
    tr['Region']=(tr['Region'].astype('category')).cat.reorder_categories(['Global', 'AusNZ', 'East Asia' , 'North Pacific', 'North Atlantic', 'North America', 'Europe', 'Antarctic', 'Arctic', 
                                                                           'Extra-Tropics', 'Tropics', 'Southern Hemisphere', 'Northern Hemisphere'  
                                                                              ])
    
    tr['Day_quant']=(tr['Day_quant'].astype('category')).cat.reorder_categories(['1 day', '3 days', '5 days' , '7 days', '10 days'
                                                                              ])
    
    if operational_comp==True:
        tr['Model']=pd.Categorical(tr['Model'], categories =['Graphcast','HRES','Pangu'])
    else:
        tr['Model']=pd.Categorical(tr['Model'], categories =['Fuxi','Graphcast','HRES','Pangu'])
        
    tr['Significance']=tr['s Best']
    
    
    model_colors = {'HRES': '#DDDDDD', 'Pangu': '#40B0A6', 'Fuxi': 'pink', 'Graphcast':'#E1BA6A'}
    
    pl=ggplot(tr)+\
        geom_tile(aes(x='Day_quant',y='Region',fill='Model', color='Significance', width=0.9, height=0.9),size=1.5)+\
        scale_color_gradientn(colors=["white","black"],breaks=[0.5],drop=False, guide=False)+\
        scale_fill_manual(values=model_colors, drop=False)+\
        theme_minimal()+\
        theme(plot_background=element_rect(fill='white'),
              text=element_text(family='Verdana'),
              axis_text=element_text(size=24),
              axis_title=element_text(size=24, face='bold'),
              title=element_text(size=28, face='bold'),
              legend_title=element_text(size=22, face='bold'),
              legend_text=element_text(size=22),
              legend_key_size= 50,
              legend_position='bottom',
              )+\
        labs(x= '', y='')

        
    return(pl)



def RMSE_point_global(dat, dat_mem, quant=0.95, greater=True, HRES_ground=True, operational_comp=True, fixed_number=False, along_lat=False, title_pl="",ML_vs_IFS=True, no_hedging=False, robust=True,n_df=36):
  #greate=true when selecting upper quantiles (wind and hot extremes), false for lower quantiles (cold extremes).
  #HRES-ground=True for using HRES t=0 as ground-truth for IFS HRES forecasts
  #operational_comp=True when comparing pre-operational models, fasle for renalysis models
  #fixed_numbers can laways be False. True to take exact same numbers of extremes from each grid-point. Not recently tested.
  #along_lat to evaluate change in RMSE with Latitude. Used only as an experiment for extra plot during revision.
  #ML_vs_IFS=True for when comparing best ML/DL model to IFS HRES. False to  compare all the models without significance testing. 
  #no_hedging=True only when selecting extremes based on IFS HRES forecasts, otheriwse always false.
  #robust=True for use of clustered standard errors
  #n_df is just there in case you would like to use other quantiles. It is the number of observations available at each grid point, used to adjust the number of degrees of freedomof the statistical test.
  
    
    theoretical=dat_mem[0]
    if HRES_ground==True:
        HRES_truth=dat_mem[1]
    nwp_det=dat_mem[2]
    AI_det_1=dat_mem[3]
    AI_det_2=dat_mem[4]
    if operational_comp==False:
        AI_det_3=dat_mem[5]
        num_pred_models=4
    else: 
        num_pred_models=3
        
    if no_hedging==True:
        
        threshold_nwp=dat[2].chunk(dict(time=-1)).quantile(quant,dim='time').values.flatten()

        threshold_nwp=np.tile(threshold_nwp, len(dat[0].time))
        
    else:
    
        threshold_theoretical=dat[0].chunk(dict(time=-1)).quantile(quant,dim='time').values.flatten()

        threshold_theoretical=np.tile(threshold_theoretical, len(dat[0].time))
    
    lat=np.tile(dat[0].latitude, len(dat[0].longitude)*len(dat[0].time))
    lon=np.tile(np.repeat(dat[0].longitude, len(dat[0].latitude)),len(dat[0].time))
    time=np.repeat(dat[0].time, len(dat[0].latitude)*len(dat[0].longitude)).values
    
    
    


    if fixed_number==True:
        
        if no_hedging==True:
            ind = np.where(nwp_det==threshold_nwp)
        
        else:
            ind = np.where(theoretical==threshold_theoretical)
            
        arr_ind= theoretical[ind]
        un_ind=np.unique(arr_ind, return_index=True)[1]
        inde=np.delete(ind,un_ind)
        theoretical=np.delete(theoretical,inde)
        if no_hedging==True:
            
            threshold_nwp=np.delete(threshold_nwp,inde)
        
        else:
            threshold_theoretical=np.delete(threshold_theoretical,inde)
        
        nwp_det=np.delete(nwp_det,inde)
        AI_det_1=np.delete(AI_det_1,inde)
        AI_det_2=np.delete(AI_det_2,inde)
        if operational_comp==False:
            AI_det_3=np.delete(AI_det_3,inde)
        if HRES_ground==True:
            HRES_truth=np.delete(HRES_truth,inde)
        
        lat=np.delete(lat,inde)
        lon=np.delete(lon,inde)
        time=np.delete(time,inde)
        
    
    if no_hedging==True:
        
        if greater==True:
            variable_quant=theoretical[nwp_det>=threshold_nwp]
            
            if HRES_ground==True:
                HRES_truth_variable_quant=HRES_truth[nwp_det>=threshold_nwp]

            HRES_variable_quant=nwp_det[nwp_det>=threshold_nwp]  
            pangu_variable_quant=AI_det_1[nwp_det>=threshold_nwp]
            
            if operational_comp==False:
                fuxi_variable_quant=AI_det_2[nwp_det>=threshold_nwp]
                graphcast_variable_quant=AI_det_3[nwp_det>=threshold_nwp]
            else:
                graphcast_variable_quant=AI_det_2[nwp_det>=threshold_nwp]
                
            lat=lat[nwp_det>=threshold_nwp]
            lon=lon[nwp_det>=threshold_nwp]
            time=time[nwp_det>=threshold_nwp]
           
             
        else:
             variable_quant=theoretical[nwp_det<=threshold_nwp]
             
             if HRES_ground==True:
                HRES_truth_variable_quant=HRES_truth[nwp_det<=threshold_nwp]

             HRES_variable_quant=nwp_det[nwp_det<=threshold_nwp]
             pangu_variable_quant=AI_det_1[nwp_det<=threshold_nwp]
             
             if operational_comp==False:
                 fuxi_variable_quant=AI_det_2[nwp_det<=threshold_nwp]
                 graphcast_variable_quant=AI_det_3[nwp_det<=threshold_nwp]
             else:
                 graphcast_variable_quant=AI_det_2[nwp_det<=threshold_nwp]
                 
             lat=lat[nwp_det<=threshold_nwp]
             lon=lon[nwp_det<=threshold_nwp]
             time=time[nwp_det<=threshold_nwp]
             
        
    else:
            
        if greater==True:
            variable_quant=theoretical[theoretical>=threshold_theoretical]
            
            if HRES_ground==True:
                HRES_truth_variable_quant=HRES_truth[theoretical>=threshold_theoretical]
    
            HRES_variable_quant=nwp_det[theoretical>=threshold_theoretical]  
            pangu_variable_quant=AI_det_1[theoretical>=threshold_theoretical]
            
            if operational_comp==False:
                fuxi_variable_quant=AI_det_2[theoretical>=threshold_theoretical]
                graphcast_variable_quant=AI_det_3[theoretical>=threshold_theoretical]
            else:
                graphcast_variable_quant=AI_det_2[theoretical>=threshold_theoretical]
                
            lat=lat[theoretical>=threshold_theoretical]
            lon=lon[theoretical>=threshold_theoretical]
            time=time[theoretical>=threshold_theoretical]
           
             
        else:
             variable_quant=theoretical[theoretical<=threshold_theoretical]
             
             if HRES_ground==True:
                HRES_truth_variable_quant=HRES_truth[theoretical<=threshold_theoretical]
    
             HRES_variable_quant=nwp_det[theoretical<=threshold_theoretical]
             pangu_variable_quant=AI_det_1[theoretical<=threshold_theoretical]
             
             if operational_comp==False:
                 fuxi_variable_quant=AI_det_2[theoretical<=threshold_theoretical]
                 graphcast_variable_quant=AI_det_3[theoretical<=threshold_theoretical]
             else:
                 graphcast_variable_quant=AI_det_2[theoretical<=threshold_theoretical]
                 
             lat=lat[theoretical<=threshold_theoretical]
             lon=lon[theoretical<=threshold_theoretical]
             time=time[theoretical<=threshold_theoretical]
             
        

    if operational_comp==False:
        if HRES_ground==True:
            sq_diff_HRES=(HRES_variable_quant-HRES_truth_variable_quant)**2
        else:
            sq_diff_HRES=(HRES_variable_quant-variable_quant)**2

        sq_diff_pangu=(pangu_variable_quant-variable_quant)**2
        sq_diff_fuxi=(fuxi_variable_quant-variable_quant)**2
        sq_diff_graphcast=(graphcast_variable_quant-variable_quant)**2
    
    
    else:
        if HRES_ground==True:
            sq_diff_HRES=(HRES_variable_quant-HRES_truth_variable_quant)**2
            sq_diff_pangu=(pangu_variable_quant-HRES_truth_variable_quant)**2
            sq_diff_graphcast=(graphcast_variable_quant-HRES_truth_variable_quant)**2
        else:
            sq_diff_HRES=(HRES_variable_quant-variable_quant)**2
            sq_diff_pangu=(pangu_variable_quant-variable_quant)**2
            sq_diff_graphcast=(graphcast_variable_quant-variable_quant)**2
    
    
    if operational_comp==False:  
        dat_tot = pd.DataFrame({
        
        'Latitude': lat,
        'Longitude': lon,
        'Time': time,
        'Sq_diff_HRES': sq_diff_HRES,
        'Sq_diff_Pangu': sq_diff_pangu,
        'Sq_diff_Fuxi': sq_diff_fuxi,
        'Sq_diff_Graphcast': sq_diff_graphcast
        
    })
        
        model_columns = ['Sq_diff_HRES', 'Sq_diff_Pangu', 'Sq_diff_Fuxi', 'Sq_diff_Graphcast']
    else:
        dat_tot = pd.DataFrame({
        
        'Latitude': lat,
        'Longitude': lon,
        'Time': time,
        'Sq_diff_HRES': sq_diff_HRES,
        'Sq_diff_Pangu': sq_diff_pangu,
        'Sq_diff_Graphcast': sq_diff_graphcast
        
    })
        
        model_columns = ['Sq_diff_HRES', 'Sq_diff_Pangu', 'Sq_diff_Graphcast']
            
    dat_tot['Longitude']=np.where(dat_tot['Longitude']>180,dat_tot['Longitude']-360,dat_tot['Longitude'])
    
    if along_lat==True:
        
        # Function to calculate RMSE
        def calculate_rmse(df, model_cols):
            rmse_dict = {}
            for col in model_cols:
                rmse_dict[col] = df.groupby(['Latitude'])[col].apply(lambda x: np.sqrt(np.mean(x)))
            rmse_df = pd.DataFrame(rmse_dict).reset_index()
            return rmse_df
        
        
        
    else:
    
        # Function to calculate RMSE
        def calculate_rmse(df, model_cols):
            rmse_dict = {}
            for col in model_cols:
                rmse_dict[col] = df.groupby(['Latitude', 'Longitude'])[col].apply(lambda x: np.sqrt(np.mean(x)))
            rmse_df = pd.DataFrame(rmse_dict).reset_index()
            return rmse_df
    
    
    
    # Calculate RMSE for each model at each (Latitude, Longitude) point
    RMSE_point = calculate_rmse(dat_tot, model_columns)
    
   
    # If using this function to build the latitude based RMSE line plot 
    if along_lat==True:
        
        RMSE_point['Sq_diff_Pangu']=(RMSE_point['Sq_diff_Pangu']-RMSE_point['Sq_diff_HRES'])*100/RMSE_point['Sq_diff_HRES']
        RMSE_point['Sq_diff_Graphcast']=(RMSE_point['Sq_diff_Graphcast']-RMSE_point['Sq_diff_HRES'])*100/RMSE_point['Sq_diff_HRES']
        RMSE_point = RMSE_point.drop(columns=['Sq_diff_HRES'])

        RMSE_point=RMSE_point.melt(id_vars='Latitude', var_name='Model')
        RMSE_point['Model'] = RMSE_point['Model'].str.replace('Sq_diff_', '')
        
        return RMSE_point
    
    if ML_vs_IFS==True:
        
        if operational_comp==True:
        
            RMSE_point['Sq_diff_ML'] = np.minimum(RMSE_point['Sq_diff_Pangu'], RMSE_point['Sq_diff_Graphcast'])
            RMSE_point['Best_model_name'] = np.where(RMSE_point['Sq_diff_Pangu'] <= RMSE_point['Sq_diff_Graphcast'], 'Sq_diff_Pangu', 'Sq_diff_Graphcast')
            RMSE_point = RMSE_point.drop(columns=['Sq_diff_Pangu', 'Sq_diff_Graphcast'])
            
        
            dat_tot = pd.merge(dat_tot, RMSE_point.loc[:,['Latitude','Longitude','Best_model_name']], on=['Latitude', 'Longitude'], how='left')
            
    
            dat_tot['Sq_diff_ML']=np.where(dat_tot['Best_model_name'] == 'Sq_diff_Pangu', dat_tot['Sq_diff_Pangu'], dat_tot['Sq_diff_Graphcast'])
            dat_tot=dat_tot.drop(columns=['Sq_diff_Pangu', 'Sq_diff_Graphcast'])
            RMSE_point = RMSE_point.drop(columns=['Best_model_name'])
            
        else:
            
            # Determine the minimum squared difference and the corresponding model name
            RMSE_point['Sq_diff_ML'] = RMSE_point[['Sq_diff_Pangu', 'Sq_diff_Graphcast', 'Sq_diff_Fuxi']].min(axis=1)
            RMSE_point['Best_model_name'] = RMSE_point[['Sq_diff_Pangu', 'Sq_diff_Graphcast', 'Sq_diff_Fuxi']].idxmin(axis=1)
            
            # Drop the individual squared difference columns for the models
            RMSE_point = RMSE_point.drop(columns=['Sq_diff_Pangu', 'Sq_diff_Graphcast', 'Sq_diff_Fuxi'])
            
            # Merge the 'Best_model_name' column with 'dat_tot'
            dat_tot = pd.merge(dat_tot, RMSE_point.loc[:, ['Latitude', 'Longitude', 'Best_model_name']], on=['Latitude', 'Longitude'], how='left')
            
            # Map the minimum squared difference back to 'dat_tot' based on the best model name
            dat_tot['Sq_diff_ML'] = dat_tot.apply(lambda row: row[row['Best_model_name']], axis=1)
            
            # Drop the individual squared difference columns for the models from 'dat_tot'
            dat_tot = dat_tot.drop(columns=['Sq_diff_Pangu', 'Sq_diff_Graphcast', 'Sq_diff_Fuxi'])
            
            # Drop the 'Best_model_name' column 
            RMSE_point = RMSE_point.drop(columns=['Best_model_name'])


# Function to find the best two models at each (lat, lon) point
    def find_best_two_models(rmse_df):
        best_models = []
        for idx, row in rmse_df.iterrows():
            model_rmse = row[2:]  # RMSE values for all models at this (lat, lon)
            best_model = model_rmse.idxmin()  # Best model
            second_best_model = model_rmse[model_rmse != model_rmse.min()].idxmin()  # Second best model
            RMSE_best_model = model_rmse.min()   #Difference in RMSE between best and second best model
            RMSE_second_best_model=model_rmse[model_rmse != model_rmse.min()].min()
            best_models.append((row['Latitude'], row['Longitude'], best_model, second_best_model, RMSE_best_model, RMSE_second_best_model))
        
        best_two_models_df = pd.DataFrame(best_models, columns=['Latitude', 'Longitude', 'Best_Model', 'Second_Best_Model','RMSE_Best_Model','RMSE_Second_Best_Model'])
        return best_two_models_df

    
    best_two_models = find_best_two_models(RMSE_point)
    
    if robust == True: 
    

        def perform_paired_t_test(df, best_models):
            results = []
            for idx, row in best_models.iterrows():
                lat, lon = row['Latitude'], row['Longitude']
                best_model_col = 'Sq_diff_' + row['Best_Model'].split('_')[-1]
                second_best_model_col = 'Sq_diff_' + row['Second_Best_Model'].split('_')[-1]
                
                lat_lon_data = df[(df['Latitude'] == lat) & (df['Longitude'] == lon)]
                best_model_values = lat_lon_data[best_model_col]
                second_best_model_values = lat_lon_data[second_best_model_col]
                
                lat_lon_data['Values']= best_model_values-second_best_model_values
                
                lat_lon_data = lat_lon_data.set_index(['Latitude', 'Time'])  #Here the location index does not matter. It is fixed since we are looking only at one location at a time.
                

                model_cluster = lm.PanelOLS.from_formula(
                formula=("Values ~ 1"),
                data=lat_lon_data).fit(cov_type="clustered", cluster_entity=False, cluster_time=True)
                 
                t_stat=model_cluster.tstats[0]


    
                results.append({'Latitude': lat, 'Longitude': lon, 't_stat':t_stat})
            return pd.DataFrame(results)
    
                
        test_results = perform_paired_t_test(dat_tot, best_two_models)
        test_results["Model"]=best_two_models["Best_Model"]
        test_results["RMSE_best_model"]=best_two_models["RMSE_Best_Model"]
        test_results["RMSE_second_best_model"]=best_two_models["RMSE_Second_Best_Model"]
        test_results['Model'] = test_results['Model'].str.replace('Sq_diff_', '')
        return test_results
        
    else: 
            
        best_two_models['Model'] = best_two_models["Best_Model"]
        best_two_models['Model'] = best_two_models['Model'].str.replace('Sq_diff_', '')
           
        return best_two_models
           
            
        
     

def p_val_cor (dat,df=36,alpha=0.1):
    
    dat["Model"]=np.where((dat["Model"] == "ML"),"DL",dat["Model"]) 
    p_val=2*(t.cdf(-abs(dat['t_stat']), df))
    sig_cor=(statsmodels.stats.multitest.fdrcorrection(p_val,alpha=0.1)[0])*1
    dat["Significant_cor"]=sig_cor
    dat["Sig_Model_cor"]=np.where((dat["Significant_cor"] == 0),"NA",dat["Model"]) 

    return dat


    # Plot the QQ plot using plotnine
def plot_RMSE_point_global(RMSE_point_df,title_pl="", guide_true=False, correction=True,test=True):
        
        if test==False:
            
            model_colors = {'HRES': '#DDDDDD', 'Pangu': '#40B0A6', 'Fuxi': 'pink', 'Graphcast':'#E1BA6A'}
        
            if guide_true==True:
            
               RMSE_base_plot_world=pw.load_ggplot((
                ggplot()
                + expand_limits(x=0, y=0)
                + theme_void()
                +theme_bw()+
                geom_tile(RMSE_point_df,aes(x='Longitude',y='Latitude',fill='Model'))+
                geom_map(world,  color='black', fill='white',alpha=0)+
                scale_fill_manual(values= model_colors)+
                scale_x_continuous(expand=(0,0))+
                scale_y_continuous(expand=(0,0))+
                #coord_fixed(1.5)+
                labs(x='',y='', title=title_pl, fill="Best model")+
                theme(text=element_text(family='Verdana'),
                      axis_text=element_text(size=18),
                      axis_title=element_text(size=18, face='bold'),
                      title=element_text(size=20, face='bold'),
                      legend_title=element_text(size=16, face='bold'),
                      legend_text=element_text(size=22),
                      legend_key_size= 30,
                      legend_position='right'
                      )
                ))
            else:
                   
                RMSE_base_plot_world=pw.load_ggplot((
                 ggplot()
                 + expand_limits(x=0, y=0)
                 + theme_void()
                 +theme_bw()+
                 geom_tile(RMSE_point_df,aes(x='Longitude',y='Latitude',fill='Model'))+
                 geom_map(world,  color='black', fill='white',alpha=0)+
                 scale_fill_manual(values= model_colors, guide=False)+
                 scale_x_continuous(expand=(0,0))+
                 scale_y_continuous(expand=(0,0))+
                 #coord_fixed(1.5)+
                 labs(x='',y='', title=title_pl)+
                 theme(text=element_text(family='Verdana'),
                       axis_text=element_text(size=22),
                       axis_title=element_text(size=22, face='bold'),
                       title=element_text(size=24, face='bold')
                       )
                 ))
                
            return RMSE_base_plot_world
        
        else:
        
            model_colors = {'HRES': 'red', 'DL':'blue'}
        
            if correction==True:
                RMSE_point_gray=RMSE_point_df[RMSE_point_df["Sig_Model_cor"]=="NA"]
                RMSE_point_df = RMSE_point_df[RMSE_point_df["Sig_Model_cor"]!="NA"]
            
            
                if guide_true==True:
                
                   RMSE_base_plot_world=pw.load_ggplot((
                    ggplot()
                    + expand_limits(x=0, y=0)
                    + theme_void()
                    +theme_bw()+
                    geom_tile(RMSE_point_df,aes(x='Longitude',y='Latitude',fill='Sig_Model_cor'))+
                    geom_tile(RMSE_point_gray,aes(x='Longitude',y='Latitude'),fill='gray',show_legend=False)+
                    geom_map(world,  color='black', fill='white',alpha=0)+
                    scale_fill_manual(values= model_colors)+
                    scale_x_continuous(expand=(0,0))+
                    scale_y_continuous(expand=(0,0))+
                    #coord_fixed(1.5)+
                    labs(x='',y='', title=title_pl, fill="Best model")+
                    theme(text=element_text(family='Verdana'),
                          axis_text=element_text(size=18),
                          axis_title=element_text(size=18, face='bold'),
                          title=element_text(size=20, face='bold'),
                          legend_title=element_text(size=16, face='bold'),
                          legend_text=element_text(size=22),
                          legend_key_size= 30,
                          legend_position='right'
                          )
                    ))
                else:
                       
                    RMSE_base_plot_world=pw.load_ggplot((
                     ggplot()
                     + expand_limits(x=0, y=0)
                     + theme_void()
                     +theme_bw()+
                     geom_tile(RMSE_point_df,aes(x='Longitude',y='Latitude',fill='Sig_Model_cor'))+
                     geom_tile(RMSE_point_gray,aes(x='Longitude',y='Latitude'),fill='gray',show_legend=False)+
                     geom_map(world,  color='black', fill='white',alpha=0)+
                     scale_fill_manual(values= model_colors, guide=False)+
                     scale_x_continuous(expand=(0,0))+
                     scale_y_continuous(expand=(0,0))+
                     #coord_fixed(1.5)+
                     labs(x='',y='', title=title_pl)+
                     theme(text=element_text(family='Verdana'),
                           axis_text=element_text(size=22),
                           axis_title=element_text(size=22, face='bold'),
                           title=element_text(size=24, face='bold')
                           )
                     ))
                
                
            else:
                RMSE_point_gray=RMSE_point_df[RMSE_point_df["Sig_Model"]=="NA"]
                
                if guide_true==True:
                
                   RMSE_base_plot_world=pw.load_ggplot((
                    ggplot()
                    + expand_limits(x=0, y=0)
                    + theme_void()
                    +theme_bw()+
                    geom_tile(RMSE_point_df,aes(x='Longitude',y='Latitude',fill='Sig_Model'))+
                    geom_tile(RMSE_point_gray,aes(x='Longitude',y='Latitude'),fill='gray')+
                    geom_map(world,  color='black', fill='white',alpha=0)+
                    scale_fill_manual(values= model_colors)+
                    scale_x_continuous(expand=(0,0))+
                    scale_y_continuous(expand=(0,0))+
                    #coord_fixed(1.5)+
                    labs(x='',y='', title=title_pl, fill="Best model")+
                    theme(text=element_text(family='Verdana'),
                          axis_text=element_text(size=18),
                          axis_title=element_text(size=18, face='bold'),
                          title=element_text(size=20, face='bold'),
                          legend_title=element_text(size=16, face='bold'),
                          legend_text=element_text(size=22),
                          legend_key_size= 30,
                          legend_position='right'
                          )
                    ))
                else:
                       
                    RMSE_base_plot_world=pw.load_ggplot((
                     ggplot()
                     + expand_limits(x=0, y=0)
                     + theme_void()
                     +theme_bw()+
                     geom_tile(RMSE_point_df,aes(x='Longitude',y='Latitude',fill='Sig_Model'))+
                     geom_map(world,  color='black', fill='white',alpha=0)+
                     scale_fill_manual(values= model_colors, guide=False)+
                     scale_x_continuous(expand=(0,0))+
                     scale_y_continuous(expand=(0,0))+
                     #coord_fixed(1.5)+
                     labs(x='',y='', title=title_pl)+
                     theme(text=element_text(family='Verdana'),
                           axis_text=element_text(size=22),
                           axis_title=element_text(size=22, face='bold'),
                           title=element_text(size=24, face='bold')
                           )
                     ))
            
            return RMSE_base_plot_world
    
    
def plot_RMSE_line_lat(RMSE_point_df,title_pl="", guide_true=False):
    
    
    if guide_true==True:
    
       RMSE_base_plot_world=pw.load_ggplot((
        ggplot()+
        theme_bw()+
        geom_line(RMSE_point_df,aes(x='Latitude',y='value',color='Model'))+
        scale_color_manual(values= model_colors)+
        scale_x_continuous(expand=(0,0), breaks=[-90,-60,-30,0,30,60,90])+
        scale_y_continuous(expand=(0,0))+
        coord_cartesian(ylim=[-50,50])+
        labs(x='',y='', title=title_pl, fill="Best model")+
        theme(text=element_text(family='Verdana'),
              axis_text=element_text(size=18),
              axis_title=element_text(size=18, face='bold'),
              title=element_text(size=20, face='bold'),
              legend_title=element_text(size=20, face='bold'),
              legend_text=element_text(size=22),
              legend_key_size= 30,
              legend_position='right'
              )
        ))
    else:
           
       RMSE_base_plot_world=pw.load_ggplot((
        ggplot()+
        theme_bw()+
        geom_line(RMSE_point_df,aes(x='Latitude',y='value',color='Model'),show_legend=guide_true,size=0.7)+
        scale_color_manual(values= model_colors)+
        scale_x_continuous(expand=(0,0), breaks=[-90,-60,-30,0,30,60,90])+
        scale_y_continuous(expand=(0,0))+
        coord_cartesian(ylim=[-50,50])+
         labs(x='',y='', title=title_pl)+
         theme(text=element_text(family='Verdana'),
               axis_text=element_text(size=22),
               axis_title=element_text(size=22, face='bold'),
               title=element_text(size=24, face='bold')
               )
         ))
    
    return RMSE_base_plot_world   



def plot_RMSE_magnitude(RMSE_point_df,title_pl="", guide_true=False, all_models=False):
    
    
    
    if all_models==False:
        RMSE_point_df['Magnitude']=RMSE_point_df['RMSE_best_model']-RMSE_point_df['RMSE_second_best_model']
        RMSE_point_df['Magnitude']=np.where((RMSE_point_df['Model']=='HRES'),-RMSE_point_df['Magnitude']*100/RMSE_point_df['RMSE_best_model'],RMSE_point_df['Magnitude']*100/RMSE_point_df['RMSE_second_best_model'])
    else:
        RMSE_point_df['Magnitude']=-(RMSE_point_df['RMSE_Best_Model']-RMSE_point_df['RMSE_Second_Best_Model'])*100/RMSE_point_df['RMSE_Second_Best_Model']
    
    if guide_true==True:
        
        
        if all_models==False:
        
           RMSE_base_plot_world=pw.load_ggplot((
            ggplot()
            + expand_limits(x=0, y=0)
            + theme_void()
            +theme_bw()+
            geom_tile(RMSE_point_df,aes(x='Longitude',y='Latitude',fill='Magnitude'))+
            geom_map(world,  color='black', fill='white',alpha=0)+
            scale_fill_gradientn(colors=["#0B559F","#2B7BBA","#539ECD","#89BEDC", "#BAD6EB", "#DBE9F6", "#FFFFFF", "#FEDBCC", "#FCAF93", "#FC8161", "#F14E38", "#BD1E1D", "#A91016"],
                                 values=[0, 0.25,0.4167,0.4583,0.483,0.4916,0.50,0.5087,0.5117,0.5417,0.5833,0.75,1], breaks=[-90,-50, -20, 0, 20, 50, 90], limits=[-100,100], 
                                 name="% difference in RMSE vs IFS HRES")+
            scale_x_continuous(expand=(0,0))+
            scale_y_continuous(expand=(0,0))+
            #coord_fixed(1.5)+
            labs(x='',y='', title=title_pl, fill="Best model")+
            theme(plot_background=element_rect(fill='white'),
                  text=element_text(family='Verdana', color= 'black'),
                  axis_text=element_text(size=22),
                  axis_title=element_text(size=22, face='bold'),
                  title=element_text(size=24, face='bold', hjust=0),
                  legend_title=element_text(size=24, face='bold'),
                  legend_text=element_text(size=18),
                  legend_key_width=15,
                  legend_key_height=70,
                  legend_position='bottom')))
           
        else:
            
            RMSE_base_plot_world=pw.load_ggplot((
             ggplot()
             + expand_limits(x=0, y=0)
             + theme_void()
             +theme_bw()+
             geom_tile(RMSE_point_df,aes(x='Longitude',y='Latitude',fill='Magnitude'))+
             geom_map(world,  color='black', fill='white',alpha=0)+
             scale_fill_gradient(low="#FFFFFF", high="#0B559F", breaks=[0,20,40,60,80,100],limits=[0,90],
                                  name="% difference in RMSE between the two best models")+
             scale_x_continuous(expand=(0,0))+
             scale_y_continuous(expand=(0,0))+
             #coord_fixed(1.5)+
             labs(x='',y='', title=title_pl, fill="Best model")+
             theme(plot_background=element_rect(fill='white'),
                   text=element_text(family='Verdana', color= 'black'),
                   axis_text=element_text(size=22),
                   axis_title=element_text(size=22, face='bold'),
                   title=element_text(size=24, face='bold', hjust=0),
                   legend_title=element_text(size=20, face='bold'),
                   legend_text=element_text(size=18),
                   legend_key_width=15,
                   legend_key_height=70,
                   legend_position='bottom')))
            
        
    else:
        
        if all_models==False:

            RMSE_base_plot_world=pw.load_ggplot((
            ggplot()
            + expand_limits(x=0, y=0)
            + theme_void()
            +theme_bw()+
            geom_tile(RMSE_point_df,aes(x='Longitude',y='Latitude',fill='Magnitude'),show_legend=guide_true)+
            geom_map(world,  color='black', fill='white',alpha=0)+
            scale_fill_gradientn(colors=["#0B559F","#2B7BBA","#539ECD","#89BEDC", "#BAD6EB", "#DBE9F6", "#FFFFFF", "#FEDBCC", "#FCAF93", "#FC8161", "#F14E38", "#BD1E1D", "#A91016"],
                                 values=[0, 0.25,0.4167,0.4583,0.483,0.4916,0.50,0.5087,0.5117,0.5417,0.5833,0.75,1], breaks=[-90,-50, -10, 0, 10, 50, 90], limits=[-100,100], 
                                 name="% difference in RMSE vs IFS HRES")+
            scale_x_continuous(expand=(0,0))+
            scale_y_continuous(expand=(0,0))+
            #coord_fixed(1.5)+
            labs(x='',y='', title=title_pl)+
            theme(text=element_text(family='Verdana'),
                  axis_text=element_text(size=22),
                  axis_title=element_text(size=22, face='bold'),
                  title=element_text(size=24, face='bold')
                  )
            ))
            
            
        else:
            
            RMSE_base_plot_world=pw.load_ggplot((
            ggplot()
            + expand_limits(x=0, y=0)
            + theme_void()
            +theme_bw()+
            geom_tile(RMSE_point_df,aes(x='Longitude',y='Latitude',fill='Magnitude'),show_legend=guide_true)+
            geom_map(world,  color='black', fill='white',alpha=0)+
            scale_fill_gradient(low="#FFFFFF", high="#0B559F",breaks=[0,20,40,60,80,100],limits=[0,90],
                                 name="% difference in RMSE between the two best models")+
            scale_x_continuous(expand=(0,0))+
            scale_y_continuous(expand=(0,0))+
            #coord_fixed(1.5)+
            labs(x='',y='', title=title_pl)+
            theme(text=element_text(family='Verdana'),
                  axis_text=element_text(size=22),
                  axis_title=element_text(size=22, face='bold'),
                  title=element_text(size=24, face='bold')
                  )
            ))
            

    
    return RMSE_base_plot_world
    
  


def qqplot_extreme(dat_mem, quant, operational_comp, greater, guide_true=False):
    
    theoretical=dat_mem[0]
    nwp_det=dat_mem[2]
    AI_det_1=dat_mem[3]
    AI_det_2=dat_mem[4]
    if operational_comp==False:
        AI_det_3=dat_mem[5]
        num_pred_models=4
    else: 
        num_pred_models=3
    
    
    if greater==True:
         variable_quant=theoretical[theoretical>np.quantile(theoretical,quant)]
         HRES_variable_quant=nwp_det[nwp_det>np.quantile(nwp_det,quant)]
         pangu_variable_quant=AI_det_1[AI_det_1>np.quantile(AI_det_1,quant)]
         if operational_comp==False:
             fuxi_variable_quant=AI_det_2[AI_det_2>np.quantile(AI_det_2,quant)]
             graphcast_variable_quant=AI_det_3[AI_det_3>np.quantile(AI_det_3,quant)]
         else:
            graphcast_variable_quant=AI_det_2[AI_det_2>np.quantile(AI_det_2,quant)]
         
  
         true_quantiles = np.percentile( variable_quant, np.arange(0, 99, 1))
         predicted_quantiles1 = np.percentile(HRES_variable_quant, np.arange(0, 99, 1))
         predicted_quantiles2 = np.percentile(pangu_variable_quant, np.arange(0, 99, 1))
         if operational_comp==False:
             predicted_quantiles3 = np.percentile(fuxi_variable_quant, np.arange(0, 99, 1))
             predicted_quantiles4 = np.percentile(graphcast_variable_quant, np.arange(0, 99, 1))
         else:
             predicted_quantiles3 = np.percentile(graphcast_variable_quant, np.arange(0, 99, 1))
    else:
         variable_quant=theoretical[theoretical<np.quantile(theoretical,quant)]
         HRES_variable_quant=nwp_det[nwp_det<np.quantile(nwp_det,quant)]
         pangu_variable_quant=AI_det_1[AI_det_1<np.quantile(AI_det_1,quant)]
         if operational_comp==False:
             fuxi_variable_quant=AI_det_2[AI_det_2<np.quantile(AI_det_2,quant)]
             graphcast_variable_quant=AI_det_3[AI_det_3<np.quantile(AI_det_3,quant)]
         else:
             graphcast_variable_quant=AI_det_2[AI_det_2<np.quantile(AI_det_2,quant)]
         
         true_quantiles = np.percentile( variable_quant, np.arange(1, 100, 1))
         predicted_quantiles1 = np.percentile(HRES_variable_quant, np.arange(1, 100, 1))
         predicted_quantiles2 = np.percentile(pangu_variable_quant, np.arange(1, 100, 1))
         if operational_comp==False:
             predicted_quantiles3 = np.percentile(fuxi_variable_quant, np.arange(1, 100, 1))
             predicted_quantiles4 = np.percentile(graphcast_variable_quant, np.arange(1, 100, 1))
         else:
             predicted_quantiles3 = np.percentile(graphcast_variable_quant, np.arange(1, 100, 1))
             

    model_colors = {'HRES': 'black', 'Pangu': '#40B0A6', 'Fuxi': '#99DDFF', 'Graphcast':'#E1BA6A'}

    if operational_comp==False:
        qqplot_data = pd.DataFrame({
            'True': np.tile(true_quantiles, num_pred_models),
            'Predicted': np.concatenate([predicted_quantiles1, predicted_quantiles2, predicted_quantiles3, predicted_quantiles4]),
            'Model': np.repeat(['HRES', 'Pangu', 'Fuxi','Graphcast'], len(true_quantiles))
        })
         

    else:
        qqplot_data = pd.DataFrame({
            'True': np.tile(true_quantiles, num_pred_models),
            'Predicted': np.concatenate([predicted_quantiles1, predicted_quantiles2, predicted_quantiles3]),
            'Model': np.repeat(['HRES', 'Pangu','Graphcast'], len(true_quantiles))
        })
         
        
        # Plot the QQ plot using plotnine
    
    if guide_true==True:
        
        plot_extr=(
            ggplot(qqplot_data, aes(x='True', y='Predicted', color='Model')) +
            geom_abline(intercept=0, slope=1, linetype='dashed', color='black') +
            geom_point(size=2.5) +
            labs(x='True Values', y='Predicted Values', title='QQ Plot of Predicted vs True Values')+
            scale_color_manual(values= model_colors)+\
            labs(x='ERA5 10m windspeed, m/s', y='Predicted 10m windspeed, m/s', title='QQ Plot of Predicted vs ERA5, 10m windspeed over 20 m/s')+\
                    theme_bw()+\
                    theme(
                    text=element_text(family='Verdana'),
                    axis_text=element_text(size=15),
                    axis_title=element_text(size=21, face='bold'),
                    title=element_text(size=28, face='bold'),
                    legend_title=element_text(size=22, face='bold'),
                    legend_text=element_text(size=22),
                    legend_key_size= 50,
                    legend_position='right'
                )+ 
                guides(colour = guide_legend(override_aes = {"size":8}, order=1))
            )
    else:
        plot_extr=(
            ggplot(qqplot_data, aes(x='True', y='Predicted', color='Model')) +
            geom_abline(intercept=0, slope=1, linetype='dashed', color='black') +
            geom_point(size=2.5) +
            labs(x='True Values', y='Predicted Values', title='QQ Plot of Predicted vs True Values')+
            scale_color_manual(values= model_colors, guide=False)+\
            labs(x='ERA5 10m windspeed, m/s', y='Predicted 10m windspeed, m/s', title='QQ Plot of Predicted vs ERA5, 10m windspeed over 20 m/s')+\
                    theme_bw()+\
                    theme(
                    text=element_text(family='Verdana'),
                    axis_text=element_text(size=15),
                    axis_title=element_text(size=21, face='bold'),
                    title=element_text(size=28, face='bold')
                )
            )
            

    return(plot_extr) 

    


def qqplot_all(dat_tot, quant=0.95, greater=True, HRES_ground=False, operational_comp=True, temperature=True):
    
    if temperature==True:
    
        qq_NH=pw.load_ggplot(qqplot_extreme(dat_tot[1], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='Northern Hempisphere'))
        qq_SH=pw.load_ggplot(qqplot_extreme(dat_tot[3], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='Southern Hemisphere'))
        qq_tropics=pw.load_ggplot(qqplot_extreme(dat_tot[5], quant, operational_comp=operational_comp, greater=greater, guide_true=True)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='Tropics'))
        qq_EXTRA=pw.load_ggplot(qqplot_extreme(dat_tot[7], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='Extra-Tropics'))
        qq_ARC=pw.load_ggplot(qqplot_extreme(dat_tot[9], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='Arctic'))
        qq_ANT=pw.load_ggplot(qqplot_extreme(dat_tot[11], quant, operational_comp=operational_comp, greater=greater, guide_true=True)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='Antartic'))
            
        #((qq_NH|qq_SH)/(qq_tropics|qq_EXTRA)/(qq_ARC|qq_ANT)).savefig(r'C:\Users\leool650\OneDrive - Uppsala universitet\Desktop\Alvex_py\Model_comparison\fig\5_macro_oper.png')
        
        qq_EU=pw.load_ggplot(qqplot_extreme(dat_tot[13], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='Europe'))
        qq_NAM=pw.load_ggplot(qqplot_extreme(dat_tot[15], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='North America'))
        qq_NAT=pw.load_ggplot(qqplot_extreme(dat_tot[17], quant, operational_comp=operational_comp, greater=greater, guide_true=True)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='North Atlantic'))
        qq_NAP=pw.load_ggplot(qqplot_extreme(dat_tot[19], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='North Pacific'))
        qq_EA=pw.load_ggplot(qqplot_extreme(dat_tot[21], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='East Asia'))
        qq_ANZ=pw.load_ggplot(qqplot_extreme(dat_tot[23], quant, operational_comp=operational_comp, greater=greater, guide_true=True)+\
        labs(x='ERA5 2m temperature, K', y='Predicted 2m temperature, K', title='AusNZ'))
        
    else:
        
        qq_NH=pw.load_ggplot(qqplot_extreme(dat_tot[1], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='Northern Hempisphere'))
        qq_SH=pw.load_ggplot(qqplot_extreme(dat_tot[3], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='Southern Hemisphere'))
        qq_tropics=pw.load_ggplot(qqplot_extreme(dat_tot[5], quant, operational_comp=operational_comp, greater=greater, guide_true=True)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='Tropics'))
        qq_EXTRA=pw.load_ggplot(qqplot_extreme(dat_tot[7], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='Extra-Tropics'))
        qq_ARC=pw.load_ggplot(qqplot_extreme(dat_tot[9], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='Arctic'))
        qq_ANT=pw.load_ggplot(qqplot_extreme(dat_tot[11], quant, operational_comp=operational_comp, greater=greater, guide_true=True)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='Antartic'))
            
        #((qq_NH|qq_SH)/(qq_tropics|qq_EXTRA)/(qq_ARC|qq_ANT)).savefig(r'C:\Users\leool650\OneDrive - Uppsala universitet\Desktop\Alvex_py\Model_comparison\fig\5_macro_oper.png')
        
        qq_EU=pw.load_ggplot(qqplot_extreme(dat_tot[13], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='Europe'))
        qq_NAM=pw.load_ggplot(qqplot_extreme(dat_tot[15], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='North America'))
        qq_NAT=pw.load_ggplot(qqplot_extreme(dat_tot[17], quant, operational_comp=operational_comp, greater=greater, guide_true=True)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='North Atlantic'))
        qq_NAP=pw.load_ggplot(qqplot_extreme(dat_tot[19], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='North Pacific'))
        qq_EA=pw.load_ggplot(qqplot_extreme(dat_tot[21], quant, operational_comp=operational_comp, greater=greater)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='East Asia'))
        qq_ANZ=pw.load_ggplot(qqplot_extreme(dat_tot[23], quant, operational_comp=operational_comp, greater=greater, guide_true=True)+\
        labs(x='ERA5 10m windspeed, K', y='Predicted 10m windspeed, m/s', title='AusNZ'))
            
    qq_NH.set_index("a", fontsize=30)
    qq_SH.set_index("b", fontsize=30)
    qq_tropics.set_index("c", fontsize=30)
    qq_EXTRA.set_index("d", fontsize=30)
    qq_ARC.set_index("e", fontsize=30)
    qq_ANT.set_index("f", fontsize=30)
    qq_EU.set_index("g", fontsize=30)
    qq_NAM.set_index("h", fontsize=30)
    qq_NAT.set_index("i", fontsize=30)
    qq_NAP.set_index("j", fontsize=30)
    qq_EA.set_index("k", fontsize=30)
    qq_ANZ.set_index("l", fontsize=30)
        
    return((qq_NH|qq_SH|qq_tropics)/(qq_EXTRA|qq_ARC|qq_ANT)/(qq_EU|qq_NAM|qq_NAT)/(qq_NAP|qq_EA|qq_ANZ))



