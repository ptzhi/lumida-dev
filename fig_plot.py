import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_master import *
import fig_format

#######################################################################
# CRYPTO INDEX
#######################################################################

# Figure 1: Index Spread ------------------------------------------------

def plot_spread_index(trailing, start_date, end_date, min_cap, max_cap):
    coin_list=coin_cap.columns[coin_cap.iloc[-2].between(min_cap*10**9,max_cap*10**9)]
    
    price_index = index_dict['spy'].loc[start_date:end_date][' Open']
    zscore_index = (price_index - price_index.rolling(trailing).mean())/price_index.rolling(trailing).std()
        
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=index_df(coin_list, trailing).loc[start_date:end_date].index,
            y=index_df(coin_list, trailing).loc[start_date:end_date][f'{trailing}maZ'],
            name=f'{trailing}ma crypto',
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=index_dict['spy'].loc[start_date:end_date].index,
            y=zscore_index,
            name=f'{trailing}ma spy'
        ),
        secondary_y=True,
    )
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=1,
                  x1=end_date,
                  y1=2,
                  line=dict(color='Red'),
                  fillcolor='red',
                  opacity=0.1,)
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=2,
                  x1=end_date,
                  y1=4,
                  line=dict(color='Red'),
                  fillcolor='red',
                  opacity=0.25,)
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=-1,
                  x1=end_date,
                  y1=-2,
                  line=dict(color='green'),
                  fillcolor='green',
                  opacity=0.1,)
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=-2,
                  x1=end_date,
                  y1=-4,
                  line=dict(color='green'),
                  fillcolor='green',
                  opacity=0.25,)
    fig.update_yaxes(
        range = [
            -4,4         
        ]
    )
    fig.update_traces(
        # overwrite=True,
        visible='legendonly',
        selector=lambda t: not t.name in [f'{trailing}ma crypto'],
    )
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text': f'Cap-weighted Index {trailing}ma Spread ',
        },
    )
    return fig

# Figure 2: Overbought Table --------------------------------------------

def plot_table_index_overbought(trailing, start_date, end_date, min_cap, max_cap):
    coin_list=coin_cap.columns[coin_cap.iloc[-2].between(min_cap*10**9,max_cap*10**9)]
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[
                        'Token',
                        'Price',
                        '7d ret%',
                        'Cap (bn)',
                        'Z Score',
                    ]
                ),
                cells=dict(
                    values=[
                   		#tokens
                       zscore_df(coin_list, trailing).iloc[-1][zscore_df(coin_list, trailing).iloc[-1]>1].sort_values(ascending=False).index,
                       #price
                       coin_price[[token for token in zscore_df(coin_list, trailing).iloc[-1][zscore_df(coin_list, trailing).iloc[-1]>1].sort_values(ascending=False).index]].iloc[-1].round(2),
                       #7day returns
                       (coin_price[[token for token in zscore_df(coin_list, trailing).iloc[-1][zscore_df(coin_list, trailing).iloc[-1]>1].sort_values(ascending=False).index]].pct_change(7).iloc[-1]*100).map('{:.2f}%'.format),
                       #market cap
                       (coin_cap[[token for token in zscore_df(coin_list, trailing).iloc[-1][zscore_df(coin_list, trailing).iloc[-1]>1].sort_values(ascending=False).index]].iloc[-2]/10**9).round(2),
                       #zscores
                       zscore_df(coin_list, trailing).iloc[-1][zscore_df(coin_list, trailing).iloc[-1]>1].sort_values(ascending=False).round(2), 
                       

                   		# #tokens
                     #   coin_zscore[coin_list].iloc[-1][coin_zscore[coin_list].iloc[-1]>1].sort_values(ascending=False).index,
                     #   #price
                     #   coin_price[[token for token in coin_zscore[coin_list].iloc[-1][coin_zscore[coin_list].iloc[-1]>1].sort_values(ascending=False).index]].iloc[-1].round(2),
                     #   #7day returns
                     #   (coin_price[[token for token in coin_zscore[coin_list].iloc[-1][coin_zscore[coin_list].iloc[-1]>1].sort_values(ascending=False).index]].pct_change(7).iloc[-1]*100).map('{:.2f}%'.format),
                     #   #market cap
                     #   (coin_cap[[token for token in coin_zscore[coin_list].iloc[-1][coin_zscore[coin_list].iloc[-1]>1].sort_values(ascending=False).index]].iloc[-2]/10**9).round(2),
                     #   #zscores
                     #   coin_zscore[coin_list].iloc[-1][coin_zscore[coin_list].iloc[-1]>1].sort_values(ascending=False).round(2), 
                    ]
                )
            )
        ]
    )
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text': f'Overbought Tokens on {end_date}',
        },
    )
    return fig


# Figure 3: Oversold Table --------------------------------------------

def plot_table_index_oversold(trailing, start_date, end_date, min_cap, max_cap):
    
    coin_list=coin_cap.columns[coin_cap.iloc[-2].between(min_cap*10**9,max_cap*10**9)]
    
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[
                        'Token',
                        'Price',
                        '7d ret%',
                        'Cap (bn)',
                        'Z Score',
                    ]
                ),
                cells=dict(
                    values=[
                    #token
                    zscore_df(coin_list, trailing).iloc[-1][zscore_df(coin_list, trailing).iloc[-1]<-1].sort_values().index,
                    #price
                    coin_price[[token for token in zscore_df(coin_list, trailing).iloc[-1][zscore_df(coin_list, trailing).iloc[-1]<-1].sort_values().index]].iloc[-1].round(2),
                    #ret
                    (coin_price[[token for token in zscore_df(coin_list, trailing).iloc[-1][zscore_df(coin_list, trailing).iloc[-1]<-1].sort_values().index]].pct_change(7).iloc[-1]*100).map('{:.2f}%'.format),
                    #cap
                    (coin_cap[[token for token in zscore_df(coin_list, trailing).iloc[-1][zscore_df(coin_list, trailing).iloc[-1]<-1].sort_values().index]].iloc[-2]/10**9).round(2),
                    #z score
                    zscore_df(coin_list, trailing).iloc[-1][zscore_df(coin_list, trailing).iloc[-1]<-1].sort_values().round(2),
                    ]
                )
            )
        ]
    )
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text': f'Oversold Tokens on {end_date}',
        },
    )
    return fig


# Figure 4: Coin SPY Price ------------------------------------------------

def plot_coin_spy_price(coin, trailing, start_date, end_date):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].loc[start_date:end_date].index,
            y=coin_price[coin].loc[start_date:end_date],
            name=coin,
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=index_dict['spy'].loc[start_date:end_date].index,
            y=index_dict['spy'].loc[start_date:end_date][' Open'],
            name='spy',
            # opacity=0.75,
            line=dict(width=1),
        ),
        secondary_y=True,

    )
    # fig.update_traces(
    #     # overwrite=True,
    #     visible='legendonly',
    #     selector=lambda t: not t.name in [coin],
    # )
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text':f'{coin} + spy price',
        },
    )  
    return fig


# Figure 5: Coin MA --------------------------------------------
def plot_ma_coin(coin, trailing, start_date, end_date):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].loc[start_date:end_date].index,
            y=coin_price[coin].loc[start_date:end_date],
            name=f'{coin} price'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].loc[start_date:end_date].index,
            y=coin_price[coin].loc[start_date:end_date].rolling('300d').mean(),
            name=f'{coin} 300ma'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].loc[start_date:end_date].index,
            y=coin_price[coin].loc[start_date:end_date].rolling('60d').mean(),
            name=f'{coin} 60ma'
        )
    )
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text': f'{coin} 60/300dma',
        },
    )
    return fig

# Figure 6: Drawdowns -------------------------------------------------------
def plot_drawdown_coin(coin, trailing, start_date, end_date):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].index,
            y=(1-coin_price[coin]/coin_price[coin].cummax()),
            name='dd%',
        )
    )
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].index,
            y=[(1-coin_price[coin]/coin_price[coin].cummax())[-1]]*len(coin_price[coin].index),
            name='current dd%',
            line=dict(
                # color='royalblue',
                # width=4,
                dash='dot'
            )
        )
    )
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].index,
            y=[(1-coin_price[coin]/coin_price[coin].cummax()).mean()]*len(coin_price[coin].index),
            name='avg dd%',
            line=dict(
                color='royalblue',
                # width=4,
                dash='dot'
            )
        )
    )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis,autorange='reversed',rangemode='tozero')
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text': f'{coin} Drawdowns',
        },
    )
    return fig


###############################################################################
# COIN SPREAD SMA OS/OB
###############################################################################

# Figure 1: COIN SPREAD ------------------------------------------------

def plot_spread_coin_index(coin, trailing, start_date, end_date):
    price_coin = coin_price[coin].loc[start_date:end_date]
    zscore_coin = (price_coin - price_coin.rolling(trailing).mean())/price_coin.rolling(trailing).std()
    
    price_index = index_dict['spy'].loc[start_date:end_date][' Open']
    zscore_index = (price_index - price_index.rolling(trailing).mean())/price_index.rolling(trailing).std()
    
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].loc[start_date:end_date].index,
            y=zscore_coin,
            name=f'{trailing}ma {coin}'
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=index_dict['spy'].loc[start_date:end_date].index,
            y=zscore_index,
            name=f'{trailing}ma spy',
            opacity=0.75,
            # line=dict(width=1),
        ),
        secondary_y=True,
    )
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=1,
                  x1=end_date,
                  y1=2,
                  line=dict(color='Red'),
                  fillcolor='red',
                  opacity=0.1,)
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=2,
                  x1=end_date,
                  y1=4,
                  line=dict(color='Red'),
                  fillcolor='red',
                  opacity=0.25,)
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=-1,
                  x1=end_date,
                  y1=-2,
                  line=dict(color='green'),
                  fillcolor='green',
                  opacity=0.1,)
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=-2,
                  x1=end_date,
                  y1=-4,
                  line=dict(color='green'),
                  fillcolor='green',
                  opacity=0.25,)
    fig.update_yaxes(
        range = [
            -4,4
            
        ]
    )
    fig.update_traces(
        # overwrite=True,
        visible='legendonly',
        selector=lambda t: not t.name in [f'{trailing}ma {coin}'],
    )
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text': f'{trailing}ma spread {coin} + spy (toggle)',
        },
    )
    return fig
    
# Figure 1: COIN Log Price ------------------------------------------------

def plot_log_price(coin, trailing, start_date, end_date):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].loc[start_date:end_date].index,
            y=coin_price[coin].loc[start_date:end_date]
        )
    )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis, type='log', zeroline=True, zerolinecolor='rgba(255, 255, 255, 0.5)',
)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text':'Log Price',
        },
    )  
    return fig
    
    
# Figure 5:COIN Overbought SUMMARY -------------------------------

def plot_table_overbought_coin_summary(coin, trailing, start_date, end_date,rolling, obthreshold):    
    price = coin_price[coin].loc[start_date:end_date]
    
    zscore = (price - price.rolling(trailing).mean())/price.rolling(trailing).std()
    
    zscore_roll = zscore.rolling(rolling).mean()
    
    days = [7, 30, 60, 90, 180, 360]

    column_headers = [' ',]
    
    values=[
    # 1st col
        [
        'Mean Returns',
        'Median Returns',
        'Count of Ups',
        'Count of Downs',
        'All Mean Returns'
        ]
    ]
    
    for day in days:
        ret = (coin_price[coin].pct_change(day).shift(-day)*100).loc[zscore_roll[zscore_roll>=int(obthreshold)].index]

        mean = "{:.2f}".format(ret.mean())

        median = "{:.2f}".format(ret.median())

        number_up = ret[ret>0].count()

        number_down = ret[ret<0].count()

        all_mean = "{:.2f}".format((coin_price[coin].loc[start_date:end_date].pct_change(day).shift(-day)*100).mean())
    
        values.append([mean, median, number_up, number_down, all_mean])
        column_headers.append(f'{day}d ret%')
    
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=column_headers
                ),
                cells=dict(
                    values=values,
#                     fill_color=[
                        
#                     ]
                )
            )
        ]
    )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text': f'SUMMARY Overbought on {rolling}ma zscore, {trailing}ma price, zscore >= {obthreshold}',
        },
    )
    return fig

# Figure 6:COIN Oversold SUMMARY -------------------------------

def plot_table_oversold_coin_summary(coin, trailing, start_date, end_date,rolling, osthreshold):    
    price = coin_price[coin].loc[start_date:end_date]
    
    zscore = (price - price.rolling(trailing).mean())/price.rolling(trailing).std()
    
    zscore_roll = zscore.rolling(rolling).mean()
    
    days = [7, 30, 60, 90, 180, 360]

    column_headers = [' ',]
    
    values=[
    # 1st col
        [
        'Mean Returns',
        'Median Returns',
        'Count of Ups',
        'Count of Downs',
        'All Mean Returns'
        ]
    ]
    
    for day in days:
        ret = (coin_price[coin].pct_change(day).shift(-day)*100).loc[zscore_roll[zscore_roll<=int(osthreshold)].index]

        mean = "{:.2f}".format(ret.mean())

        median = "{:.2f}".format(ret.median())

        number_up = ret[ret>0].count()

        number_down = ret[ret<0].count()

        all_mean = "{:.2f}".format((coin_price[coin].loc[start_date:end_date].pct_change(day).shift(-day)*100).mean())
    
        values.append([mean, median, number_up, number_down, all_mean])
        column_headers.append(f'{day}d ret%')
    
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=column_headers
                ),
                cells=dict(
                    values=values
#                     fill_color=[
                        
#                     ]
                )
            )
        ]
    )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text': f'SUMMARY Oversold on {rolling}ma zscore, {trailing}ma price, zscore <= {osthreshold}',
        },
    )
    return fig
    

###############################################################################
# NEW PAGE: OB OS DETAILS
###############################################################################

# Figure 2: COIN SMA Spread ------------------------------------------------

def plot_spread_price(coin, trailing, start_date, end_date):
    price = coin_price[coin].loc[start_date:end_date]
    zscore = (price - price.rolling(trailing).mean())/price.rolling(trailing).std()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].loc[start_date:end_date].index,
            y=zscore,
            name=f'{trailing}ma spread'
        )
    )
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=1,
                  x1=end_date,
                  y1=2,
                  line=dict(color='Red'),
                  fillcolor='red',
                  opacity=0.1,)
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=2,
                  x1=end_date,
                  y1=4,
                  line=dict(color='Red'),
                  fillcolor='red',
                  opacity=0.25,)
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=-1,
                  x1=end_date,
                  y1=-2,
                  line=dict(color='green'),
                  fillcolor='green',
                  opacity=0.1,)
    fig.add_shape(type='rect',
                  x0=start_date,
                  y0=-2,
                  x1=end_date,
                  y1=-4,
                  line=dict(color='green'),
                  fillcolor='green',
                  opacity=0.25,)
    fig.update_yaxes(
        range = [
            -4,4
            
        ]
    )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text': f'{coin} {trailing}ma Spread ',
        },
    )
    return fig
    
    
# Figure 3:COIN Overbought table ------------------------------------------------

def plot_table_overbought_coin(coin, trailing, start_date, end_date,rolling, obthreshold):    
	# coin price
    price = coin_price[coin].loc[start_date:end_date]
    # coin zscore all
    zscore = (price - price.rolling(trailing).mean())/price.rolling(trailing).std()
    # coin zscore trailing
    zscore_roll = zscore.rolling(rolling).mean()
	# event date
    zscore_threshold_date = zscore_roll[zscore_roll>=int(obthreshold)].index.date
	# event z score
    zscore_threshold_value = zscore_roll[zscore_roll>=int(obthreshold)].map('{:.1f}'.format)

	# set up for loop for table values
    days = [7, 30, 60, 90, 180, 360]
    column_headers = [
    	'Event Date',
	     f'{rolling} sma',
    ]
    values = [
		zscore_threshold_date,
		zscore_threshold_value,
    ]
    for day in days:
        ret = (coin_price[coin].pct_change(day).shift(-day).fillna(0)*100).map('{:.1f}'.format).loc[zscore_roll[zscore_roll>=int(obthreshold)].index]
        values.append(ret)
        column_headers.append(f'{day}d ret%')

	# plot the table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=column_headers
                ),
                cells=dict(
                	values = values,
                 	font_size=10,
                )
            )
        ]
    )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        height=500,
        title={
            'text': f'Overbought on {rolling}ma zscore, {trailing}ma price, zscore >= {obthreshold}',
        },
    )
    return fig
    
# Figure 4: COIN Oversold table ------------------------------------------------

def plot_table_oversold_coin(coin, trailing, start_date, end_date,rolling, osthreshold):    
	# coin price
    price = coin_price[coin].loc[start_date:end_date]
    # coin zscore all
    zscore = (price - price.rolling(trailing).mean())/price.rolling(trailing).std()
    # coin zscore trailing
    zscore_roll = zscore.rolling(rolling).mean()
	# event date
    zscore_threshold_date = zscore_roll[zscore_roll<=int(osthreshold)].index.date
	# event z score
    zscore_threshold_value = zscore_roll[zscore_roll<=int(osthreshold)].map('{:.1f}'.format)

	# set up for loop for table values
    days = [7, 30, 60, 90, 180, 360]
    column_headers = [
    	'Event Date',
	     f'{rolling} sma',
    ]
    values = [
		zscore_threshold_date,
		zscore_threshold_value,
    ]
    for day in days:
        ret = (coin_price[coin].pct_change(day).shift(-day).fillna(0)*100).map('{:.1f}'.format).loc[zscore_roll[zscore_roll<=int(osthreshold)].index]
        values.append(ret)
        column_headers.append(f'{day}d ret%')

	# plot the table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=column_headers
                ),
                cells=dict(
                	values = values,
                 	font_size=10,
                )
            )
        ]
    )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        height=500,
        title={
            'text': f'Oversold on {rolling}ma zscore, {trailing}ma price, zscore <= {osthreshold}',
        },
    )
    return fig

###############################################################################
# MACD simple moving average
###############################################################################

# Create MACD variables -----------------------------------------------------
# def variables_macd_sma(coin, macd1ma, macd2ma, signalma, start_date, end_date):

# macd1ma = 12
# macd2ma = 26
# signalma = 9

# def macd_sma(coin, macd1ma, macd2ma, signalma, start_date, end_date):
#     sma12 = coin_price[coin].rolling(macd1ma).mean().fillna(0).loc[start_date:end_date]
#     sma26 = coin_price[coin].rolling(macd2ma).mean().fillna(0).loc[start_date:end_date]
#     macd_sma = sma12 - sma26
#     return macd_sma

# def macd_sma_signal(signalma):
#     macd_sma_signal = macd_sma(coin, macd1ma, macd2ma, signalma, start_date, end_date).rolling(signalma).mean().fillna(0)   
#     return macd_sma_signal

# def macd_sma_cross():
#     macd_sma_cross = macd_sma(coin, macd1ma, macd2ma, signalma, start_date, end_date) - macd_sma_signal(signalma)
#     return macd_sma_cross
    
# def cross_dates(start_date, end_date):
#     cross_trigger = macd_sma_cross().shift(1)/macd_sma_cross()
#     cross_dates = [pd.to_datetime(start_date)] + list(cross_trigger[cross_trigger<0].index) + [pd.to_datetime(end_date)]
#     return cross_dates

# def macd_ret():
#     # get signal on day n, implement trade day after n+1, shorting
#     macd_ret = []
#     for i in range(0,len(cross_dates(start_date, end_date))-1):
#         cross_start = cross_dates(start_date, end_date)[i] + pd.Timedelta(1, unit='D')
#         cross_end = cross_dates(start_date, end_date)[i+1]
#         if macd_sma_cross().loc[cross_dates(start_date, end_date)[i]] > 0:
#             macd_ret.append((coin_price['btc'].loc[cross_end]/coin_price['btc'].loc[cross_start] - 1))
#         else:
#             macd_ret.append((-(coin_price['btc'].loc[cross_end]/coin_price['btc'].loc[cross_start] - 1))) 
#     return macd_ret
    
# def macd_ret_sell():
#     # get signal on day n, implement trade day after n+1, sell only
#     macd_ret_sell = []
#     for i in range(0,len(cross_dates(start_date, end_date))-1):
#         cross_start = cross_dates(start_date, end_date)[i] + pd.Timedelta(1, unit='D')
#         cross_end =cross_dates(start_date, end_date)[i+1]
#         if macd_sma_cross().loc[cross_dates()[i]] > 0:
#             macd_ret_sell.append((coin_price['btc'].loc[cross_end]/coin_price['btc'].loc[cross_start] - 1))
#         else:
#             macd_ret_sell.append(0) 
#     return macd_ret_sell
    
# def eq_btc_ts(start_date, end_date):
#     eq_btc= 100
#     eq_btc_ts = []
#     for ret in (coin_price[coin].pct_change(1)+1).loc[start_date:end_date]:
#         eq_btc = eq_btc*ret
#         eq_btc_ts.append(eq_btc)
#     return eq_btc_ts
    
# def eq_macd_sma_ts():
#     eq_macd_sma = 100
#     eq_macd_sma_ts = []
#     for ret in [x+1 for x in macd_ret()]:
#         eq_macd_sma = eq_macd_sma*ret
#         eq_macd_sma_ts.append(eq_macd_sma)
#     return eq_macd_sma_ts
    
# def eq_macd_sma_sell_ts():
#     eq_macd_sma_sell = 100
#     eq_macd_sma_sell_ts = []
#     for ret in [x+1 for x in macd_ret_sell()]:
#         eq_macd_sma_sell = eq_macd_sma_sell*ret
#         eq_macd_sma_sell_ts.append(eq_macd_sma_sell)
#     return eq_macd_sma_sell_ts

# Figure 1: MACD SMA Coin ------------------------------------------------
# def plot_macd_sma(coin, macd1ma, macd2ma, signalma, start_date, end_date):

macd1ma = 12
macd2ma = 26
signalma = 9

def plot_macd_sma(coin, start_date, end_date):

    
    sma12 = coin_price[coin].rolling(macd1ma).mean().fillna(0).loc[start_date:end_date]
    sma26 = coin_price[coin].rolling(macd2ma).mean().fillna(0).loc[start_date:end_date]
    macd_sma = sma12 - sma26
    macd_sma_signal = macd_sma.rolling(signalma).mean().fillna(0)
    macd_sma_cross = macd_sma - macd_sma_signal

    macd_sma_over = macd_sma_cross[macd_sma_cross>0]
    macd_sma_under = macd_sma_cross[macd_sma_cross<0]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].loc[start_date:end_date].index,
            y=coin_price[coin].loc[start_date:end_date],
            name=f'{coin} price',
            line=dict(width=1),
            opacity=0.9,
        ),
        secondary_y=True,
        
    )
    fig.add_trace(
        go.Bar(
            x=macd_sma_under.index,
            y=macd_sma_under,
            name=f'MACD short',
        ),
        secondary_y=False,

    )
    fig.add_trace(
        go.Bar(
            x=macd_sma_over.index,
            y=macd_sma_over,
            name=f'MACD long',
        ),
        secondary_y=False,

    )
    fig.add_trace(
        go.Scatter(
            x=macd_sma.index,
            y=macd_sma,
            name=f'MACD line',
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=macd_sma_signal.index,
            y=macd_sma_signal,
            name=f'Signal line',
        ),
        secondary_y=False,

    )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text':f'{coin} MACD SMA {macd1ma}d/{macd2ma}d cross {signalma}d signal',
        },
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.1
        )
    )  
    return fig



# Figure 2: MACD SMA Equity Value ----------------------------------------


# def plot_macd_sma_eqv(coin, macd1ma, macd2ma, signalma, start_date, end_date):

def plot_macd_sma_eqv(coin,start_date, end_date):
    
    
    sma12 = coin_price[coin].rolling(macd1ma).mean().fillna(0).loc[start_date:end_date]
    sma26 = coin_price[coin].rolling(macd2ma).mean().fillna(0).loc[start_date:end_date]
    macd_sma = sma12 - sma26
    macd_sma_signal = macd_sma.rolling(signalma).mean().fillna(0)
    macd_sma_cross = macd_sma - macd_sma_signal
    
    cross_trigger = macd_sma_cross.shift(1)/macd_sma_cross
    cross_dates = [pd.to_datetime(start_date)] + list(cross_trigger[cross_trigger<0].index) + [pd.to_datetime(end_date)]
    
    # get signal on day n, implement trade day after n+1, WITH SHORTING
    macd_ret = []
    for i in range(0,len(cross_dates)-1):
        cross_start = cross_dates[i] + pd.Timedelta(1, unit='D')
        cross_end = cross_dates[i+1]
        if macd_sma_cross.loc[cross_dates[i]] > 0:
            macd_ret.append((coin_price['btc'].loc[cross_end]/coin_price['btc'].loc[cross_start] - 1))
        else:
            macd_ret.append(-((coin_price['btc'].loc[cross_end]/coin_price['btc'].loc[cross_start] - 1))) 
    
    # get signal on day n, implement trade day after n+1, NO SHORTING
    macd_ret_sell = []
    for i in range(0,len(cross_dates)-1):
        cross_start = cross_dates[i] + pd.Timedelta(1, unit='D')
        cross_end = cross_dates[i+1]
        if macd_sma_cross.loc[cross_dates[i]] > 0:
            macd_ret_sell.append((coin_price['btc'].loc[cross_end]/coin_price['btc'].loc[cross_start] - 1))
        else:
            macd_ret_sell.append(0) 
    
    eq_btc= 100
    eq_btc_ts = []
    for ret in (coin_price[coin].pct_change(1)+1).loc[start_date:end_date]:
        eq_btc = eq_btc*ret
        eq_btc_ts.append(eq_btc)
    
    eq_macd_sma = 100
    eq_macd_sma_ts = []
    for ret in [x+1 for x in macd_ret]:
        eq_macd_sma = eq_macd_sma*ret
        eq_macd_sma_ts.append(eq_macd_sma)
    
    
    eq_macd_sma_sell = 100
    eq_macd_sma_sell_ts = []
    for ret in [x+1 for x in macd_ret_sell]:
        eq_macd_sma_sell = eq_macd_sma_sell*ret
        eq_macd_sma_sell_ts.append(eq_macd_sma_sell)
        
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=coin_price[coin].loc[start_date:end_date].index,
            y=eq_btc_ts[:-1],
            name=f'{coin} hold',
        ),        
    )
    fig.add_trace(
        go.Scatter(
            x=macd_sma_cross.loc[cross_dates].index[:-1],
            y=eq_macd_sma_ts,
            name=f'MACD w/ short',
        ),
    )
    fig.add_trace(
        go.Scatter(
            x=macd_sma_cross.loc[cross_dates].index[:-1],
            y=eq_macd_sma_sell_ts,
            name=f'MACD w/ sell',
        ),
    )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text':f'Equity Value of Holding {coin} versus Systematic MACD SMA w/ and w/o Shorting',
        },
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.1
        )
    )  
    return fig
    # return fig, macd_ret, eq_macd_sma_ts, eq_btc_ts


# Figure 3: MACD SMA over -------------------------------

def plot_table_macd_sma_over_summary(coin, start_date, end_date):    
    
    sma12 = coin_price[coin].rolling(macd1ma).mean().fillna(0).loc[start_date:end_date]
    sma26 = coin_price[coin].rolling(macd2ma).mean().fillna(0).loc[start_date:end_date]
    macd_sma = sma12 - sma26
    macd_sma_signal = macd_sma.rolling(signalma).mean().fillna(0)
    macd_sma_cross = macd_sma - macd_sma_signal

    macd_sma_over = macd_sma_cross[macd_sma_cross>0]
    # macd_sma_under = macd_sma_cross[macd_sma_cross<0]
    
    price = coin_price[coin].loc[start_date:end_date]
            
    days = [7, 30, 60, 90, 180, 360]

    column_headers = [' ',]
    
    values=[
    # 1st col
        [
        'Mean Returns',
        'Median Returns',
        'Count of Ups',
        'Count of Downs',
        'All Mean Returns'
        ]
    ]
    
    for day in days:
        # ret = (coin_price[coin].pct_change(day).shift(-day).fillna(0)*100).loc[macd_sma_over_roll[macd_sma_over_roll>=int(obthreshold)].index]
        
        ret = (coin_price[coin].pct_change(day).shift(-day).fillna(0)*100).loc[macd_sma_over.index]

        mean = "{:.2f}".format(ret.mean())

        median = "{:.2f}".format(ret.median())

        number_up = ret[ret>0].count()

        number_down = ret[ret<0].count()

        all_mean = "{:.2f}".format((coin_price[coin].loc[start_date:end_date].pct_change(day).shift(-day)*100).mean())
    
        values.append([mean, median, number_up, number_down, all_mean])
        column_headers.append(f'{day}d ret%')
    
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=column_headers
                ),
                cells=dict(
                    values=values,
#                     fill_color=[
                        
#                     ]
                )
            )
        ]
    )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text': f'SUMMARY MACD SMA over',
        },
    )
    return fig


# Figure 4:MACD SMA UNDER SUMMARY -------------------------------

def plot_table_macd_sma_under_summary(coin, start_date, end_date):    
    
    sma12 = coin_price[coin].rolling(macd1ma).mean().fillna(0).loc[start_date:end_date]
    sma26 = coin_price[coin].rolling(macd2ma).mean().fillna(0).loc[start_date:end_date]
    macd_sma = sma12 - sma26
    macd_sma_signal = macd_sma.rolling(signalma).mean().fillna(0)
    macd_sma_cross = macd_sma - macd_sma_signal

    macd_sma_under = macd_sma_cross[macd_sma_cross<0]
    # macd_sma_under = macd_sma_cross[macd_sma_cross<0]
    
    price = coin_price[coin].loc[start_date:end_date]
            
    days = [7, 30, 60, 90, 180, 360]

    column_headers = [' ',]
    
    values=[
    # 1st col
        [
        'Mean Returns',
        'Median Returns',
        'Count of Ups',
        'Count of Downs',
        'All Mean Returns'
        ]
    ]
    
    for day in days:
        # ret = (coin_price[coin].pct_change(day).shift(-day).fillna(0)*100).loc[macd_sma_over_roll[macd_sma_over_roll>=int(obthreshold)].index]
        
        ret = (coin_price[coin].pct_change(day).shift(-day).fillna(0)*100).loc[macd_sma_under.index]

        mean = "{:.2f}".format(ret.mean())

        median = "{:.2f}".format(ret.median())

        number_up = ret[ret>0].count()

        number_down = ret[ret<0].count()

        all_mean = "{:.2f}".format((coin_price[coin].loc[start_date:end_date].pct_change(day).shift(-day)*100).mean())
    
        values.append([mean, median, number_up, number_down, all_mean])
        column_headers.append(f'{day}d ret%')
    
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=column_headers
                ),
                cells=dict(
                    values=values,
#                     fill_color=[
                        
#                     ]
                )
            )
        ]
    )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    fig.update_layout(
        title={
            'text': f'SUMMARY MACD SMA under',
        },
    )
    return fig

###############################################################################
# Multicoin Dashboard - App Page with Plotly, Dash
###############################################################################

# Figure 1: Price ---------------------------------------------------------------
def plot_price(trailing, coin_list, start_date, end_date):
    fig = go.Figure()
    for coin in coin_list:
        fig.add_trace(
            go.Scatter(
                x=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)].resample(trailing, on='time').last().index,
                y=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)].resample(trailing, on='time').last()['price'],
                name=coin,opacity=0.75,
                hovertemplate ='$%{y:.2f}',
            )
        )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    return fig

# Figure 2: Log Price ------------------------------------------------------------
def plot_logprice(trailing, coin_list, start_date, end_date):
    fig = go.Figure()
    for coin in coin_list:
        fig.add_trace(
            go.Scatter(
                x=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)].resample(trailing, on='time').last().index, y=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)].resample(trailing, on='time').last()['price'],
                name=coin,opacity=0.75,
                hovertemplate ='$%{y:.2f}',
            )
        )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(type='log', zeroline=True, zerolinecolor='rgba(255, 255, 255, 0.5)',)
    fig.update_layout(fig_format.layout)
    return fig

# Figure 3: Returns ----------------------------------------------------------
def plot_returns(trailing, coin_list, start_date, end_date):
    fig = go.Figure()
    for coin in coin_list:
        if trailing == '1d':
            fig.add_trace(
                go.Scatter(
                    x=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)]['time'],
                    y=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)]['price'].pct_change(30).fillna(0),
                    name=coin,opacity=0.75,
                    hovertemplate ='%{y:.4f}',
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)]['time'],
                    y=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)]['price'].pct_change(int(trailing[:-1])).fillna(0),
                    name=coin,opacity=0.75,
                    hovertemplate ='%{y:.4f}',
                )
            )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    return fig

# Figure 4: Vol --------------------------------------------------------------
def plot_volatility(trailing, coin_list, start_date, end_date):
    fig = go.Figure()
    for coin in coin_list:
        if trailing == '1d':
            fig.add_trace(
                go.Scatter(
                    x=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)]['time'],
                    y=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)]['price'].pct_change(1).fillna(0).rolling(30).std().fillna(0),
                    name=coin,opacity=0.75,
                    hovertemplate ='%{y:.4f}',
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)]['time'],
                    y=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)]['price'].pct_change(1).fillna(0).rolling(int(trailing[:-1])).std().fillna(0),
                    name=coin,opacity=0.75,
                    hovertemplate ='%{y:.4f}',
                )
            )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    return fig

# Figure 5: Drawdown ---------------------------------------------------------
def plot_drawdown(trailing, coin_list, start_date, end_date):
    fig = go.Figure()
    for coin in coin_list:
        fig.add_trace(
            go.Scatter(
                x=coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)].resample(trailing, on='time')['price'].max().index,
                y=(1-coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)].set_index('time').price/coins_dict[coin][coins_dict[coin].time.between(start_date, end_date)].set_index('time').price.cummax()).resample(trailing).max(),
                name=coin,opacity=0.75,
                hovertemplate ='%{y:.4f}',
            )
        )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis,autorange='reversed',rangemode='tozero')
    fig.update_layout(fig_format.layout)
    return fig

# Figure 6: Pair-Wise Correlation -------------------------------------------------
# TO DO: DATE RANGE PICKE!!!!!!!!!!!!!
def plot_rollingcorr(trailing, coin_list, start_date, end_date):
    from itertools import combinations
    fig = go.Figure()
    comb_list=[]
    count = 0
    for i in combinations(coin_list,2):
        comb_list.append(i)
        count += 1
        df = pd.concat([coins_dict[comb_list[count-1][0]].set_index('time', drop=False).price.pct_change().fillna(0), coins_dict[comb_list[count-1][1]].set_index('time', drop=False).price.pct_change().fillna(0)], axis=1, join='inner').reset_index()
        df = df[df.time.between(start_date, end_date)]
        if trailing == '1d':
            fig.add_trace(
                go.Scatter(
                x=df.time,
                y=df.iloc[:,1].rolling(30).corr(df.iloc[:,2]),
                name=str(comb_list[count-1]),
                opacity=0.75,
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                x=df.time,
                y=df.iloc[:,1].rolling(int(trailing[:-1])).corr(df.iloc[:,2]),
                name=str(comb_list[count-1]),
                opacity=0.75,
                )
            )
    fig.update_traces(overwrite=True)
    fig.update_xaxes(fig_format.xaxis)
    fig.update_yaxes(fig_format.yaxis)
    fig.update_layout(fig_format.layout)
    return fig
