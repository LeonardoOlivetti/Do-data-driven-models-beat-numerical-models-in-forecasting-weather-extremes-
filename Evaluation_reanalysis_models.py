#%% Import functions

#exec(open(r'functions.py').read())
#%% Modules and open zarr

#from scipy.io import netcdf
import numpy as np
import sys
import xarray as xr
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm
import linearmodels as lm
import zarr

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

#%% pangu

midnights=list(range(3,41,4))

#zarr open
#pangu=xr.open_zarr('gs://weatherbench2/datasets/pangu/2018-2022_0012_0p25.zarr', chunks= {'time':8})
pangu=xr.open_zarr('gs://weatherbench2/datasets/pangu/2018-2022_0012_240x121_equiangular_with_poles_conservative.zarr', chunks= {'time':8})

# check zarr content
#print(pangu)


pangu = pangu[variables_s].sel( time=slice(start,end))

pangu = pangu.isel(prediction_timedelta = midnights) 
pangu = pangu.where(np.logical_or(pangu['time.hour'] == 00, pangu['time.hour'] == 12), drop=True)

pangu_wind_speed = pangu[variables_s[1]]
pangu_temp_2m = pangu[variables_s[0]]


#%%fuxi

midnights=list(range(3,41,4))

#zarr open
fuxi=xr.open_zarr('gs://weatherbench2/datasets/fuxi/2020-240x121_equiangular_with_poles_conservative.zarr', chunks= {'time':8})

#print(fuxi)

fuxi = fuxi[variables_s].sel( time=slice(start,end))

fuxi = fuxi.isel(prediction_timedelta = midnights) 
fuxi = fuxi.where(np.logical_or(fuxi['time.hour'] == 00, fuxi['time.hour'] == 12), drop=True)

fuxi_wind_speed = fuxi[variables_s[1]]
fuxi_temp_2m = fuxi[variables_s[0]]

#%% graphcast

midnights=list(range(3,41,4))

graphcast=xr.open_zarr('gs://weatherbench2/datasets/graphcast/2020/date_range_2019-11-16_2021-02-01_12_hours-240x121_equiangular_with_poles_conservative.zarr', chunks= {'time':8})

#print(graphcast)

graphcast = graphcast[variables_s].sel( time=slice(start,end))

graphcast = graphcast.isel(prediction_timedelta = midnights) 
graphcast = graphcast.where(np.logical_or(graphcast['time.hour'] == 00, graphcast['time.hour'] == 12), drop=True)

graphcast_wind_speed = graphcast[variables_s[1]]
graphcast_temp_2m = graphcast[variables_s[0]]


#%% Data import

#N.B. Remmember to use operational_comp=False throughout (comparison of reanalysis based models) and HRES_ground=True and, if you want to use IFS HRES t=0 as ground truth for IFS HRES, IFS_ground=True.
# More documentaion is available in the functions file



dat_temp_1=prep_all(temp_2m, HRES_truth_temp_2m, HRES_temp_2m, pangu_temp_2m, fuxi_temp_2m, graphcast_temp_2m, days_ahead=1, operational_comp=False)
dat_temp_3=prep_all(temp_2m, HRES_truth_temp_2m, HRES_temp_2m, pangu_temp_2m, fuxi_temp_2m, graphcast_temp_2m, days_ahead=3, operational_comp=False)
dat_temp_5=prep_all(temp_2m, HRES_truth_temp_2m, HRES_temp_2m, pangu_temp_2m, fuxi_temp_2m, graphcast_temp_2m, days_ahead=5, operational_comp=False)
dat_temp_7=prep_all(temp_2m, HRES_truth_temp_2m, HRES_temp_2m, pangu_temp_2m, fuxi_temp_2m, graphcast_temp_2m, days_ahead=7, operational_comp=False)
dat_temp_10=prep_all(temp_2m, HRES_truth_temp_2m, HRES_temp_2m, pangu_temp_2m, fuxi_temp_2m, graphcast_temp_2m, days_ahead=10, operational_comp=False)


dat_wind_1=prep_all(wind_speed, HRES_truth_wind_speed, HRES_wind_speed, pangu_wind_speed, fuxi_wind_speed, graphcast_wind_speed, days_ahead=1, operational_comp=False)
dat_wind_3=prep_all(wind_speed, HRES_truth_wind_speed, HRES_wind_speed, pangu_wind_speed, fuxi_wind_speed, graphcast_wind_speed, days_ahead=3, operational_comp=False)
dat_wind_5=prep_all(wind_speed, HRES_truth_wind_speed, HRES_wind_speed, pangu_wind_speed, fuxi_wind_speed, graphcast_wind_speed, days_ahead=5, operational_comp=False)
dat_wind_7=prep_all(wind_speed, HRES_truth_wind_speed, HRES_wind_speed, pangu_wind_speed, fuxi_wind_speed, graphcast_wind_speed, days_ahead=7, operational_comp=False)
dat_wind_10=prep_all(wind_speed, HRES_truth_wind_speed, HRES_wind_speed, pangu_wind_speed, fuxi_wind_speed, graphcast_wind_speed, days_ahead=10, operational_comp=False)


    
#%% RMSE computation


RMSE_temp_1_01=RMSE_all(dat_temp_1, operational_comp=False, greater=False, HRES_ground=True, quant=0.01)
RMSE_temp_3_01=RMSE_all(dat_temp_3, operational_comp=False, greater=False, HRES_ground=True, quant=0.01)
RMSE_temp_5_01=RMSE_all(dat_temp_5, operational_comp=False, greater=False, HRES_ground=True, quant=0.01)
RMSE_temp_7_01=RMSE_all(dat_temp_7, operational_comp=False, greater=False, HRES_ground=True, quant=0.01)
RMSE_temp_10_01=RMSE_all(dat_temp_10, operational_comp=False, greater=False, HRES_ground=True, quant=0.01)

RMSE_temp_1_05=RMSE_all(dat_temp_1, operational_comp=False, greater=False, HRES_ground=True, quant=0.05)
RMSE_temp_3_05=RMSE_all(dat_temp_3, operational_comp=False, greater=False, HRES_ground=True, quant=0.05)
RMSE_temp_5_05=RMSE_all(dat_temp_5, operational_comp=False, greater=False, HRES_ground=True, quant=0.05)
RMSE_temp_7_05=RMSE_all(dat_temp_7, operational_comp=False, greater=False, HRES_ground=True, quant=0.05)
RMSE_temp_10_05=RMSE_all(dat_temp_10, operational_comp=False, greater=False, HRES_ground=True, quant=0.05)

RMSE_temp_1_00=RMSE_all(dat_temp_1, operational_comp=False, greater=True, HRES_ground=True)
RMSE_temp_3_00=RMSE_all(dat_temp_3, operational_comp=False, greater=True, HRES_ground=True)
RMSE_temp_5_00=RMSE_all(dat_temp_5, operational_comp=False, greater=True, HRES_ground=True)
RMSE_temp_7_00=RMSE_all(dat_temp_7, operational_comp=False, greater=True, HRES_ground=True)
RMSE_temp_10_00=RMSE_all(dat_temp_10, operational_comp=False, greater=True, HRES_ground=True)

RMSE_temp_1_95=RMSE_all(dat_temp_1, operational_comp=False, greater=True, HRES_ground=True, quant=0.95)
RMSE_temp_3_95=RMSE_all(dat_temp_3, operational_comp=False, greater=True, HRES_ground=True, quant=0.95)
RMSE_temp_5_95=RMSE_all(dat_temp_5, operational_comp=False, greater=True, HRES_ground=True, quant=0.95)
RMSE_temp_7_95=RMSE_all(dat_temp_7, operational_comp=False, greater=True, HRES_ground=True, quant=0.95)
RMSE_temp_10_95=RMSE_all(dat_temp_10, operational_comp=False, greater=True, HRES_ground=True, quant=0.95)

RMSE_temp_1_99=RMSE_all(dat_temp_1, operational_comp=False, greater=True, HRES_ground=True, quant=0.99)
RMSE_temp_3_99=RMSE_all(dat_temp_3, operational_comp=False, greater=True, HRES_ground=True, quant=0.99)
RMSE_temp_5_99=RMSE_all(dat_temp_5, operational_comp=False, greater=True, HRES_ground=True, quant=0.99)
RMSE_temp_7_99=RMSE_all(dat_temp_7, operational_comp=False, greater=True, HRES_ground=True, quant=0.99)
RMSE_temp_10_99=RMSE_all(dat_temp_10, operational_comp=False, greater=True, HRES_ground=True, quant=0.99)

RMSE_wind_1_00=RMSE_all(dat_wind_1, operational_comp=False, greater=True, HRES_ground=True)
RMSE_wind_3_00=RMSE_all(dat_wind_3, operational_comp=False, greater=True, HRES_ground=True)
RMSE_wind_5_00=RMSE_all(dat_wind_5, operational_comp=False, greater=True, HRES_ground=True)
RMSE_wind_7_00=RMSE_all(dat_wind_7, operational_comp=False, greater=True, HRES_ground=True)
RMSE_wind_10_00=RMSE_all(dat_wind_10, operational_comp=False, greater=True, HRES_ground=True)

RMSE_wind_1_95=RMSE_all(dat_wind_1, operational_comp=False, greater=True, HRES_ground=True, quant=0.95)
RMSE_wind_3_95=RMSE_all(dat_wind_3, operational_comp=False, greater=True, HRES_ground=True, quant=0.95)
RMSE_wind_5_95=RMSE_all(dat_wind_5, operational_comp=False, greater=True, HRES_ground=True, quant=0.95)
RMSE_wind_7_95=RMSE_all(dat_wind_7, operational_comp=False, greater=True, HRES_ground=True, quant=0.95)
RMSE_wind_10_95=RMSE_all(dat_wind_10, operational_comp=False, greater=True, HRES_ground=True, quant=0.95)

RMSE_wind_1_99=RMSE_all(dat_wind_1, operational_comp=False, greater=True, HRES_ground=True, quant=0.99)
RMSE_wind_3_99=RMSE_all(dat_wind_3, operational_comp=False, greater=True, HRES_ground=True, quant=0.99)
RMSE_wind_5_99=RMSE_all(dat_wind_5, operational_comp=False, greater=True, HRES_ground=True, quant=0.99)
RMSE_wind_7_99=RMSE_all(dat_wind_7, operational_comp=False, greater=True, HRES_ground=True, quant=0.99)
RMSE_wind_10_99=RMSE_all(dat_wind_10, operational_comp=False, greater=True, HRES_ground=True, quant=0.99)



#%% Figures grid-point level significance and magnitude

# In depth tile plots

tile_depth_temp_01=tile_depth_all(RMSE_temp_1_01, RMSE_temp_3_01, RMSE_temp_5_01, RMSE_temp_7_01, RMSE_temp_10_01, "Cold extremes", operational_comp=False)
tile_depth_temp_99=tile_depth_all(RMSE_temp_1_99, RMSE_temp_3_99, RMSE_temp_5_99, RMSE_temp_7_99, RMSE_temp_10_99, "Hot extremes", operational_comp=False)
tile_depth_wind_99=tile_depth_all(RMSE_wind_1_99, RMSE_wind_3_99, RMSE_wind_5_99, RMSE_wind_7_99, RMSE_wind_10_99, "Wind extremes", operational_comp=False)

tile_depth_temp_01.set_index("a", fontsize=50)
tile_depth_temp_99.set_index("b", fontsize=50)
tile_depth_wind_99.set_index("c", fontsize=50)

(tile_depth_temp_01|tile_depth_temp_99|tile_depth_wind_99).savefig()


tile_depth_temp_05=tile_depth_all(RMSE_temp_1_05, RMSE_temp_3_05, RMSE_temp_5_05, RMSE_temp_7_05, RMSE_temp_10_05, "Cold extremes", operational_comp=False)
tile_depth_temp_95=tile_depth_all(RMSE_temp_1_95, RMSE_temp_3_95, RMSE_temp_5_95, RMSE_temp_7_95, RMSE_temp_10_95, "Warm extremes", operational_comp=False)
tile_depth_wind_95=tile_depth_all(RMSE_wind_1_95, RMSE_wind_3_95, RMSE_wind_5_95, RMSE_wind_7_95, RMSE_wind_10_95, "Wind extremes", operational_comp=False)

tile_depth_temp_05.set_index("a", fontsize=50)
tile_depth_temp_95.set_index("b", fontsize=50)
tile_depth_wind_95.set_index("c", fontsize=50)
(tile_depth_temp_05|tile_depth_temp_95|tile_depth_wind_95).savefig()


tile_depth_temp_00=tile_depth_all(RMSE_temp_1_00, RMSE_temp_3_00, RMSE_temp_5_00, RMSE_temp_7_00, RMSE_temp_10_00, "2m temperature", operational_comp=False)
tile_depth_wind_00=tile_depth_all(RMSE_wind_1_00, RMSE_wind_3_00, RMSE_wind_5_00, RMSE_wind_7_00, RMSE_wind_10_00, "10m windspeed", operational_comp=False)

tile_depth_temp_00.set_index("a", fontsize=50)
tile_depth_wind_00.set_index("b", fontsize=50)
(tile_depth_temp_00|tile_depth_wind_00).savefig()


# Tile best model table
model_colors = {'HRES': '#DDDDDD', 'Pangu': '#40B0A6', 'Fuxi': 'pink', 'Graphcast':'#E1BA6A'}


#Tile figure
RMSE_tile_temp_05=pw.load_ggplot(tile_comp_plot(RMSE_temp_1_05,RMSE_temp_3_05,RMSE_temp_5_05,RMSE_temp_7_05,RMSE_temp_10_05, operational_comp=False)+\
    ggtitle("Cold extremes 5%")+\
    scale_fill_manual(values=model_colors, guide=False))
    
RMSE_tile_temp_01=pw.load_ggplot(tile_comp_plot(RMSE_temp_1_01,RMSE_temp_3_01,RMSE_temp_5_01,RMSE_temp_7_01,RMSE_temp_10_01, operational_comp=False)+\
    ggtitle("Cold extremes 1%")+\
    scale_fill_manual(values=model_colors, guide=False))
    
RMSE_tile_temp_global=pw.load_ggplot(tile_comp_plot(RMSE_temp_1_00,RMSE_temp_3_00,RMSE_temp_5_00,RMSE_temp_7_00,RMSE_temp_10_00, operational_comp=False)+\
    ggtitle("2m temperature: all observations"))
    
RMSE_tile_temp_95=pw.load_ggplot(tile_comp_plot(RMSE_temp_1_95,RMSE_temp_3_95,RMSE_temp_5_95,RMSE_temp_7_95,RMSE_temp_10_95, operational_comp=False)+\
    ggtitle("Hot extremes 5%")+\
    scale_fill_manual(values=model_colors, guide=False))
    
RMSE_tile_temp_99=pw.load_ggplot(tile_comp_plot(RMSE_temp_1_99,RMSE_temp_3_99,RMSE_temp_5_99,RMSE_temp_7_99,RMSE_temp_10_99, operational_comp=False)+\
    ggtitle("Hot extremes 1%")+\
    scale_fill_manual(values=model_colors, guide=False))
    
RMSE_tile_wind_global=pw.load_ggplot(tile_comp_plot(RMSE_wind_1_00,RMSE_wind_3_00,RMSE_wind_5_00,RMSE_wind_7_00,RMSE_wind_10_00, operational_comp=False)+\
    ggtitle("10m windspeed: all observations"))
    
RMSE_tile_wind_95=pw.load_ggplot(tile_comp_plot(RMSE_wind_1_95,RMSE_wind_3_95,RMSE_wind_5_95,RMSE_wind_7_95,RMSE_wind_10_95, operational_comp=False)+\
    ggtitle("Windspeed extremes 5%")+\
    scale_fill_manual(values=model_colors, guide=False))
    
RMSE_tile_wind_99=pw.load_ggplot(tile_comp_plot(RMSE_wind_1_99,RMSE_wind_3_99,RMSE_wind_5_99,RMSE_wind_7_99,RMSE_wind_10_99, operational_comp=False)+\
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

((RMSE_tile_temp_05|RMSE_tile_temp_95|RMSE_tile_wind_95)/(RMSE_tile_temp_01|RMSE_tile_temp_99|RMSE_tile_wind_99)/(RMSE_tile_temp_global|RMSE_tile_wind_global)).savefig()



# Maps



te_1_00=RMSE_point_global(dat_temp_1[24], dat_temp_1[25], quant=0.00, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
co_1_05=RMSE_point_global(dat_temp_1[24], dat_temp_1[25], quant=0.05, greater=False, HRES_ground=True, operational_comp=False, fixed_number=False)
wa_1_95=RMSE_point_global(dat_temp_1[24], dat_temp_1[25], quant=0.95, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
wi_1_00=RMSE_point_global(dat_wind_1[24], dat_wind_1[25], quant=0.00, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
wi_1_95=RMSE_point_global(dat_wind_1[24], dat_wind_1[25], quant=0.95, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)


model_colors = {'HRES': '#DDDDDD', 'Pangu': '#40B0A6', 'Fuxi': 'pink', 'Graphcast':'#E1BA6A'}


world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

te_1_00=p_val_cor(te_1_00)
wi_1_00=p_val_cor(wi_1_00)

co_1_05=p_val_cor(co_1_05)
wa_1_95=p_val_cor(wa_1_95)
wi_1_95=p_val_cor(wi_1_95)  

pl_co_1_05=plot_RMSE_point_global(co_1_05)
pl_wa_1_95=plot_RMSE_point_global(wa_1_95)
pl_wi_1_95=plot_RMSE_point_global(wi_1_95,guide_true=True)

pl_te_1_00=plot_RMSE_point_global(te_1_00)
pl_wi_1_00=plot_RMSE_point_global(wi_1_00,guide_true=True)

pl_co_1_05_magnitude=plot_RMSE_magnitude(co_1_05)
pl_wa_1_95_magnitude=plot_RMSE_magnitude(wa_1_95)
pl_wi_1_95_magnitude=plot_RMSE_magnitude(wi_1_95)

pl_te_1_00_magnitude=plot_RMSE_magnitude(te_1_00)
pl_wi_1_00_magnitude=plot_RMSE_magnitude(wi_1_00)

    
te_3_00=RMSE_point_global(dat_temp_3[24], dat_temp_3[25], quant=0.00, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
co_3_05=RMSE_point_global(dat_temp_3[24], dat_temp_3[25], quant=0.05, greater=False, HRES_ground=True, operational_comp=False, fixed_number=False)
wa_3_95=RMSE_point_global(dat_temp_3[24], dat_temp_3[25], quant=0.95, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
wi_3_00=RMSE_point_global(dat_wind_3[24], dat_wind_3[25], quant=0.00, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
wi_3_95=RMSE_point_global(dat_wind_3[24], dat_wind_3[25], quant=0.95, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)

te_3_00=p_val_cor(te_3_00)
wi_3_00=p_val_cor(wi_3_00)

co_3_05=p_val_cor(co_3_05)
wa_3_95=p_val_cor(wa_3_95)
wi_3_95=p_val_cor(wi_3_95)

pl_co_3_05=plot_RMSE_point_global(co_3_05)
pl_wa_3_95=plot_RMSE_point_global(wa_3_95)
pl_wi_3_95=plot_RMSE_point_global(wi_3_95,guide_true=True)

pl_te_3_00=plot_RMSE_point_global(te_3_00)
pl_wi_3_00=plot_RMSE_point_global(wi_3_00,guide_true=True)

pl_co_3_05_magnitude=plot_RMSE_magnitude(co_3_05)
pl_wa_3_95_magnitude=plot_RMSE_magnitude(wa_3_95)
pl_wi_3_95_magnitude=plot_RMSE_magnitude(wi_3_95)

pl_te_3_00_magnitude=plot_RMSE_magnitude(te_3_00)
pl_wi_3_00_magnitude=plot_RMSE_magnitude(wi_3_00)

    

te_5_00=RMSE_point_global(dat_temp_5[24], dat_temp_5[25], quant=0.00, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
co_5_05=RMSE_point_global(dat_temp_5[24], dat_temp_5[25], quant=0.05, greater=False, HRES_ground=True, operational_comp=False, fixed_number=False)
wa_5_95=RMSE_point_global(dat_temp_5[24], dat_temp_5[25], quant=0.95, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
wi_5_00=RMSE_point_global(dat_wind_5[24], dat_wind_5[25], quant=0.00, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
wi_5_95=RMSE_point_global(dat_wind_5[24], dat_wind_5[25], quant=0.95, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)

te_5_00=p_val_cor(te_5_00)
wi_5_00=p_val_cor(wi_5_00)

co_5_05=p_val_cor(co_5_05)
wa_5_95=p_val_cor(wa_5_95)
wi_5_95=p_val_cor(wi_5_95)

pl_co_5_05=plot_RMSE_point_global(co_5_05)
pl_wa_5_95=plot_RMSE_point_global(wa_5_95)
pl_wi_5_95=plot_RMSE_point_global(wi_5_95,guide_true=True)

pl_te_5_00=plot_RMSE_point_global(te_5_00)
pl_wi_5_00=plot_RMSE_point_global(wi_5_00,guide_true=True)

pl_co_5_05_magnitude=plot_RMSE_magnitude(co_5_05)
pl_wa_5_95_magnitude=plot_RMSE_magnitude(wa_5_95)
pl_wi_5_95_magnitude=plot_RMSE_magnitude(wi_5_95)

pl_te_5_00_magnitude=plot_RMSE_magnitude(te_5_00)
pl_wi_5_00_magnitude=plot_RMSE_magnitude(wi_5_00)

    
te_7_00=RMSE_point_global(dat_temp_7[24], dat_temp_7[25], quant=0.00, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
co_7_05=RMSE_point_global(dat_temp_7[24], dat_temp_7[25], quant=0.05, greater=False, HRES_ground=True, operational_comp=False, fixed_number=False)
wa_7_95=RMSE_point_global(dat_temp_7[24], dat_temp_7[25], quant=0.95, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
wi_7_00=RMSE_point_global(dat_wind_7[24], dat_wind_7[25], quant=0.00, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
wi_7_95=RMSE_point_global(dat_wind_7[24], dat_wind_7[25], quant=0.95, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)

te_7_00=p_val_cor(te_7_00)
wi_7_00=p_val_cor(wi_7_00)

co_7_05=p_val_cor(co_7_05)
wa_7_95=p_val_cor(wa_7_95)
wi_7_95=p_val_cor(wi_7_95)

pl_co_7_05=plot_RMSE_point_global(co_7_05)
pl_wa_7_95=plot_RMSE_point_global(wa_7_95)
pl_wi_7_95=plot_RMSE_point_global(wi_7_95,guide_true=True)

pl_te_7_00=plot_RMSE_point_global(te_7_00)
pl_wi_7_00=plot_RMSE_point_global(wi_7_00,guide_true=True)

pl_co_7_05_magnitude=plot_RMSE_magnitude(co_7_05)
pl_wa_7_95_magnitude=plot_RMSE_magnitude(wa_7_95)
pl_wi_7_95_magnitude=plot_RMSE_magnitude(wi_7_95)

pl_te_7_00_magnitude=plot_RMSE_magnitude(te_7_00)
pl_wi_7_00_magnitude=plot_RMSE_magnitude(wi_7_00)


te_10_00=RMSE_point_global(dat_temp_10[24], dat_temp_10[25], quant=0.00, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
co_10_05=RMSE_point_global(dat_temp_10[24], dat_temp_10[25], quant=0.05, greater=False, HRES_ground=True, operational_comp=False, fixed_number=False)
wa_10_95=RMSE_point_global(dat_temp_10[24], dat_temp_10[25], quant=0.95, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
wi_10_00=RMSE_point_global(dat_wind_10[24], dat_wind_10[25], quant=0.00, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)
wi_10_95=RMSE_point_global(dat_wind_10[24], dat_wind_10[25], quant=0.95, greater=True, HRES_ground=True, operational_comp=False, fixed_number=False)

te_10_00=p_val_cor(te_10_00)
wi_10_00=p_val_cor(wi_10_00)

co_10_05=p_val_cor(co_10_05)
wa_10_95=p_val_cor(wa_10_95)
wi_10_95=p_val_cor(wi_10_95)

pl_co_10_05=plot_RMSE_point_global(co_10_05)
pl_wa_10_95=plot_RMSE_point_global(wa_10_95)
pl_wi_10_95=plot_RMSE_point_global(wi_10_95,guide_true=True)

pl_te_10_00=plot_RMSE_point_global(te_10_00)
pl_wi_10_00=plot_RMSE_point_global(wi_10_00,guide_true=True)

pl_co_10_05_magnitude=plot_RMSE_magnitude(co_10_05,guide_true=True)
pl_wa_10_95_magnitude=plot_RMSE_magnitude(wa_10_95)
pl_wi_10_95_magnitude=plot_RMSE_magnitude(wi_10_95,guide_true=True)

pl_te_10_00_magnitude=plot_RMSE_magnitude(te_10_00,guide_true=True)
pl_wi_10_00_magnitude=plot_RMSE_magnitude(wi_10_00,guide_true=True)


#%% Build the panles

pl_te_1_00.set_index("a", fontsize=25)
pl_wi_1_00.set_index("b", fontsize=25)
pl_te_3_00.set_index("c", fontsize=25)
pl_wi_3_00.set_index("d", fontsize=25)
pl_te_5_00.set_index("e", fontsize=25)
pl_wi_5_00.set_index("f", fontsize=25)
pl_te_7_00.set_index("g", fontsize=25)
pl_wi_7_00.set_index("h", fontsize=25)
pl_te_10_00.set_index("i", fontsize=25)
pl_wi_10_00.set_index("j", fontsize=25)



a=pl_te_1_00/pl_te_3_00/pl_te_5_00/pl_te_7_00/pl_te_10_00
b=pl_wi_1_00/pl_wi_3_00/pl_wi_5_00/pl_wi_7_00/pl_wi_10_00

a.set_suptitle("2m temperature", size=28, fontweight='bold')
b.set_suptitle("10m windspeed", size=28, fontweight='bold')

ab=(a|b)

ab.set_supxlabel("longitude", size=24, fontweight='bold')
ab.set_supylabel("latitude", size=24, fontweight='bold')

ab.savefig()


pl_co_1_05.set_index("a", fontsize=25)
pl_wa_1_95.set_index("b", fontsize=25)
pl_wi_1_95.set_index("c", fontsize=25)
pl_co_3_05.set_index("d", fontsize=25)
pl_wa_3_95.set_index("e", fontsize=25)
pl_wi_3_95.set_index("f", fontsize=25)
pl_co_5_05.set_index("g", fontsize=25)
pl_wa_5_95.set_index("h", fontsize=25)
pl_wi_5_95.set_index("i", fontsize=25)
pl_co_7_05.set_index("j", fontsize=25)
pl_wa_7_95.set_index("k", fontsize=25)
pl_wi_7_95.set_index("l", fontsize=25)
pl_co_10_05.set_index("m", fontsize=25)
pl_wa_10_95.set_index("n", fontsize=25)
pl_wi_10_95.set_index("o", fontsize=25)

a=pl_co_1_05/pl_co_3_05/pl_co_5_05/pl_co_7_05/pl_co_10_05
b=pl_wa_1_95/pl_wa_3_95/pl_wa_5_95/pl_wa_7_95/pl_wa_10_95
c=pl_wi_1_95/pl_wi_3_95/pl_wi_5_95/pl_wi_7_95/pl_wi_10_95

a.set_suptitle("Cold extremes", size=28, fontweight='bold')
b.set_suptitle("Hot extremes", size=28, fontweight='bold')
c.set_suptitle("Windspeed extremes", size=28, fontweight='bold')

abc=(a|b|c)


abc.set_supxlabel("longitude", size=24, fontweight='bold')
abc.set_supylabel("latitude", size=24, fontweight='bold')



#Magntiude


pl_te_1_00_magnitude.set_index("a", fontsize=20)
pl_wi_1_00_magnitude.set_index("b", fontsize=20)

pl_te_3_00_magnitude.set_index("c", fontsize=20)
pl_wi_3_00_magnitude.set_index("d", fontsize=20)

pl_te_5_00_magnitude.set_index("e", fontsize=20)
pl_wi_5_00_magnitude.set_index("f", fontsize=20)

pl_te_7_00_magnitude.set_index("g", fontsize=20)
pl_wi_7_00_magnitude.set_index("h", fontsize=20)

pl_te_10_00_magnitude.set_index("i", fontsize=20)
pl_wi_10_00_magnitude.set_index("j", fontsize=20)


a=pl_te_1_00_magnitude/pl_te_3_00_magnitude/pl_te_5_00_magnitude/pl_te_7_00_magnitude/pl_te_10_00_magnitude
b=pl_wi_1_00_magnitude/pl_wi_3_00_magnitude/pl_wi_5_00_magnitude/pl_wi_7_00_magnitude/pl_wi_10_00_magnitude

a.set_suptitle("2m temperature", size=28, fontweight='bold')
b.set_suptitle("10m windspeed", size=28, fontweight='bold')

ab=(a|b)

ab.set_supxlabel("longitude", labelpad=-15, size=24, fontweight='bold')
ab.set_supylabel("latitude", size=24, fontweight='bold')



pl_co_1_05_magnitude.set_index("a", fontsize=20)
pl_wa_1_95_magnitude.set_index("b", fontsize=20)
pl_wi_1_95_magnitude.set_index("c", fontsize=20)
pl_co_3_05_magnitude.set_index("d", fontsize=20)
pl_wa_3_95_magnitude.set_index("e", fontsize=20)
pl_wi_3_95_magnitude.set_index("f", fontsize=20)
pl_co_5_05_magnitude.set_index("g", fontsize=20)
pl_wa_5_95_magnitude.set_index("h", fontsize=20)
pl_wi_5_95_magnitude.set_index("i", fontsize=20)
pl_co_7_05_magnitude.set_index("j", fontsize=20)
pl_wa_7_95_magnitude.set_index("k", fontsize=20)
pl_wi_7_95_magnitude.set_index("l", fontsize=20)
pl_co_10_05_magnitude.set_index("m", fontsize=20)
pl_wa_10_95_magnitude.set_index("n", fontsize=20)
pl_wi_10_95_magnitude.set_index("o", fontsize=20)


a=pl_co_1_05_magnitude/pl_co_3_05_magnitude/pl_co_5_05_magnitude/pl_co_7_05_magnitude/pl_co_10_05_magnitude
b=pl_wa_1_95_magnitude/pl_wa_3_95_magnitude/pl_wa_5_95_magnitude/pl_wa_7_95_magnitude/pl_wa_10_95_magnitude
c=pl_wi_1_95_magnitude/pl_wi_3_95_magnitude/pl_wi_5_95_magnitude/pl_wi_7_95_magnitude/pl_wi_10_95_magnitude

a.set_suptitle("Cold extremes", size=28, fontweight='bold')
b.set_suptitle("Hot extremes", size=28, fontweight='bold')
c.set_suptitle("Windspeed extremes", size=28, fontweight='bold')

abc=(a|b|c)

abc.set_supxlabel("longitude", size=24, fontweight='bold')
abc.set_supylabel("latitude", size=24, fontweight='bold')

