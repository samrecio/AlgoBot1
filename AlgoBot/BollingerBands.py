import os
import pandas as pd
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
from IPython.display import display
import certifi
import urllib3
import requests
import time
import csv
import matplotlib.pyplot as plt
import qgrid
import datetime as dt

btc = client.get_symbol_ticker(symbol="BTCUSDT")

btc['20 day MA'] = btc['Last'].rolling(20).mean()

btc['Upper'] = btc['20 day MA'] + (2*btc['Last'].rolling(20).std())

btc['Lower'] = btc['20 day MA'] - (2*btc['Last'].rolling(20).std())

btc[['Last','20 day MA','Upper','Lower']].plot(figsize=(16,6))
