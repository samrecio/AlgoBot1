import os
import pandas as pd
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
from IPython.display import display
import certifi
import urllib3
import requests

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')


client = Client(api_key,api_secret)
btc_price = {'error':False}
client.API_URL = 'https://testnet.binance.vision/api'

test = requests.get('https://testnet.binance.vision/api')
cafile = certifi.where()
#with open('binance-vision.pem', 'rb')
#as infile:
    #customca = infile.read()
#with open(cafile, 'ab') as outfile:
    #outfile.write(customca)


print(client.get_account())

def btc_trade_history(msg):
    ''' define how to process incoming WebSocket messages '''
    if msg['e'] != 'error':
        print(msg['c'])
        btc_price['last'] = msg['c']
        btc_price['bid'] = msg['b']
        btc_price['last'] = msg['a']
    else:
        btc_price['error'] = True

