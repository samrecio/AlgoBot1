import pandas as pd
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

std = 2

window = 21

start = '2020-07-17'
end = '2021-02-11'

data = web.DataReader('BTC-USD', 'yahoo', start, end)

close = data['Adj Close']

volume = data['Volume']

volumechange = volume.diff()

volumechange = volumechange[:1]

change = close.diff()

change = change[1:]

# RSI
up, down = change.copy(), change.copy()
up[up < 0] = 0
down[down > 0] = 0

roll_up1 = up.ewm(span=window).mean()
roll_down1 = down.abs().ewm(span=window).mean()

RS1 = roll_up1 / roll_down1
RSI1 = 100.0 - (100.0 / (1.0 + RS1))

RSIframe = RSI1.to_frame()

RSIframe.columns = ['RSI']

dataRSI = pd.merge(data, RSIframe, on='Date', how='inner')

# MFI
typical_price = data['Close'] + data['High'] + data['Low'] / 3
money_flow = typical_price * data['Volume']

roll_up2 = up.rolling(window=window).mean()
roll_down2 = down.abs().rolling(window=window).mean()

protomfi = roll_up2 / roll_down2
MFI = 100.0 - (100.0 / (1.0 + protomfi))

MFIframe = MFI.to_frame()

MFIframe.columns = ['MFI']

dataMFI = pd.merge(dataRSI, MFIframe, on='Date', how='inner')

# Bollinger Bands
rolling_mean = close.rolling(window=window).mean()
rolling_std = close.rolling(window=window).std()
upper_b = rolling_mean + (rolling_std * std)
lower_b = rolling_mean - (rolling_std * std)

BLOWERframe = lower_b.to_frame()

BLOWERframe.columns = ['Blow']

datalower = pd.merge(dataMFI, BLOWERframe, on='Date', how='inner')

BUPPERframe = upper_b.to_frame()

BUPPERframe.columns = ['Bup']

BBdata = pd.merge(datalower, BUPPERframe, on='Date', how='inner')

# fig, (ax1, ax2, ax3) = plt.subplots(3)
# # ax1.get_xaxis().set_visible(False)
# # ax2.get_xaxis().set_visible(False)
# # fig.suptitle('Analysis')
# #
# # upper_b.plot(ax=ax1, color = 'green')
# # lower_b.plot(ax=ax1, color = 'red')
# # close.plot(ax=ax1, color = 'orange')
# # ax1.set_ylabel('Price ($)')
# #
# # RSI1.plot(ax=ax2)
# # ax2.set_ylim(0,100)
# # ax2.axhline(30, color='r', linestyle='--')
# # ax2.axhline(70, color='r', linestyle='--')
# # ax2.set_ylabel('RSI')
# #
# # MFI.plot(ax=ax3)
# # ax3.set_ylim(0,100)
# # ax3.axhline(10, color='orange', linestyle='--')
# # ax3.axhline(20, color='r', linestyle='--')
# # ax3.axhline(80, color='r', linestyle='--')
# # ax3.axhline(90, color='orange', linestyle='--')
# # ax3.set_ylabel('MFI')


cash = 1000.0
balance_btc = 0
order_size: float = cash


BBdata['buy_signal'] = 0

BBdata['sell_signal'] = 0
print(BBdata)
for index, row in BBdata.iterrows():
    # conditions for buy
    if row['RSI'] < 30 and row['Adj Close'] < row['Blow'] and cash >= order_size:
        #  and cash >= order_size:
        # adds a buy signal
        row['buy_signal'] = 1
        # adds order size to balance

        # calculates balance in btc
        balance_btc += order_size / row['Adj Close']
        print('buy: ' + str(order_size) + ' balance = ' + str(balance_btc * row["Adj Close"]))
        # subtracts order size amount from cash
        cash -= order_size

        # print(balance_btc)

    if row['RSI'] > 70 and row['Adj Close'] > row['Bup'] and balance_btc * row['Adj Close'] >= order_size:
        row['sell_signal'] = 1
        balance_btc -= order_size / row['Adj Close']
        cash += order_size
        print('sell: ' + str(order_size) + ' balance = ' + str(balance_btc * row["Adj Close"]))

        # print(balance_btc)

# balance_btcframe = balance_btc.to_frame()
#
# balance_btcframe.columns = ['BTC Balance']
#
# total_data = pd.merge(BBdata, balance_btcframe, on='Date', how='inner')

# print(balance_btc)
# print(balance)
# print(BBdata)

# fig, (ax1) = plt.subplots(1)
# balance.plot(ax=ax1)

# pd.set_option('display.max_rows', None)
# print(BBdata)

plt.show()
