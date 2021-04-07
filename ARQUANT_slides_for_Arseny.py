#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modified on Jan 27, 2021
@author: alexander
"""

print('Initialization.. !!!')

from IPython import get_ipython
ipython = get_ipython()
if '__IPYTHON__' in globals():
    ipython.magic('load_ext autoreload')
    ipython.magic('autoreload 2')
# get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
# get_ipython().run_line_magic('matplotlib', 'inline')
    
import numpy as np
import pandas as pd
from os import chdir, listdir, path, rename, makedirs
import datetime as dt
from importlib import reload

# Read historical returns
print('Loading daily returns of startegies..')

maindir='./'
datadir='Presentation_2021-2/'

#%%
## PRINTING and PLOTING for Slides 5, 6, 7, 8, 9
chdir(maindir)
import Slides_for_print_function

# specify the custom font to use
import matplotlib.pyplot as plt
plt.rcParams['font.family']= 'Avenir'
# to check all fonts available
# import matplotlib.font_manager
# matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
# plt.rcParams['font.Avenir'] = 'Avenir'

dicclrs={'arquant':'#ea6639',   # '#dc6d45'
         'benchmark1':'#43884e',
         'benchmark2':'#6b6c6d',
         'benchmark3': '#b5583c',
         'background':'#edb6a2', # '#f2d1c6'
         'dates': '#afb1b2',    # '#d6d7d8'
         'plotname': 'black'}

period_list_plot=['Inception'] #for slides 5 and 6
periods_stats=['Inception', 
               # '2018', 
               '2019', 
               '2020', 
               '2021', 
               # 'L12M', 
               # 'L3M', 
               # 'L1M'
               ]
periods_ff=['Inception', #for slides 7 and 8
         # '2018', 
         '2019', 
         '2020', 
         '2021', 
          # 'L12M', 
          # 'YTD',
          # 'L3M', 
         # 'L1M'
         ]  

##Preparing Statistics for Slide 7
from Slides_for_print_function import stats_periods_for_print

ak_stats=pd.read_pickle(maindir+datadir+'Stats.pkl')
ak_stats_for_print=stats_periods_for_print(ak_stats)
ak_stats_for_print.to_csv(maindir+datadir+'Stats_for_print.csv')
# Make HTML with company styling
reload(Slides_for_print_function)
from Slides_for_print_function import stat_html
stat_html(ak_stats_for_print[periods_stats], 
          maindir+datadir+'Stats_for_print')


## Preparing French-Fama model for Slide 8
#Load from file+index_col=[0]
# reload(Slides_for_print_function)
from Slides_for_print_function import f_alpha, f_beta
bt_all=pd.read_pickle(maindir+datadir+'FF3x2.pkl')
# Make as % and reduce decimals
bt=f_alpha(bt_all)
bt=f_beta(bt)
#Make HTML with company styling      
stat_html(bt[periods_ff], maindir+datadir+'FF3x2_for_print')


## Preparing Factsheet for Slide 9
# reload(Slides_for_print_function)
from Slides_for_print_function import f_fsnet, factsheet_html
feestring='1.0-20-5'
fs_net=pd.read_csv(maindir+datadir+'Fact_Sheet_after_fees.csv', index_col=[0])
factsheet_html(f_fsnet(fs_net), maindir+datadir+'Fact_sheet_after_fees')


## Preparing Drawdown Plot for Slide 6
# reload(Slides_for_print_function)
from Slides_for_print_function import plot_longest_drawdowns, period_index, read_csv
print('Creating Drawdown Period Plot for given time period...')
subdir='Plots/'
makedirs(maindir+datadir+subdir, exist_ok=True)
ak=pd.read_pickle(maindir+datadir+'Returns.pkl').squeeze()

periods=period_index(ak, period_list_plot)

for period in periods.keys():
    print('Period: ', period)    
    model3 = 'Drawdoans Periods'
    savefig3=maindir+datadir+subdir+model3+'_'+period+'.png'
    plot_longest_drawdowns(ak.loc[periods[period]], dicclrs, 
                           savefig=savefig3,
                           periods=5, grayscale=False, 
                           show=False, figsize=(8.5, 5.5))


## Preparing Cumulative Return Plot for Slide 5
# reload(Slides_for_print_function)
from Slides_for_print_function import plot_for_print

dfs=pd.read_pickle(maindir+datadir+'ARQuant vs Benchmarks.pkl')

print(dfs)

pDate=dfs.to_json()
print(pDate)
import json
with open('pMonth.json', 'w') as outfile:
    json.dump(pDate, outfile)

periods=period_index(dfs, period_list_plot) #New indexies for L12M

print('Comparing and plotting monthly performance of ARQuant vs SPY, QQQ and HFR indexes...')
#Dictionary with colors
clist=[] #Colors from ARQuant presentation
for key, value in dicclrs.items():
    temp = value
    clist.append(temp)
from matplotlib.cm import get_cmap
clist=clist[:3]
if len(dfs.columns) > len(clist) :
    d=len(dfs.columns) - len(clist)
    cmap = get_cmap('Paired') #RuOr Accent
    for i in range(d):
        clist.append(cmap(1/d))

for period in periods.keys():
    print('Period: ', period)    
    dfs_wealth = ((1+dfs.loc[periods[period]]).cumprod()-1)*100
    # start_wealth=pd.DataFrame(np.ones( (1,len(dfs_wealth.columns)) ), index=[dfs_wealth.index[0].start_time.to_period('D')], columns=dfs.columns)
    # dfs_sim1=pd.concat([start_wealth, dfs_wealth], axis=0)
    plot_for_print(dfs_wealth, dicclrs,
                   datadir=maindir+datadir+subdir, 
                   plotname='ARQuant vs Benchmarks '+period,
                   figsize=(9,6),
                   c=clist)
   
