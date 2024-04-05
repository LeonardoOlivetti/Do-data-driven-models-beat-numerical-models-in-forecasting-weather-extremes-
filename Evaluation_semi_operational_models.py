# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 17:02:44 2024

@author: leool650
"""
#%% Import functions

#exec(open(r'functions.py').read())


#%% Modules and open zarr

#from scipy.io import netcdf
import numpy as np
import sys
import xarray as xr


# Define variables and time-range


variables_s = ['2m_temperature','10m_wind_speed']


#%% ERA5

ERA5=xr.open_zarr('gs://weatherbench2/datasets/era5/1959-2023_01_10-6h-240x121_equiangular_with_poles_conservative.zarr')

#Keep only midnight 

ERA5 = ERA5.where(np.logical_or(ERA5['time.hour'] == 00, ERA5['time.hour'] == 12), drop=True)

#print(ERA5)

temp_2m = ERA5[variables_s[0]]
wind_speed = ERA5[variables_s[1]]

#Cosine weights
cos_weights=np.cos(np.deg2rad(ERA5.latitude))
cos_weights=np.tile(cos_weights/np.mean(cos_weights), len(ERA5.time)*len(ERA5.longitude))

#%% IFS HRES truth

HRES_truth=xr.open_zarr('gs://weatherbench2/datasets/hres/2016-2022-0012-240x121_equiangular_with_poles_conservative.zarr', chunks= {'time':8})

HRES_truth = HRES_truth.where(np.logical_or(HRES_truth['time.hour'] == 00, HRES_truth['time.hour'] == 12), drop=True)

HRES_truth = HRES_truth.isel(prediction_timedelta = 0)

HRES_truth_temp_2m = HRES_truth[variables_s[0]]
HRES_truth_wind_speed = HRES_truth[variables_s[1]]

#%% IFS HRES prediction

midnights=list(range(4,41,4))

start = '2020-01-01 00:00:00'
end = '2020-12-16 12:00:00'
#zarr open

HRES=xr.open_zarr('gs://weatherbench2/datasets/hres/2016-2022-0012-240x121_equiangular_with_poles_conservative.zarr', chunks= {'time':8})

HRES = HRES[variables_s].sel( time=slice(start,end))

#Keep only midnight 

HRES = HRES.isel(prediction_timedelta = midnights)
HRES = HRES.where(np.logical_or(HRES['time.hour'] == 00, HRES['time.hour'] == 12), drop=True)


HRES_wind_speed = HRES[variables_s[1]]
HRES_temp_2m = HRES[variables_s[0]]

#%% Pangu operational

midnights=list(range(3,41,4))

#zarr open
pangu_oper=xr.open_zarr('gs://weatherbench2/datasets/pangu_hres_init/2020_0012_240x121_equiangular_with_poles_conservative.zarr', chunks= {'time':8})

# check zarr content
#print(pangu)

#ds.chunksizes

pangu_oper = pangu_oper[variables_s].sel( time=slice(start,end))

#Keep only midnight and noon

pangu_oper = pangu_oper.isel(prediction_timedelta = midnights) 
pangu_oper = pangu_oper.where(np.logical_or(pangu_oper['time.hour'] == 00, pangu_oper['time.hour'] == 12), drop=True)

pangu_wind_speed_oper = pangu_oper[variables_s[1]]
pangu_temp_2m_oper = pangu_oper[variables_s[0]]


#%% graphcast operational

midnights=list(range(3,41,4))

graphcast_oper=xr.open_zarr('gs://weatherbench2/datasets/graphcast_hres_init/2020/date_range_2019-11-16_2021-02-01_12_hours-240x121_equiangular_with_poles_conservative.zarr', chunks= {'time':8})

#print(graphcast_oper)

graphcast_oper = graphcast_oper[variables_s].sel( time=slice(start,end))

#Keep only midnight and noon

graphcast_oper = graphcast_oper.isel(prediction_timedelta = midnights) 
graphcast_oper = graphcast_oper.where(np.logical_or(graphcast_oper['time.hour'] == 00, graphcast_oper['time.hour'] == 12), drop=True)

graphcast_wind_speed_oper = graphcast_oper[variables_s[1]]
graphcast_temp_2m_oper = graphcast_oper[variables_s[0]]

#%% Data import

dat_temp_1=prep_all(temp_2m, HRES_truth_temp_2m, HRES_temp_2m, pangu_temp_2m_oper, graphcast_temp_2m_oper,days_ahead=1)
dat_temp_3=prep_all(temp_2m, HRES_truth_temp_2m, HRES_temp_2m, pangu_temp_2m_oper, graphcast_temp_2m_oper,days_ahead=3)
dat_temp_5=prep_all(temp_2m, HRES_truth_temp_2m, HRES_temp_2m, pangu_temp_2m_oper, graphcast_temp_2m_oper,days_ahead=5)
dat_temp_7=prep_all(temp_2m, HRES_truth_temp_2m, HRES_temp_2m, pangu_temp_2m_oper, graphcast_temp_2m_oper,days_ahead=7)
dat_temp_10=prep_all(temp_2m, HRES_truth_temp_2m, HRES_temp_2m, pangu_temp_2m_oper, graphcast_temp_2m_oper,days_ahead=10)

 
dat_wind_1=prep_all(wind_speed, HRES_truth_wind_speed, HRES_wind_speed, pangu_wind_speed_oper, graphcast_wind_speed_oper,days_ahead=1)
dat_wind_3=prep_all(wind_speed, HRES_truth_wind_speed, HRES_wind_speed, pangu_wind_speed_oper, graphcast_wind_speed_oper,days_ahead=3)
dat_wind_5=prep_all(wind_speed, HRES_truth_wind_speed, HRES_wind_speed, pangu_wind_speed_oper, graphcast_wind_speed_oper,days_ahead=5)
dat_wind_7=prep_all(wind_speed, HRES_truth_wind_speed, HRES_wind_speed, pangu_wind_speed_oper, graphcast_wind_speed_oper,days_ahead=7)
dat_wind_10=prep_all(wind_speed, HRES_truth_wind_speed, HRES_wind_speed, pangu_wind_speed_oper, graphcast_wind_speed_oper,days_ahead=10)


#%% RMSE computation


RMSE_temp_1_01_oper=RMSE_all(dat_temp_1, operational_comp=True, quant=0.01, greater=False)
RMSE_temp_3_01_oper=RMSE_all(dat_temp_3, operational_comp=True, quant=0.01, greater=False)
RMSE_temp_5_01_oper=RMSE_all(dat_temp_5, operational_comp=True, quant=0.01, greater=False)
RMSE_temp_7_01_oper=RMSE_all(dat_temp_7, operational_comp=True, quant=0.01, greater=False)
RMSE_temp_10_01_oper=RMSE_all(dat_temp_10, operational_comp=True, quant=0.01, greater=False)

RMSE_temp_1_05_oper=RMSE_all(dat_temp_1, operational_comp=True, quant=0.05, greater=False)
RMSE_temp_3_05_oper=RMSE_all(dat_temp_3, operational_comp=True, quant=0.05, greater=False)
RMSE_temp_5_05_oper=RMSE_all(dat_temp_5, operational_comp=True, quant=0.05, greater=False)
RMSE_temp_7_05_oper=RMSE_all(dat_temp_7, operational_comp=True, quant=0.05, greater=False)
RMSE_temp_10_05_oper=RMSE_all(dat_temp_10, operational_comp=True, quant=0.05, greater=False)

RMSE_temp_1_00_oper=RMSE_all(dat_temp_1, operational_comp=True, greater=True)
RMSE_temp_3_00_oper=RMSE_all(dat_temp_3, operational_comp=True, greater=True)
RMSE_temp_5_00_oper=RMSE_all(dat_temp_5, operational_comp=True, greater=True)
RMSE_temp_7_00_oper=RMSE_all(dat_temp_7, operational_comp=True, greater=True)
RMSE_temp_10_00_oper=RMSE_all(dat_temp_10, operational_comp=True, greater=True)

RMSE_temp_1_95_oper=RMSE_all(dat_temp_1, operational_comp=True, quant=0.95, greater=True)
RMSE_temp_3_95_oper=RMSE_all(dat_temp_3, operational_comp=True, quant=0.95, greater=True)
RMSE_temp_5_95_oper=RMSE_all(dat_temp_5, operational_comp=True, quant=0.95, greater=True)
RMSE_temp_7_95_oper=RMSE_all(dat_temp_7, operational_comp=True, quant=0.95, greater=True)
RMSE_temp_10_95_oper=RMSE_all(dat_temp_10, operational_comp=True, quant=0.95, greater=True)

RMSE_temp_1_99_oper=RMSE_all(dat_temp_1, operational_comp=True, quant=0.99, greater=True)
RMSE_temp_3_99_oper=RMSE_all(dat_temp_3, operational_comp=True, quant=0.99, greater=True)
RMSE_temp_5_99_oper=RMSE_all(dat_temp_5, operational_comp=True, quant=0.99, greater=True)
RMSE_temp_7_99_oper=RMSE_all(dat_temp_7, operational_comp=True, quant=0.99, greater=True)
RMSE_temp_10_99_oper=RMSE_all(dat_temp_10, operational_comp=True, quant=0.99, greater=True)

RMSE_wind_1_00_oper=RMSE_all(dat_wind_1, operational_comp=True, greater=True)
RMSE_wind_3_00_oper=RMSE_all(dat_wind_3, operational_comp=True, greater=True)
RMSE_wind_5_00_oper=RMSE_all(dat_wind_5, operational_comp=True, greater=True)
RMSE_wind_7_00_oper=RMSE_all(dat_wind_7, operational_comp=True, greater=True)
RMSE_wind_10_00_oper=RMSE_all(dat_wind_10, operational_comp=True, greater=True)

RMSE_wind_1_95_oper=RMSE_all(dat_wind_1, operational_comp=True, quant=0.95, greater=True)
RMSE_wind_3_95_oper=RMSE_all(dat_wind_3, operational_comp=True, quant=0.95, greater=True)
RMSE_wind_5_95_oper=RMSE_all(dat_wind_5, operational_comp=True, quant=0.95, greater=True)
RMSE_wind_7_95_oper=RMSE_all(dat_wind_7, operational_comp=True, quant=0.95, greater=True)
RMSE_wind_10_95_oper=RMSE_all(dat_wind_10, operational_comp=True, quant=0.95, greater=True)

RMSE_wind_1_99_oper=RMSE_all(dat_wind_1, operational_comp=True, quant=0.99, greater=True)
RMSE_wind_3_99_oper=RMSE_all(dat_wind_3, operational_comp=True, quant=0.99, greater=True)
RMSE_wind_5_99_oper=RMSE_all(dat_wind_5, operational_comp=True, quant=0.99, greater=True)
RMSE_wind_7_99_oper=RMSE_all(dat_wind_7, operational_comp=True, quant=0.99, greater=True)
RMSE_wind_10_99_oper=RMSE_all(dat_wind_10, operational_comp=True, quant=0.99, greater=True)



#%% Plots

# Fig. 1-3

tile_depth_temp_01=tile_depth_all(RMSE_temp_1_01_oper, RMSE_temp_3_01_oper, RMSE_temp_5_01_oper, RMSE_temp_7_01_oper, RMSE_temp_10_01_oper, "Cold extremes")
tile_depth_temp_99=tile_depth_all(RMSE_temp_1_99_oper, RMSE_temp_3_99_oper, RMSE_temp_5_99_oper, RMSE_temp_7_99_oper, RMSE_temp_10_99_oper, "Hot extremes")
tile_depth_wind_99=tile_depth_all(RMSE_wind_1_99_oper, RMSE_wind_3_99_oper, RMSE_wind_5_99_oper, RMSE_wind_7_99_oper, RMSE_wind_10_99_oper, "Wind extremes")

tile_depth_temp_01.set_index("a", fontsize=50)
tile_depth_temp_99.set_index("b", fontsize=50)
tile_depth_wind_99.set_index("c", fontsize=50)

(tile_depth_temp_01|tile_depth_temp_99|tile_depth_wind_99).savefig(r'C:\Users\leool650\OneDrive - Uppsala universitet\Desktop\Alvex_py\Model_comparison\fig\tile_depth_1.pdf', format='pdf')


tile_depth_temp_05=tile_depth_all(RMSE_temp_1_05_oper, RMSE_temp_3_05_oper, RMSE_temp_5_05_oper, RMSE_temp_7_05_oper, RMSE_temp_10_05_oper, "Cold extremes")
tile_depth_temp_95=tile_depth_all(RMSE_temp_1_95_oper, RMSE_temp_3_95_oper, RMSE_temp_5_95_oper, RMSE_temp_7_95_oper, RMSE_temp_10_95_oper, "Warm extremes")
tile_depth_wind_95=tile_depth_all(RMSE_wind_1_95_oper, RMSE_wind_3_95_oper, RMSE_wind_5_95_oper, RMSE_wind_7_95_oper, RMSE_wind_10_95_oper, "Wind extremes")

tile_depth_temp_05.set_index("a", fontsize=50)
tile_depth_temp_95.set_index("b", fontsize=50)
tile_depth_wind_95.set_index("c", fontsize=50)
(tile_depth_temp_05|tile_depth_temp_95|tile_depth_wind_95).savefig(r'C:\Users\leool650\OneDrive - Uppsala universitet\Desktop\Alvex_py\Model_comparison\fig\tile_depth_5.pdf', format='pdf')


tile_depth_temp_00=tile_depth_all(RMSE_temp_1_00_oper, RMSE_temp_3_00_oper, RMSE_temp_5_00_oper, RMSE_temp_7_00_oper, RMSE_temp_10_00_oper, "2m temperature")
tile_depth_wind_00=tile_depth_all(RMSE_wind_1_00_oper, RMSE_wind_3_00_oper, RMSE_wind_5_00_oper, RMSE_wind_7_00_oper, RMSE_wind_10_00_oper, "10m windspeed")

tile_depth_temp_00.set_index("a", fontsize=50)
tile_depth_wind_00.set_index("b", fontsize=50)
(tile_depth_temp_00|tile_depth_wind_00).savefig(r'C:\Users\leool650\OneDrive - Uppsala universitet\Desktop\Alvex_py\Model_comparison\fig\tile_depth_all.pdf', format='pdf')


# Fig. 4

model_colors = {'HRES': '#DDDDDD', 'Pangu': '#77AADD', 'Fuxi': '#99DDFF', 'Graphcast':'#EE8866'}

#Tile figure
RMSE_tile_temp_05=pw.load_ggplot(tile_comp_plot(RMSE_temp_1_05_oper,RMSE_temp_3_05_oper,RMSE_temp_5_05_oper,RMSE_temp_7_05_oper,RMSE_temp_10_05_oper)+\
    ggtitle("Cold extremes 5%")+\
    scale_fill_manual(values=model_colors, guide=False))
    
RMSE_tile_temp_01=pw.load_ggplot(tile_comp_plot(RMSE_temp_1_01_oper,RMSE_temp_3_01_oper,RMSE_temp_5_01_oper,RMSE_temp_7_01_oper,RMSE_temp_10_01_oper)+\
    ggtitle("Cold extremes 1%")+\
    scale_fill_manual(values=model_colors, guide=False))
    
RMSE_tile_temp_global=pw.load_ggplot(tile_comp_plot(RMSE_temp_1_00_oper,RMSE_temp_3_00_oper,RMSE_temp_5_00_oper,RMSE_temp_7_00_oper,RMSE_temp_10_00_oper)+\
    ggtitle("2m temperature: all observations"))
    
RMSE_tile_temp_95=pw.load_ggplot(tile_comp_plot(RMSE_temp_1_95_oper,RMSE_temp_3_95_oper,RMSE_temp_5_95_oper,RMSE_temp_7_95_oper,RMSE_temp_10_95_oper)+\
    ggtitle("Hot extremes 5%")+\
    scale_fill_manual(values=model_colors, guide=False))
    
RMSE_tile_temp_99=pw.load_ggplot(tile_comp_plot(RMSE_temp_1_99_oper,RMSE_temp_3_99_oper,RMSE_temp_5_99_oper,RMSE_temp_7_99_oper,RMSE_temp_10_99_oper)+\
    ggtitle("Hot extremes 1%")+\
    scale_fill_manual(values=model_colors, guide=False))
    
RMSE_tile_wind_global=pw.load_ggplot(tile_comp_plot(RMSE_wind_1_00_oper,RMSE_wind_3_00_oper,RMSE_wind_5_00_oper,RMSE_wind_7_00_oper,RMSE_wind_10_00_oper)+\
    ggtitle("10m windspeed: all observations"))
    
RMSE_tile_wind_95=pw.load_ggplot(tile_comp_plot(RMSE_wind_1_95_oper,RMSE_wind_3_95_oper,RMSE_wind_5_95_oper,RMSE_wind_7_95_oper,RMSE_wind_10_95_oper)+\
    ggtitle("Windspeed extremes 5%")+\
    scale_fill_manual(values=model_colors, guide=False))
    
RMSE_tile_wind_99=pw.load_ggplot(tile_comp_plot(RMSE_wind_1_99_oper,RMSE_wind_3_99_oper,RMSE_wind_5_99_oper,RMSE_wind_7_99_oper,RMSE_wind_10_99_oper)+\
    ggtitle("Windspeed extremes 1%")+\
    scale_fill_manual(values=model_colors, guide=False))
    
RMSE_tile_temp_05.set_index("a", fontsize=30)
RMSE_tile_temp_01.set_index("d", fontsize=30)
RMSE_tile_temp_global.set_index("g", fontsize=30)
RMSE_tile_temp_95.set_index("b", fontsize=30)
RMSE_tile_temp_99.set_index("e", fontsize=30) 
RMSE_tile_wind_global.set_index("h", fontsize=30)  
RMSE_tile_wind_95.set_index("c", fontsize=30)  
RMSE_tile_wind_99.set_index("f", fontsize=30)    

((RMSE_tile_temp_05|RMSE_tile_temp_95|RMSE_tile_wind_95)/(RMSE_tile_temp_01|RMSE_tile_temp_99|RMSE_tile_wind_99)/(RMSE_tile_temp_global|RMSE_tile_wind_global)).savefig(r'C:\Users\leool650\OneDrive - Uppsala universitet\Desktop\Alvex_py\Model_comparison\fig\tile_tot.pdf', format='pdf')



# Fig.5
qq_co_01=pw.load_ggplot((qqplot_extreme(dat_temp_1[25] ,quant=0.1, greater=False, operational_comp=True)+labs(title=" ")))
qq_co_03=pw.load_ggplot((qqplot_extreme(dat_temp_3[25] ,quant=0.1, greater=False, operational_comp=True)+labs(title=" ")))
qq_co_05=pw.load_ggplot((qqplot_extreme(dat_temp_5[25] ,quant=0.1, greater=False, operational_comp=True)+labs(title=" ")))
qq_co_07=pw.load_ggplot((qqplot_extreme(dat_temp_7[25] ,quant=0.1, greater=False, operational_comp=True)+labs(title=" ")))
qq_co_10=pw.load_ggplot((qqplot_extreme(dat_temp_10[25] ,quant=0.1, greater=False, operational_comp=True)+labs(title=" ")))

qq_wa_01=pw.load_ggplot((qqplot_extreme(dat_temp_1[25] ,quant=0.9, greater=True, operational_comp=True)+labs(title=" ")))
qq_wa_03=pw.load_ggplot((qqplot_extreme(dat_temp_3[25] ,quant=0.9, greater=True, operational_comp=True)+labs(title=" ")))
qq_wa_05=pw.load_ggplot((qqplot_extreme(dat_temp_5[25] ,quant=0.9, greater=True, operational_comp=True)+labs(title=" ")))
qq_wa_07=pw.load_ggplot((qqplot_extreme(dat_temp_7[25] ,quant=0.9, greater=True, operational_comp=True)+labs(title=" ")))
qq_wa_10=pw.load_ggplot((qqplot_extreme(dat_temp_10[25] ,quant=0.9, greater=True, operational_comp=True)+labs(title=" ")))

qq_wi_01=pw.load_ggplot((qqplot_extreme(dat_wind_1[25] ,quant=0.9, greater=True, operational_comp=True, guide_true=True)+labs(title=" ")))
qq_wi_03=pw.load_ggplot((qqplot_extreme(dat_wind_3[25] ,quant=0.9, greater=True, operational_comp=True, guide_true=True)+labs(title=" ")))
qq_wi_05=pw.load_ggplot((qqplot_extreme(dat_wind_5[25] ,quant=0.9, greater=True, operational_comp=True, guide_true=True)+labs(title=" ")))
qq_wi_07=pw.load_ggplot((qqplot_extreme(dat_wind_7[25] ,quant=0.9, greater=True, operational_comp=True, guide_true=True)+labs(title=" ")))
qq_wi_10=pw.load_ggplot((qqplot_extreme(dat_wind_10[25] ,quant=0.9, greater=True, operational_comp=True, guide_true=True)+labs(title=" ")))


qq_co_01.set_index("a1", fontsize=30)
qq_co_03.set_index("a2", fontsize=30)
qq_co_05.set_index("a3", fontsize=30)
qq_co_07.set_index("a4", fontsize=30)
qq_co_10.set_index("a5", fontsize=30)

qq_wa_01.set_index("b1", fontsize=30)
qq_wa_03.set_index("b2", fontsize=30)
qq_wa_05.set_index("b3", fontsize=30)
qq_wa_07.set_index("b4", fontsize=30)
qq_wa_10.set_index("b5", fontsize=30)

qq_wi_01.set_index("c1", fontsize=30)
qq_wi_03.set_index("c2", fontsize=30)
qq_wi_05.set_index("c3", fontsize=30)
qq_wi_07.set_index("c4", fontsize=30)
qq_wi_10.set_index("c5", fontsize=30)

qq_co=qq_co_01/qq_co_03/qq_co_05/qq_co_07/qq_co_10
qq_wa=qq_wa_01/qq_wa_03/qq_wa_05/qq_wa_07/qq_wa_10
qq_wi=qq_wi_01/qq_wi_03/qq_wi_05/qq_wi_07/qq_wi_10

qq_co.set_suptitle("Cold extremes", size=32, fontweight='bold')
qq_wa.set_suptitle("Hot extremes", size=32, fontweight='bold')
qq_wi.set_suptitle("Windspeed extremes", size=32, fontweight='bold')

qq_world=(qq_co|qq_wa|qq_wi)

qq_world.savefig()


# Fig.6-8

qqplot_all(dat_temp_5, quant=0.1, greater=False, temperature=True).savefig()
qqplot_all(dat_temp_5, quant=0.9, greater=True, temperature=True).savefig()
qqplot_all(dat_wind_5, quant=0.9, greater=True, temperature=False).savefig()




# Fig.9-10


pl_te_1_00=RMSE_tail_plot(dat_temp_1[24], dat_temp_1[25], quant=0.00, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_co_1_05=RMSE_tail_plot(dat_temp_1[24], dat_temp_1[25], quant=0.05, greater=False, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_wa_1_95=RMSE_tail_plot(dat_temp_1[24], dat_temp_1[25], quant=0.95, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_wi_1_00=RMSE_tail_plot(dat_wind_1[24], dat_wind_1[25], quant=0.00, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False, guide_true=True)
pl_wi_1_95=RMSE_tail_plot(dat_wind_1[24], dat_wind_1[25], quant=0.95, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False, guide_true=True)

    
pl_te_3_00=RMSE_tail_plot(dat_temp_3[24], dat_temp_3[25], quant=0.00, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_co_3_05=RMSE_tail_plot(dat_temp_3[24], dat_temp_3[25], quant=0.05, greater=False, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_wa_3_95=RMSE_tail_plot(dat_temp_3[24], dat_temp_3[25], quant=0.95, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_wi_3_00=RMSE_tail_plot(dat_wind_3[24], dat_wind_3[25], quant=0.00, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False, guide_true=True)
pl_wi_3_95=RMSE_tail_plot(dat_wind_3[24], dat_wind_3[25], quant=0.95, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False, guide_true=True)

    
pl_te_5_00=RMSE_tail_plot(dat_temp_5[24], dat_temp_5[25], quant=0.00, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_co_5_05=RMSE_tail_plot(dat_temp_5[24], dat_temp_5[25], quant=0.05, greater=False, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_wa_5_95=RMSE_tail_plot(dat_temp_5[24], dat_temp_5[25], quant=0.95, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_wi_5_00=RMSE_tail_plot(dat_wind_5[24], dat_wind_5[25], quant=0.00, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False, guide_true=True)
pl_wi_5_95=RMSE_tail_plot(dat_wind_5[24], dat_wind_5[25], quant=0.95, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False, guide_true=True)

    
pl_te_7_00=RMSE_tail_plot(dat_temp_7[24], dat_temp_7[25], quant=0.00, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_co_7_05=RMSE_tail_plot(dat_temp_7[24], dat_temp_7[25], quant=0.05, greater=False, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_wa_7_95=RMSE_tail_plot(dat_temp_7[24], dat_temp_7[25], quant=0.95, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_wi_7_00=RMSE_tail_plot(dat_wind_7[24], dat_wind_7[25], quant=0.00, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False, guide_true=True)
pl_wi_7_95=RMSE_tail_plot(dat_wind_7[24], dat_wind_7[25], quant=0.95, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False, guide_true=True)

    
pl_te_10_00=RMSE_tail_plot(dat_temp_10[24], dat_temp_10[25], quant=0.00, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_co_10_05=RMSE_tail_plot(dat_temp_10[24], dat_temp_10[25], quant=0.05, greater=False, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_wa_10_95=RMSE_tail_plot(dat_temp_10[24], dat_temp_10[25], quant=0.95, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False)
pl_wi_10_00=RMSE_tail_plot(dat_wind_10[24], dat_wind_10[25], quant=0.00, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False, guide_true=True)
pl_wi_10_95=RMSE_tail_plot(dat_wind_10[24], dat_wind_10[25], quant=0.95, greater=True, HRES_ground=False, operational_comp=True, fixed_number=False, guide_true=True)


pl_te_1_00.set_index("a1", fontsize=25)
pl_wi_1_00.set_index("b1", fontsize=25)
pl_co_1_05.set_index("a1", fontsize=25)
pl_wa_1_95.set_index("b1", fontsize=25)
pl_wi_1_95.set_index("c1", fontsize=25)

pl_te_3_00.set_index("a2", fontsize=25)
pl_wi_3_00.set_index("b2", fontsize=25)
pl_co_3_05.set_index("a2", fontsize=25)
pl_wa_3_95.set_index("b2", fontsize=25)
pl_wi_3_95.set_index("c2", fontsize=25)

pl_te_5_00.set_index("a3", fontsize=25)
pl_wi_5_00.set_index("b3", fontsize=25)
pl_co_5_05.set_index("a3", fontsize=25)
pl_wa_5_95.set_index("b3", fontsize=25)
pl_wi_5_95.set_index("c3", fontsize=25)

pl_te_7_00.set_index("a4", fontsize=25)
pl_wi_7_00.set_index("b4", fontsize=25)
pl_co_7_05.set_index("a4", fontsize=25)
pl_wa_7_95.set_index("b4", fontsize=25)
pl_wi_7_95.set_index("c4", fontsize=25)

pl_te_10_00.set_index("a5", fontsize=25)
pl_wi_10_00.set_index("b5", fontsize=25)
pl_co_10_05.set_index("a5", fontsize=25)
pl_wa_10_95.set_index("b5", fontsize=25)
pl_wi_10_95.set_index("c5", fontsize=25)

#Fig.9
a=pl_te_1_00/pl_te_3_00/pl_te_5_00/pl_te_7_00/pl_te_10_00
b=pl_wi_1_00/pl_wi_3_00/pl_wi_5_00/pl_wi_7_00/pl_wi_10_00

a.set_suptitle("2m temperature", size=28, fontweight='bold')
b.set_suptitle("10m windspeed", size=28, fontweight='bold')

ab=(a|b)

ab.set_supxlabel("longitude", size=24, fontweight='bold')
ab.set_supylabel("latitude", size=24, fontweight='bold')

ab.savefig()

#Fig.10
a=pl_co_1_05/pl_co_3_05/pl_co_5_05/pl_co_7_05/pl_co_10_05
b=pl_wa_1_95/pl_wa_3_95/pl_wa_5_95/pl_wa_7_95/pl_wa_10_95
c=pl_wi_1_95/pl_wi_3_95/pl_wi_5_95/pl_wi_7_95/pl_wi_10_95

a.set_suptitle("Cold extremes", size=28, fontweight='bold')
b.set_suptitle("Hot extremes", size=28, fontweight='bold')
c.set_suptitle("Windspeed extremes", size=28, fontweight='bold')

abc=(a|b|c)

abc.set_supxlabel("longitude", size=24, fontweight='bold')
abc.set_supylabel("latitude", size=24, fontweight='bold')

abc.savefig()
