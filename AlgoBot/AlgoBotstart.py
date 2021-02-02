import os
import pandas as pd
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
from IPython.display import display
import certifi
import urllib3
import requests
import csv
import matplotlib.pyplot as plt
import qgrid
import datetime as dt
import btalib

data = pd.read_csv("BTCUSDT-1m-2018-03.csv")
print(data.head())

btc_df['20MA'] = btalib.sma(btc_df.close, period=20).df
print(btc_df.tail())

rsi = btalib.rsi(btc_df, period=11)
print(rsi.tail())

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')


client = Client(api_key,api_secret)
btc_price = {'error':False}
client.API_URL = 'https://testnet.binance.vision/api'

test = requests.get('https://testnet.binance.vision/api')
cafile = certifi.where()



def btc_trade_history(msg):
    if msg['e'] != 'error':
        print(msg['c'])
        btc_price['last'] = msg['c']
        btc_price['bid'] = msg['b']
        btc_price['last'] = msg['a']
    else:
        btc_price['error'] = True



bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', btc_trade_history)
#bsm.start()

#print(btc_price)





#btc_price['MA'] = btc_price['last'].rolling().mean()

#btc_price['Upper'] = btc_price['MA'] + (2*btc_price['last'].rolling().std())

#btc_price['Lower'] = btc_price['MA'] - (2*btc_price['last'].rolling().std())

#btc_price[['last','MA','Upper','Lower']].plot(figsize=(16,6))







#print(client.get_account())





