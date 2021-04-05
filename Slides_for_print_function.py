#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 13:26:07 2021

@author: alexander
"""
import datetime as dt
import pandas as pd

#%%
def stats_periods_for_print(st, rnd=1):
    stats=st.copy()
    stats.rename(columns={'Historic CVaR (5%)':'CVaR (5%)',
                          'Cornish-Fisher VaR (5%)':'VaR (5%)', 
                          'Recovery time (max days)':'Recovery (days)',
                          'Sharpe ratio':'Sharpe'
                          },  inplace=True)
    stats=stats.drop(["Recovery time(75% cases)", 
                      "Daily Win Probability", "Leverage optimal",
                      "Expected growth", "Years to increase by 1x Vol"], 
                     axis=1)

    stats['Recovery (days)']=st['Recovery time (max days)'].dt.days #convert DeltaTime to Days   
    stats["Growth"]= (st['Growth']*100).round(rnd).astype(str)+"%"
    stats["Return annualized"]= (st["Return annualized"]*100).round(rnd).astype(str)+"%"
    stats["Volatility annualized"]= (st["Volatility annualized"]*100).round(rnd).astype(str)+"%"
    stats["VaR (5%)"]= (st["Cornish-Fisher VaR (5%)"]*100).round(rnd).astype(str)+"%"
    stats["CVaR (5%)"]= (st["Historic CVaR (5%)"]*100).round(rnd).astype(str)+"%"
    stats["Max Drawdown"]= (st["Max Drawdown"]*100).round(rnd).astype(str)+"%"
    stats["Mean Return daily"]= (st["Mean Return daily"]*100).round(2).astype(str)+"%"
    stats["Calmar"]=st["Calmar"].round(rnd+1)
    stats["Sortino"]=st["Sortino"].round(rnd+1)
    stats['Kelly criterion']=st["Kelly criterion"].round(rnd+1)
    stats["Best Day"]= (st["Best Day"]*100).round(rnd).astype(str)+"%"
    stats["Worst Day"]= (st["Worst Day"]*100).round(rnd).astype(str)+"%"
    stats["Average Win daily"]= (st["Average Win daily"]*100).round(rnd).astype(str)+"%"
    stats["Average Loss daily"]= (st["Average Loss daily"]*100).round(rnd).astype(str)+"%"
    stats["Win rate"]= (st["Win rate"]*100).round(rnd).astype(str)+"%"
    return stats.T

    
def f_alpha(bt_all, row=['Alpha (p.a.)'], decimals=0):
    for col in bt_all.columns:
        if decimals==0:
            bt_all.loc[row,col]=(bt_all.loc[row,col]*100).astype(int).astype(str)+"%"
        else:
            bt_all.loc[row,col]=round((bt_all.loc[row,col]*100).astype(float),decimals).astype(str)+"%"            
    return bt_all

def f_beta(bt_all, row=['Beta', 'SMB', 'HML', 'RMW', 'CMA'], decimals=2):
    for col in bt_all.columns:
        bt_all.loc[row,col]=round(bt_all.loc[row,col].astype('float'),decimals)
    return bt_all

# Statists Table -> HTML
def stat_html(df, outputname):
      #  Try letter instead of <style>
      # <link rel="stylesheet" type="text/css" href="style.css"> 

    pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
    # create html_string with styles
    html_string = '''
    <html>
      <head><title>HTML Pandas Dataframe with CSS</title>
      <style>
        .dataframe table    { margin-bottom: 1.4em; 
                             width: 100%; 
                             border-collapse: collapse;
                             border-spacing: 0;
                             font-family: "Avenir";
                             }
        .dataframe th       { font-weight: bold; text-align: left; 
                             padding: 5px 25px 5px 10px; 
                             border: 0px;}
        .dataframe tr > *:nth-child(1) { width:35%; }
        .dataframe tr:last-child{ border-bottom: 5px solid #f0997a;}
        .dataframe thead th { background: #f0997a; 
                             padding: 5px 25px 5px 10px;}
        .dataframe td       { text-align: left; 
                             padding: 5px 25px 5px 10px; 
                             border: 0; }
        .dataframe th,td,caption { padding: 5px 25px 5px 10px; }
        .dataframe tbody tr:nth-child(even) td, 
        .dataframe tbody tr.even td { background: #d2d2d2; }
        .dataframe tbody tr:nth-child(even) th, 
        .dataframe tbody tr.even th { background: #d2d2d2; }
        .dataframe tbody tr:last-child td { background: #f0997a; }
        .dataframe tbody tr:last-child th { background: #f0997a; }
        .dataframe tfoot     { font-style: italic; }
        .dataframe caption   { background: #eee; }
                              
         </style>
      </head>
      <body>'''

    html_string += df.to_html()
    #Remove space between cells
    html_string=html_string.replace('table border="1"',
                                    'table border="0" cellspacing="0"'
                                    )
    #Add last row with orange color
    html_string=html_string.replace('</tbody>',
    '''<tr style="height: 25px; ">
          <th></th>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
    </tr>
  </tbody>'''
  )
  
    html_string +='''
    </body>
    </html>'''
    
    # OUTPUT AN HTML FILE
    with open(outputname+'.html', 'w') as f:
        f.write(html_string)
    
    from weasyprint import HTML, CSS
    HTML(outputname+'.html').write_png(outputname+'.png')
    # HTML(outputname+'.html').write_png(outputname+'.png',
    #                                    stylesheets=CSS())    
    return 

def factsheet_html(df, outputname):
      #  Try letter instead of <style>
      # <link rel="stylesheet" type="text/css" href="style.css"> 

    pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
    # create html_string with styles
    html_string = '''
    <html>
      <head><title>HTML Pandas Dataframe with CSS</title>
      <style>
        .dataframe table    { margin-bottom: 1.4em; 
                             width: 100%; 
                             border-collapse: collapse;
                             border-spacing: 0;
                             font-family: "Avenir";
                             }
        .dataframe th       { font-weight: bold; text-align: left; 
                             padding: 5px 25px 5px 10px; 
                             border: 0px;}
        .dataframe tr:last-child{ border-bottom: 5px solid #f0997a;}
        .dataframe thead th { background: #f0997a; 
                             padding: 5px 25px 5px 10px;}
        .dataframe td       { text-align: left; 
                             padding: 5px 25px 5px 10px; 
                             border: 0; }
        .dataframe th,td,caption { padding: 5px 25px 5px 10px; }
        .dataframe tbody tr:nth-child(even) td, 
        .dataframe tbody tr.even td { background: #d2d2d2; }
        .dataframe tbody tr:nth-child(even) th, 
        .dataframe tbody tr.even th { background: #d2d2d2; }
        .dataframe tfoot     { font-style: italic; }
        .dataframe caption   { background: #eee; }
                              
         </style>
      </head>
      <body>'''

    html_string += df.to_html()
    #Remove space between cells
    html_string=html_string.replace('table border="1"',
                                    'table border="0" cellspacing="0"'
                                    )
    #Add last row with orange color
    html_string=html_string.replace('</tbody>',
    '''<tr style="height: 25px; ">
          <th></th>
          <td></td><td></td><td></td>
          <td></td><td></td><td></td>
          <td></td><td></td><td></td>
          <td></td><td></td><td></td>
          <td></td>
    </tr>
  </tbody>'''
  )
  
    html_string +='''
    </body>
    </html>'''
    
    # OUTPUT AN HTML FILE
    with open(outputname+'.html', 'w') as f:
        f.write(html_string)
    
    from weasyprint import HTML, CSS
    HTML(outputname+'.html').write_png(outputname+'.png')
    # HTML(outputname+'.html').write_png(outputname+'.png',
    #                                    stylesheets=CSS())   
    return 

def f_fsnet(df):
    df.fillna(' ', inplace=True)
    df1=df.copy()    
    for row in df.index:
        for col in df.columns:
            if df.loc[row,col]!= ' ':
                df1.loc[row,col]="{0:.1f}%".format(df.loc[row,col] * 100)
    return df1


##Drawdown Periods Plot
# chdir('/users/alexander/Dropbox/5-Finance/GQS_Capital/ML/Python/GoTrader/')
# from edhec_risk_kit import drawdown
# ak_dd=drawdown(ak_ret)
# ak_dd.Drawdown.pyplot.bar
# import quantstats.plots as qsplot

def format_pct_axis(x, _):
    x *= 100  # lambda x, loc: "{:,}%".format(int(x * 100))
    if x >= 1e12:
        res = '%1.1fT%%' % (x * 1e-12)
        return res.replace('.0T%', 'T%')
    if x >= 1e9:
        res = '%1.1fB%%' % (x * 1e-9)
        return res.replace('.0B%', 'B%')
    if x >= 1e6:
        res = '%1.1fM%%' % (x * 1e-6)
        return res.replace('.0M%', 'M%')
    if x >= 1e3:
        res = '%1.1fK%%' % (x * 1e-3)
        return res.replace('.0K%', 'K%')
    res = '%1.0f%%' % x
    return res.replace('.0%', '%')

def plot_longest_drawdowns(returns, dicclrs, periods=5, lw=1.5,
                           fontname='Avenir Next', grayscale=False,
                           log_scale=False, figsize=(10, 6), ylabel=True,
                           subtitle=True, compounded=True,
                           savefig=None, show=True):
    #colors = ['#348dc1', '#003366', 'red'] #inially
    colors = [dicclrs['arquant'], '#b5583c', dicclrs['background']] #ARQuant, Brown, Light Peach
    if grayscale: colors = ['#000000'] * 3
    
    import matplotlib.pyplot as plt
    import matplotlib.dates as _mdates
    import quantstats.stats as _stats
    from matplotlib.ticker import (
    FormatStrFormatter as _FormatStrFormatter,
    FuncFormatter as _FuncFormatter)

    dd = _stats.to_drawdown_series(returns.fillna(0))
    dddf = _stats.drawdown_details(dd)
    longest_dd = dddf.sort_values(by='days', ascending=False, 
                                  kind='mergesort')[:periods]

    fig, ax = plt.subplots(figsize=figsize)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # fig.suptitle("Top %.0f Drawdown Periods\n" %
    #               periods, y=1.1, x=0.25, 
    #               fontweight="normal", fontname=fontname,
    #               fontsize=18, color=dicclrs['plotname'])
    if subtitle:
        # plt.rc('text', usetex=True)
        # plt.title(r'\fontsize{30pt}{3em}\selectfont{}{Mean WRFv3.5 LHF\r}{\fontsize{18pt}{3em}\selectfont{}(September 16 - October 30, 2012)}')

        plt.title("", loc='left', #Top %.0f Drawdown Periods\n %periods
                  fontweight="medium", fontname=fontname,
                  fontsize=18, color=dicclrs['plotname'])
        
        dates= " Top %.0f Drawdown Periods | %s - %s " %(
            periods,
            returns.index.date[:1][0].strftime('%e %b \'%y'),
            returns.index.date[-1:][0].strftime('%e %b \'%y')
            )

        import json
        with open('slide2.txt', 'w') as outfile:
            json.dump(dates, outfile)
            

        # plt.title(dates, loc='center')
        # plt.text(0.45, 0.97, dates, 
        #           fontdict=dict(fontweight='normal', fontname=fontname,
        #           fontsize=14, color=dicclrs['dates']),
        #           transform=fig.transFigure
        #           )
    #Plot the line
    fig.set_facecolor('white')
    ax.set_facecolor('white')
    series = _stats.compsum(returns) if compounded else returns.cumsum()
    ax.plot(series, lw=lw, label="Backtest", color=colors[0])
    #PLot spans
    highlight = 'black' if grayscale else dicclrs['background'] # it was initially 'red'
    for _, row in longest_dd.iterrows():
        ax.axvspan(*_mdates.datestr2num([str(row['start']), str(row['end'])]),
                   color=highlight, alpha=.5)
    ## Horizontal line for 0%
    ax.axhline(0, ls="-", lw=1, color="#000000", zorder=2)
    
    ## X -axis
    # rotate and align the tick labels so they look better
    # fig.autofmt_xdate()
    fig.autofmt_xdate(bottom=0.2, rotation=0, ha='center', which=None)
    # use a more precise date string for the x axis locations in the toolbar    
    ax.fmt_xdata = _mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_tick_params(labelsize=8, color=dicclrs['dates'])
    
    ## Y -axis
    plt.yscale("symlog" if log_scale else "linear")
    if ylabel:
        ax.set_ylabel("Cumulative Returns", fontname=fontname,
                      fontweight='medium', fontsize=12, color="black")
        ax.yaxis.set_label_coords(-.075, .5)

    ax.yaxis.set_major_formatter(_FuncFormatter(format_pct_axis))
    # ax.yaxis.set_major_formatter(plt.FuncFormatter(
    #     lambda x, loc: "{:,}%".format(int(x*100))))

    ax.yaxis.set_tick_params(labelsize=8)

    try:
        plt.subplots_adjust(hspace=0, bottom=0, top=1)
    except Exception:
        pass

    try:
        fig.tight_layout()
    except Exception:
        pass
    
    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig, dpi=300)
        else:
            plt.savefig(savefig, dpi=300)

    if show:
        plt.show(block=False)

    plt.close()

    if not show:
        return fig

    return None

def f_xticks(dfs_sim1):
    import numpy as np
    long=dfs_sim1.shape[0]
    if long in range(1,7): step=1
    elif long in range(7,13): step=2
    elif long in range(13,25): step=4
    elif long in range(25,37): step=6
    elif long in range(37,49): step=8    
    else: step=long//8
    # filtering dates for ticks
    if step ==1:
        x_ticks=dfs_sim1.index.astype(str).values
    elif step in range(2,6):
        x_ticks=dfs_sim1.iloc[np.arange(1,long+1, step)].index.astype(str).values
    else:
        x_ticks=dfs_sim1.iloc[np.linspace(0,long-1, step)].index.astype(str).values
    return x_ticks

# plotname='AVESA- Andrew vs Indexies since Inception'
def plot_for_print(dfs_sim1, dicclrs, datadir='Traders/Data/', 
                   plotname='ARQuant-',
                   figsize=(10,6),
                   c=['b','r','g', 'm', 'y', 'c', 'k'],
                   marker=['o','^', (8,2,0), 'v', '*', '+', 'd'],
                   ls=['-','--','-.', ':', '--','-.', ':'],
                   fontname='Avenir Next', ylabel=True,
                   subtitle=True, show=True
                   ):
    import matplotlib.ticker as mtick
    import matplotlib.pyplot as plt
    import matplotlib.dates as _mdates #DateFormatter, AutoDateLocator, AutoDateFormatter, datestr2num
    from matplotlib.ticker import (FormatStrFormatter as _FormatStrFormatter,
                                    FuncFormatter as _FuncFormatter)

    x=dfs_sim1.index.astype(str).values
    # x = _mdates.datestr2num(dfs_sim1.index.astype(str).values)    

    y=dfs_sim1
    # ymin=y.min(axis=0).min(axis=1)
    # ymax=y.max(axis=0).max(axis=1)

    fig1, ax1 = plt.subplots(figsize=figsize)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    
    fig1.set_facecolor('white')
    ax1.set_facecolor('white')

    for col in range(len(y.columns)):    
        ax1.plot(x, y.iloc[:,col], c=c[col], marker=marker[col], ls=ls[col],label=y.columns[col])

    # Y-axis
    if ylabel:
        plt.ylabel('Cumulative Returns\n ', fontsize=13, fontweight='medium')
        ax1.yaxis.set_major_formatter(mtick.PercentFormatter())
    #X-axis
    x_ticks=f_xticks(dfs_sim1)
    # long=dfs_sim1.shape[0]
    # if long in range(1,7): step=1
    # elif long in range(7,13): step=2
    # elif long in range(13,25): step=4
    # elif long in range(25,37): step=6
    # elif long in range(37,49): step=8    
    # else: step=long/8
    # # filtering dates for ticks
    # if step ==1:
    #     x_ticks=dfs_sim1.index.astype(str).values
    # elif step in range(2,6):
    #     x_ticks=dfs_sim1.iloc[np.arange(1,long+1, step)].index.astype(str).values
    # else:
    #     x_ticks=dfs_sim1.iloc[np.linspace(0,long-1, step)].index.astype(str).values
    plt.xticks(x_ticks) # setting ticks
    ax1.set_xticklabels(x_ticks) # setting labels for ticks
    # Positioning ticks
    fig1.autofmt_xdate(bottom=0.2, rotation=0, ha='center', which=None)
    # Sizing and coloring ticks
    ax1.xaxis.set_tick_params(labelsize=8, color=dicclrs['dates'])
    
    ax1.legend()
    
    if subtitle:
    # plt.rc('text', usetex=True)
    # plt.title(r'\fontsize{30pt}{3em}\selectfont{}{Mean WRFv3.5 LHF\r}{\fontsize{18pt}{3em}\selectfont{}(September 16 - October 30, 2012)}')

        plt.title(" ", loc='left', #ARQuant Strategy vs Benchmarks
                  fontweight="medium", fontname=fontname,
                  fontsize=18, color=dicclrs['plotname'])
        
        dates= "  %s - %s " %(
            dfs_sim1.index.to_timestamp(how='start').date[:1][0].strftime('%e %b \'%y'),
            dfs_sim1.index.to_timestamp(how='end').date[-1:][0].strftime('%e %b \'%y')
            )
        import json
        with open('slide1.txt', 'w') as outfile:
            json.dump(dates, outfile)
        # plt.title(dates, loc='center')
        # plt.text(0.56, 0.92, dates, 
        #           fontdict=dict(fontweight='normal', fontname=fontname,
        #           fontsize=14, color=dicclrs['dates']),
        #           transform=fig1.transFigure
        #           )
    # plt.savefig(datadir+plotname+'.png',dpi=400)
    figure = ax1.get_figure()
    figure.savefig(datadir+plotname+'.png', dpi=400, bbox_inches='tight')
    if show: plt.show()
    return

def regime_plot(vix, lower=16.5, upper =  19.5, ylabel='VIX', figsize=(10,6)):

    # Each term inside parentheses is [False, True, ...]
    # Both terms must be True element-wise for a trigger to occur
    blue = (vix < upper) & (vix.shift() >= upper)
    yellow = (vix < lower) & (vix.shift() >= lower)
    green = (vix > upper) & (vix.shift() <= upper)
    red = (vix > lower) & (vix.shift() <= lower)
    
    mapping = {1: 'blue', 2: 'yellow', 3: 'green', 4: 'red'}
    
    indicator = pd.Series(np.where(blue, 1., np.where(yellow, 2.,
                          np.where(green, 3., np.where(red, 4., np.nan)))),
                          index=vix.index).ffill().map(mapping).dropna()
    vix = vix.reindex(indicator.index)

    import matplotlib.pyplot as plt        
    fig, ax = plt.subplots(figsize=figsize)
    plt.scatter(vix.index, vix, c=indicator, marker='.')
    plt.title(ylabel+' regime')
    plt.ylabel(ylabel)
    
    # x_ticks=f_xticks(vix)
    # setting labels for ticks
    # ax.set_xticklabels(x_ticks) 
    import matplotlib.dates as mdates
    # all your fancy plotting code
    locator=mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))

    # Positioning ticks
    fig.autofmt_xdate(bottom=0.2, rotation=0, ha='center', which=None)
    # Sizing and coloring ticks
    ax.xaxis.set_tick_params(labelsize=8, color=dicclrs['dates'])
    plt.show()
    return

def period_index(df, period_list):
    periods={}
    for per in period_list:
        if per=='Inception':    periods[per]=df.index
        elif per=='YTD':        periods[per]=df.loc[str(dt.date.today().year)]
        elif per[0]=='2':       periods[per]=df.loc[per].index
        elif per[0]=='L':
            if isinstance(df.index, pd.PeriodIndex): 
                p=per[1:]
                p=int(p[:-1])
                periods[per]=df.index[-p:]
            else: periods[per]=df.last(per[1:]).index
        else: continue
    return periods

def read_csv(datadir, filename='AVESA_Group_Ltd_U3577443_history.csv'):
    andrew_ret=pd.read_csv(datadir+filename, engine='python')
    andrew_ret['Date']=pd.to_datetime(andrew_ret['Date'], 
                                  infer_datetime_format='%Y-%m-%d')
    andrew_ret.set_index(['Date'], inplace=True)
    return andrew_ret