# NEED TO REFACTOR THIS ASAP!!!!!!!!!
# key variables
# coin_cap, coin_pct, coin_price, coin_zscore, coin_index_all, coin_index, trailing


import glob
import pandas as pd

#-------------------------------------------------------------------
# Grab all indexes csvs (change this to s3 later)
#-------------------------------------------------------------------

# Check number of indexes
all_indexes = glob.glob('data/equities-index/*.csv')

index_dict = dict()
for index in all_indexes:
    index_name = index.split('/')[-1].split('.')[0]
    index_dict[index_name] = pd.read_csv(index, parse_dates=['Date'])

index_dict['spy'] = index_dict['spy'].sort_values(by='Date')
index_dict['spy'].set_index(['Date'], inplace=True)

#-------------------------------------------------------------------
# Grab all token csvs (change this to s3 later)
#-------------------------------------------------------------------

all_files = glob.glob('data/tokens/*.csv')
len(all_files)

coins_dict = dict()
for file in all_files:
    coin_name = file.split('/')[-1].split('.')[0]
    coins_dict[coin_name] = pd.read_csv(file, usecols=lambda x: x in ['time','ReferenceRateUSD', 'CapMrktCurUSD', 'CapMrktEstUSD'], parse_dates=['time'])

#-------------------------------------------------------------------
# Filter out coins without a price
#-------------------------------------------------------------------
coin_del = []
for coin in coins_dict.keys():
    if not {'ReferenceRateUSD'} <= set(coins_dict[coin].columns):
        coin_del.append(coin)

for coin in coin_del:
    coins_dict.pop(coin, None)

for coin in coins_dict.keys():
    if {'ReferenceRateUSD','CapMrktCurUSD'} <= set(coins_dict[coin].columns):
        coins_dict[coin] = coins_dict[coin].rename(columns={'ReferenceRateUSD':'price','CapMrktCurUSD':'cap'})
    elif {'ReferenceRateUSD','CapMrktEstUSD'} <= set(coins_dict[coin].columns):
        coins_dict[coin] = coins_dict[coin].rename(columns={'ReferenceRateUSD':'price','CapMrktEstUSD':'cap'})

#---------------------------------------------------------------------------
# Create synthetic index
#---------------------------------------------------------------------------


# Coin price ------------------------------------------------------------

coin_price = coins_dict['btc'].rename(columns={'price':'btc'})[['time','btc']]

coin_price.set_index('time',inplace=True)

for coin in coins_dict.keys():
    if not coin == 'btc':
        try:
            to_concat = coins_dict[coin].rename(columns={'price':coin})[['time',coin]]
            to_concat.set_index('time',inplace=True)
            coin_price = pd.concat([coin_price, to_concat],axis=1,join='outer')
        except KeyError:
            pass

coin_price = coin_price.fillna(method='ffill').fillna(0)


#Coin zscore --------------------------------------------------

    
def zscore_df(coin_list, trailing):
    coin_zscore = pd.DataFrame(((coin_price[coin_list[0]]-coin_price[coin_list[0]].rolling(trailing).mean())/coin_price[coin_list[0]].rolling(trailing).std()),columns=[coin_list[0]])
    for coin in coin_cap[coin_list].iloc[:,1:].columns:
        to_concat =  pd.DataFrame(((coin_price[coin]-coin_price[coin].rolling(trailing).mean())/coin_price[coin].rolling(trailing).std()),columns=[coin])
        coin_zscore = pd.concat([coin_zscore,to_concat],axis=1,join='outer').fillna(0)
    return coin_zscore

# coin_zscore = pd.DataFrame(((coin_price['btc']-coin_price['btc'].rolling('60d').mean())/coin_price['btc'].rolling('60d').std()),columns=['btc'])

# for coin in coin_price.columns.values:
#     if not coin == 'btc':
#         try:
#             to_concat = pd.DataFrame(((coin_price[coin]-coin_price[coin].rolling('60d').mean())/coin_price[coin].rolling('60d').std()),columns=[coin])
#             coin_zscore = pd.concat([coin_zscore,to_concat],axis=1,join='outer')
#         except KeyError:
#             pass
            
# coin_zscore = coin_zscore.fillna(0)


# Coin market cap -------------------------------------------------------

coin_cap = coins_dict['btc'].rename(columns={'cap':'btc'})[['time','btc']]

coin_cap.set_index('time',inplace=True)

for coin in coins_dict.keys():
    if not coin == 'btc':
        try:
            to_concat = coins_dict[coin].rename(columns={'cap':coin})[['time',coin]]
            to_concat.set_index('time',inplace=True)
            coin_cap = pd.concat([coin_cap, to_concat],axis=1,join='outer')
        except KeyError:
            pass

coin_cap = coin_cap.fillna(0)


# Coin market cap -------------------------------------------------------


def index_df(coin_list, trailing):
    coin_index_val = 0
    for coin in coin_cap[coin_list].columns:
        coin_pct = coin_cap[coin]/coin_cap[coin_list].sum(axis=1)
        coin_index_val += coin_price[coin] * coin_pct
    coin_index = pd.DataFrame(coin_index_val,columns=['index'])

    u = coin_index['index'].rolling(trailing).mean()
    sigma = coin_index['index'].rolling(trailing).std()
    coin_index[f'{trailing}maZ'] = (coin_index['index']-u)/sigma
    return coin_index
    
    

# def coin_price_df(coin):
#     coin_price = pd.DataFrame(coins_dict[coin].rename(columns={'price':coin})[['time',coin]])
#     coin_price.set_index('time',inplace=True)
#     return coin_price

    
# def zscore_df(coin_list, trailing):
#     coin_zscore = pd.DataFrame(((coin_price_df(coin_list[0])-coin_price_df(coin_list[0]).rolling(trailing).mean())/coin_price_df(coin_list[0]).rolling(trailing).std()),columns=[coin_list[0]])

#     for coin in coin_cap[coin_list].iloc[:,1:].columns:
#         to_concat = pd.DataFrame(((coin_price_df(coin)-coin_price_df(coin).rolling(trailing).mean())/coin_price_df(coin).rolling(trailing).std()),columns=[coin])
#         coin_zscore = pd.concat([coin_zscore,to_concat],axis=1,join='outer')
#     return coin_zscore


    




# # Coin cap by percentage of total-----------------------------------------

# coin_pct = pd.DataFrame(coin_cap['btc']/coin_cap['total'], columns=['btc'])

# for coin in coin_cap.columns.values[:-1]:
# 	if not coin == 'btc':
# 		try: 
# 			to_concat = pd.DataFrame(coin_cap[coin]/coin_cap['total'], columns=[coin])
# 			coin_pct = pd.concat([coin_pct,to_concat],axis=1,join='outer')
# 		except KeyError:
# 			pass

# coin_pct = coin_pct.fillna(0)




# # Coin index  ------------------------------------------------------------


# # coin_index = pd.DataFrame((coin_pct*coin_price).sum(axis=1)[:-1],columns=['index'])


# coin_index = pd.DataFrame((coin_pct*coin_price).sum(axis=1)[:-1],columns=['index'])

# trailing = ['30d', '60d', '90d', '180d', '360d']

# for days in trailing:
#     coin_index[f'{days}ma'] = coin_index['index'].rolling(days).mean()
#     coin_index[f'{days}maVol'] = coin_index['index'].rolling(days).std()
#     coin_index[f'{days}maZ'] = (coin_index['index']-coin_index[f'{days}ma'])/coin_index[f'{days}maVol']





