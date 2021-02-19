import pandas as pd
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import numpy as np

std = 2

window_length = 14

start = '2014-07-17'
end = '2021-02-11'

data = web.DataReader('BTC-USD', 'yahoo', start, end)

close = data['Adj Close']

volume = data['Volume']

volumechange = volume.diff()

volumechange = volumechange[:1]

change = close.diff()

change = change[1:] 

#RSI
up, down = change.copy(), change.copy()
up[up < 0] = 0
down[down > 0] = 0


roll_up1 = up.ewm(span=window_length).mean()
roll_down1 = down.abs().ewm(span=window_length).mean()


RS1 = roll_up1 / roll_down1
RSI1 = 100.0 - (100.0 / (1.0 + RS1))

RSIframe=RSI1.to_frame()

RSIframe.columns = ['RSI']

dataRSI = pd.merge(data,RSIframe,on = 'Date', how='inner')



#MFI
typical_price = data['Close'] + data['High'] + data['Low'] / 3
money_flow = typical_price * data['Volume']

roll_up2 = up.rolling(window=window_length).mean()
roll_down2 = down.abs().rolling(window=window_length).mean()


protomfi = roll_up2 / roll_down2
MFI = 100.0 - (100.0 / (1.0 + protomfi))

MFIframe=MFI.to_frame()

MFIframe.columns = ['MFI']

dataMFI = pd.merge(dataRSI,RSIframe,on = 'Date', how='inner')

print(dataMFI)


#Bollinger Bands
rolling_mean = close.rolling(window=window_length).mean()
rolling_std  = close.rolling(window=window_length).std()
upper_b = rolling_mean + (rolling_std*std)
lower_b = rolling_mean - (rolling_std*std)

BLOWERframe=lower_b.to_frame()

BLOWERframe.columns = ['Blow']

datalower = pd.merge(dataMFI,BLOWERframe,on = 'Date', how='inner')



BUPPERframe=upper_b.to_frame()

BUPPERframe.columns = ['Bup']

totaldata = pd.merge(datalower,BUPPERframe,on = 'Date', how='inner')

print(totaldata)




# fig, (ax1, ax2, ax3) = plt.subplots(3)
# ax1.get_xaxis().set_visible(False)
# ax2.get_xaxis().set_visible(False)
# fig.suptitle('Analysis')

# upper_b.plot(ax=ax1, color = 'green')
# lower_b.plot(ax=ax1, color = 'red')
# close.plot(ax=ax1, color = 'orange')
# ax1.set_ylabel('Price ($)')

# RSI1.plot(ax=ax2)
# ax2.set_ylim(0,100)
# ax2.axhline(30, color='r', linestyle='--')
# ax2.axhline(70, color='r', linestyle='--')
# ax2.set_ylabel('RSI')

# MFI.plot(ax=ax3)
# ax3.set_ylim(0,100)
# ax3.axhline(10, color='orange', linestyle='--')
# ax3.axhline(20, color='r', linestyle='--')
# ax3.axhline(80, color='r', linestyle='--')
# ax3.axhline(90, color='orange', linestyle='--')
# ax3.set_ylabel('MFI')

balance = 1000.0



#for index, row in df.iterrows():
    #print(row['c1'], row['c2'])




plt.show()
