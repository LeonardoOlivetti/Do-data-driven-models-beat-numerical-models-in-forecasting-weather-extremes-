# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:54:26 2024

@author: leool650
"""

#%% Data preparation 

from datetime import date, datetime
from plotnine import *
import pandas as pd
import patchworklib as pw
import geopandas as gpd

def prep_time_loc(theoretical, HRES_truth, nwp_det, AI_det_1, AI_det_2, AI_det_3=None,lower_latitude=-90,upper_latitude=90, lower_longitude=-1, upper_longitude=361, operational_comp=False):
    
    
    
    
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



def write_data (dat, operational_comp=False):

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




def comp_RMSE_tail(dat, dat_mem, operational_comp, greater, HRES_ground,quant=None,):
   
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
        if greater==True:
             variable_quant=theoretical[theoretical>np.quantile(theoretical,quant)]
             cos_weights_quant=cos_weights[theoretical>np.quantile(theoretical,quant)]
             
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
            RMSE_tail_HRES=(sum(cos_weights_quant*(HRES_variable_quant-HRES_truth_variable_quant)**2)/len(variable_quant))**(1/2)
        else:
            RMSE_tail_HRES=(sum(cos_weights_quant*(HRES_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
        
        RMSE_tail_pangu=(sum(cos_weights_quant*(pangu_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
        RMSE_tail_graphcast=(sum(cos_weights_quant*(graphcast_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
        RMSE_tail_fuxi=(sum(cos_weights_quant*(fuxi_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
        
        return RMSE_tail_HRES, RMSE_tail_pangu, RMSE_tail_fuxi, RMSE_tail_graphcast
        
    else:

        if HRES_ground==True:
            RMSE_tail_HRES=(sum(cos_weights_quant*(HRES_variable_quant-HRES_truth_variable_quant)**2)/len(variable_quant))**(1/2)
            RMSE_tail_pangu=(sum(cos_weights_quant*(pangu_variable_quant-HRES_truth_variable_quant)**2)/len(variable_quant))**(1/2)
            RMSE_tail_graphcast=(sum(cos_weights_quant*(graphcast_variable_quant-HRES_truth_variable_quant)**2)/len(variable_quant))**(1/2)
        else:
            RMSE_tail_HRES=(sum(cos_weights_quant*(HRES_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
            RMSE_tail_pangu=(sum(cos_weights_quant*(pangu_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
            RMSE_tail_graphcast=(sum(cos_weights_quant*(graphcast_variable_quant-variable_quant)**2)/len(variable_quant))**(1/2)
    
        return RMSE_tail_HRES, RMSE_tail_pangu, RMSE_tail_graphcast
    



def RMSE_all(dat_tot, greater=True, HRES_ground=False, operational_comp=True, quant=None):
    
    
    
    RMSE_NH=comp_RMSE_tail(dat_tot[0], dat_tot[1], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    RMSE_SH=comp_RMSE_tail(dat_tot[2], dat_tot[3], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    RMSE_tropics=comp_RMSE_tail(dat_tot[4], dat_tot[5], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    RMSE_EXTRA=comp_RMSE_tail(dat_tot[6], dat_tot[7], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    RMSE_ARC=comp_RMSE_tail(dat_tot[8], dat_tot[9], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    RMSE_ANT=comp_RMSE_tail(dat_tot[10], dat_tot[11], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    
    
    RMSE_EU=comp_RMSE_tail(dat_tot[12], dat_tot[13], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    RMSE_NAM=comp_RMSE_tail(dat_tot[14], dat_tot[15], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    RMSE_NAT=comp_RMSE_tail(dat_tot[16], dat_tot[17], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    RMSE_NAP=comp_RMSE_tail(dat_tot[18], dat_tot[19], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    RMSE_EA=comp_RMSE_tail(dat_tot[20], dat_tot[21], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    RMSE_ANZ=comp_RMSE_tail(dat_tot[22], dat_tot[23], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    
    RMSE=comp_RMSE_tail(dat_tot[24], dat_tot[25], operational_comp=operational_comp, greater=greater, HRES_ground=HRES_ground,quant=quant)
    
    RMSE=np.array([RMSE_NH, RMSE_SH,RMSE_tropics,RMSE_EXTRA,RMSE_ARC,RMSE_ANT,
                RMSE_EU,RMSE_NAM,RMSE_NAT,RMSE_NAP,RMSE_EA,RMSE_ANZ, RMSE])
    
    if operational_comp==True:
    
        RMSE= pd.DataFrame(RMSE, columns=['HRES', 'Pangu','Graphcast'], index=['Northern Hemisphere', 'Southern Hemisphere', 'Tropics', 'Extra-Tropics', 'Arctic', 'Antarctic', 
                                                                              'Europe', 'North America', 'North Atlantic', 'North Pacific', 'East Asia', 'AusNZ', 'Global'])
    else:
        RMSE= pd.DataFrame(RMSE, columns=['HRES', 'Pangu','Fuxi','Graphcast'], index=['Northern Hemisphere', 'Southern Hemisphere', 'Tropics', 'Extra-Tropics', 'Arctic', 'Antarctic', 
                                                                                  'Europe', 'North America', 'North Atlantic', 'North Pacific', 'East Asia', 'AusNZ', 'Global'])
        
    return(RMSE)

#%% Plots


def plot_tile_depth (var_1, var_3, var_5, var_7, var_10, region, operational_comp=True, text_size_table=30, text_size_axis=28, abbreviation=True):
    if abbreviation==True:
       d = {'1 d': (var_1.loc[region]).values.squeeze(), '3 d': (var_3.loc[region]).values.squeeze() , '5 d': (var_5.loc[region]).values.squeeze(),
             '7 d': (var_7.loc[region]).values.squeeze(), '10 d': (var_10.loc[region]).values.squeeze()}
    else:
           
       d = {'1 day': (var_1.loc[region]).values.squeeze(), '3 days': (var_3.loc[region]).values.squeeze() , '5 days': (var_5.loc[region]).values.squeeze(),
         '7 days': (var_7.loc[region]).values.squeeze(), '10 days': (var_10.loc[region]).values.squeeze()}
       
    df = pd.DataFrame(data=d)
    
    if operational_comp==True:
        df.index = ['HRES', 'Pangu', 'Graphcast']
    else:
        df.index = ['HRES', 'Pangu', 'Fuxi','Graphcast']
    
    diff=(df-(df[0:1].values.squeeze()))/(df[0:1].values.squeeze())*100
    
    diff=diff.melt()
    
    df=((df.reset_index()).melt(id_vars='index'))
    
    df=df.rename(columns={"index":"Model", "variable":"Days", "value":"RMSE"})
    
    df['Difference']=diff['value']
    
    df['RMSE']=round(df['RMSE'], ndigits=2)
    
    if (operational_comp==True):
        df['Model']=(df['Model'].astype('category')).cat.reorder_categories(['Pangu', 'Graphcast', 'HRES'])
    else: 
        df['Model']=(df['Model'].astype('category')).cat.reorder_categories(['Fuxi','Pangu', 'Graphcast', 'HRES'])
        
    if abbreviation==True:
        df['Days']=(df['Days'].astype('category')).cat.reorder_categories(['1 d', '3 d', '5 d' , '7 d', '10 d'])
    else:
        df['Days']=(df['Days'].astype('category')).cat.reorder_categories(['1 day', '3 days', '5 days' , '7 days', '10 days'])
    
    pl=ggplot(df, aes(x='Days',y='Model',fill='Difference'))+\
        geom_tile(aes(width=0.9, height=0.9),color='white',size=4)+\
        geom_text(aes(label='RMSE'), color='black', size=text_size_table)+\
        scale_fill_gradientn(colors=["#0B559F","#2B7BBA","#539ECD","#89BEDC", "#BAD6EB", "#DBE9F6", "#FFFFFF", "#FEDBCC", "#FCAF93", "#FC8161", "#F14E38", "#BD1E1D", "#A91016"],
                             values=[0, 0.25,0.4167,0.4583,0.483,0.4916,0.50,0.5087,0.5117,0.5417,0.5833,0.75,1], breaks=[-60,-30, -10, 0, 10, 30, 60], limits=[-60,60], 
                             name="% difference in RMSE vs IFS HRES"
    )+\
        theme_minimal()+\
        theme(plot_background=element_rect(fill='white'),
              text=element_text(family='Verdana'),
              axis_text=element_text(size=text_size_axis),
              axis_title=element_text(size=32, face='bold'),
              title=element_text(size=44, face='bold', hjust=0),
              legend_title=element_text(size=34, face='bold'),
              legend_text=element_text(size=28),
              legend_key_width=20,
              legend_key_height=150,
              legend_position='bottom')
        
    return(pl)
#scale_fill_gradient2(low='#769fca',high='#ff6c65', limits =[-60,60], breaks=[-60,-30,0,30,60], name="% difference in RMSE vs IFS HRES")+\
def tile_depth_all(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, title_gl, operational_comp=True):


    pl_nh=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Northern Hemisphere', operational_comp=operational_comp)+
    labs(x= '', y='Northern Hemisphere')+theme(legend_position='none'))
    pl_sh=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Southern Hemisphere', operational_comp=operational_comp)+
    labs(x= '', y='Southern Hemisphere')+theme(legend_position='none'))
    pl_tr=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Tropics', operational_comp=operational_comp)+
    labs(x= '', y='Tropics')+theme(legend_position='none'))
    pl_ex=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Extra-Tropics', operational_comp=operational_comp)+
    labs(x= '', y='Extra-Tropics')+theme(legend_position='none'))
    pl_ar=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Arctic', operational_comp=operational_comp)+
    labs(x= '', y='Arcitc')+theme(legend_position='none'))
    pl_an=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Antarctic', operational_comp=operational_comp)+
    labs(x= '', y='Antarctic')+theme(legend_position='none'))
    pl_eu=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Europe', operational_comp=operational_comp)+
    labs(x= '', y='Europe')+theme(legend_position='none'))
    pl_nam=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='North America', operational_comp=operational_comp)+
    labs(x= '', y='North America')+theme(legend_position='none'))
    pl_nat=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='North Atlantic', operational_comp=operational_comp)+
    labs(x= '', y='North Atlantic')+theme(legend_position='none'))
    pl_np=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='North Pacific', operational_comp=operational_comp)+
    labs(x= '', y='North Pacific')+theme(legend_position='none'))
    pl_ea=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='East Asia', operational_comp=operational_comp)+
    labs(x= '', y='East Asia')+theme(legend_position='none'))
    pl_au=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='AusNZ', operational_comp=operational_comp)+
    labs(x= '', y='AusNZ')+theme(legend_position='none'))
    pl_gl=pw.load_ggplot(plot_tile_depth(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, region='Global', operational_comp=operational_comp, text_size_table=40, text_size_axis=30, abbreviation=False)+
    labs(x= '', y='Global', title=title_gl ))
    
    a=(pl_gl/(pl_nh|pl_sh)/(pl_tr|pl_ex)/(pl_ar|pl_an)/(pl_eu|pl_nam)/(pl_nat|pl_np)/(pl_ea|pl_au))


    return(a)


def tile_comp_plot(RMSE_day_1, RMSE_day_3, RMSE_day_5, RMSE_day_7, RMSE_day_10, operational_comp=True):

    a=pd.melt((RMSE_day_1.transpose()).reset_index(), id_vars='index')
    
    ids=a.groupby('variable', sort=False)['value'].idxmin()
    
    RMSE_1_95=(a.iloc[ids]).rename(columns = {'index':'Model', 'variable':'Region', 'value': 'Value'}) 
    RMSE_1_95['Day_quant']="1 day"
    
    a=pd.melt((RMSE_day_3.transpose()).reset_index(), id_vars='index')
    
    ids=a.groupby('variable', sort=False)['value'].idxmin()
    
    RMSE_3_95=(a.iloc[ids]).rename(columns = {'index':'Model', 'variable':'Region', 'value': 'Value'}) 
    RMSE_3_95['Day_quant']="3 days"
    
    
    a=pd.melt((RMSE_day_5.transpose()).reset_index(), id_vars='index')
    
    ids=a.groupby('variable', sort=False)['value'].idxmin()
    
    RMSE_5_95=(a.iloc[ids]).rename(columns = {'index':'Model', 'variable':'Region', 'value': 'Value'}) 
    RMSE_5_95['Day_quant']="5 days"
    
    a=pd.melt((RMSE_day_7.transpose()).reset_index(), id_vars='index')
    
    ids=a.groupby('variable', sort=False)['value'].idxmin()
    
    RMSE_7_95=(a.iloc[ids]).rename(columns = {'index':'Model', 'variable':'Region', 'value': 'Value'}) 
    RMSE_7_95['Day_quant']="7 days"
    
    a=pd.melt((RMSE_day_10.transpose()).reset_index(), id_vars='index')
    
    ids=a.groupby('variable', sort=False)['value'].idxmin()
    
    RMSE_10_95=(a.iloc[ids]).rename(columns = {'index':'Model', 'variable':'Region', 'value': 'Value'}) 
    RMSE_10_95['Day_quant']="10 days"
    
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
    
    
    model_colors = {'HRES': '#DDDDDD', 'Pangu': '#77AADD', 'Fuxi': '#99DDFF', 'Graphcast':'#EE8866'}
    
    pl=ggplot(tr, aes(x='Day_quant',y='Region',fill='Model'))+\
        geom_tile(aes(width=0.9, height=0.9),color='white')+\
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



def RMSE_tail_plot(dat, dat_mem, quant=0.95, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False, title_pl="",guide_true=False):
    
    
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
    
    threshold_theoretical=dat[0].chunk(dict(time=-1)).quantile(quant,dim='time').values.flatten()

    threshold_theoretical=np.tile(threshold_theoretical, len(dat[0].time))
    
    lat=np.tile(dat[0].latitude, len(dat[0].longitude)*len(dat[0].time))
    lon=np.tile(np.repeat(dat[0].longitude, len(dat[0].latitude)),len(dat[0].time))


    if fixed_number==True:

        ind = np.where(theoretical==threshold_theoretical)
        arr_ind= theoretical[ind]
        un_ind=np.unique(arr_ind, return_index=True)[1]
        inde=np.delete(ind,un_ind)
        theoretical=np.delete(theoretical,inde)
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
         
    
    n_days=round(len(pangu_variable_quant)/(len(dat[0].latitude)*len(dat[0].longitude)))
    

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
    
    #return sq_diff_HRES
#sq_diff_pangu, sq_diff_fuxi, sq_diff_graphcast, n_days,len(variable_quant),len(dat[0].latitude),len(dat[0].longitude)
    if operational_comp==False:  
        dat_tot = pd.DataFrame({
        
        'Latitude': np.tile(lat,num_pred_models),
        'Longitude': np.tile(lon,num_pred_models),
        'Predicted': np.concatenate([sq_diff_HRES, sq_diff_pangu, sq_diff_fuxi, sq_diff_graphcast]),
        'Model': np.repeat(['HRES', 'Pangu', 'Fuxi','Graphcast'], len(variable_quant))
        
    })
    else:
        dat_tot = pd.DataFrame({
        
        'Latitude': np.tile(lat,num_pred_models),
        'Longitude': np.tile(lon,num_pred_models),
        'Predicted': np.concatenate([sq_diff_HRES, sq_diff_pangu, sq_diff_graphcast]),
        'Model': np.repeat(['HRES', 'Pangu', 'Graphcast'], len(variable_quant))
        
    })
            
    dat_tot['Longitude']=np.where(dat_tot['Longitude']>180,dat_tot['Longitude']-360,dat_tot['Longitude'])
    #return(dat_tot)
    RMSE_point=(dat_tot.groupby(['Latitude', 'Longitude', 'Model'])['Predicted'].sum()/(len(dat[0].latitude)*len(dat[0].longitude)))**(1/2)
    RMSE_point=RMSE_point.reset_index()
    idx_min = RMSE_point.groupby(['Latitude', 'Longitude'])['Predicted'].idxmin()

    # Use the indices to extract the corresponding model names
    RMSE_point_min = RMSE_point.loc[idx_min, ['Latitude', 'Longitude', 'Model', 'Predicted']]
    
    
    model_colors = {'HRES': '#DDDDDD', 'Pangu': '#77AADD', 'Fuxi': '#99DDFF', 'Graphcast':'#EE8866'}

    #model_colors = {'HRES': '#CCCCCC', 'Pangu': '#6b8ea4', 'Fuxi': '#99DDFF', 'Graphcast':'#e48646'}


    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    if guide_true==True:
    
       RMSE_base_plot_world=pw.load_ggplot((
        ggplot()
        + expand_limits(x=0, y=0)
        + theme_void()
        +theme_bw()+
        geom_tile(RMSE_point_min,aes(x='Longitude',y='Latitude',fill='Model'))+
        geom_map(world,  color='black', fill='white',alpha=0)+
        scale_fill_manual(values= model_colors)+
        scale_x_continuous(expand=(0,0))+
        scale_y_continuous(expand=(0,0))+
        #coord_fixed(1.5)+
        labs(x='',y='', title=title_pl)+
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
         geom_tile(RMSE_point_min,aes(x='Longitude',y='Latitude',fill='Model'))+
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
             
  

    model_colors = {'HRES': '#222222', 'Pangu': 'darkblue', 'Fuxi': 'lightblue', 'Graphcast':'red'}
    #model_colors = {'HRES': '#222222', 'Pangu': '#77AADD', 'Fuxi': '#99DDFF', 'Graphcast':'#EE8866'}

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
         
        #model_colors = {'HRES': 'black', 'Pangu': 'darkblue', 'Graphcast':'red'}
    
    # Plot the QQ plot using plotnine
    
    if guide_true==True:
        
        plot_extr=(
            ggplot(qqplot_data, aes(x='True', y='Predicted', color='Model')) +
            geom_abline(intercept=0, slope=1, linetype='dashed', color='black') +
            geom_point() +
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
            geom_point() +
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

