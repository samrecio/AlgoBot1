import pandas as pd
from pandas_datareader import data, wb
import datetime#Define start and end date
start = pd.to_datetime('2018-02-04')
end = pd.to_datetime('2020-05-29')#Import market data
jacobs_df = data.DataReader('J', 'yahoo', start , end)
jacobs_df#Appliying Bollinger Band strategy
jacobs_df['Middle Band'] = jacobs_df['Close'].rolling(window=20).mean()jacobs_df['Upper Band'] = jacobs_df['Middle Band'] + 1.96*jacobs_df['Close'].rolling(window=20).std()jacobs_df['Lower Band'] = jacobs_df['Middle Band'] - 1.96*jacobs_df['Close'].rolling(window=20).std()#Checking the dataframe
jacobs_df#Visualise data using PlotLy
import plotly.graph_objs as go
#declare figure
fig = go.Figure()#Set up traces
fig.add_trace(go.Scatter(x=jacobs_df.index, y= jacobs_df['Middle Band'],line=dict(color='blue', width=.7), name = 'Middle Band'))
fig.add_trace(go.Scatter(x=jacobs_df.index, y= jacobs_df['Upper Band'],line=dict(color='red', width=1.5), name = 'Upper Band (Sell)'))
fig.add_trace(go.Scatter(x=jacobs_df.index, y= jacobs_df['Lower Band'],line=dict(color='green', width=1.5), name = 'Lower Band (Buy)'))fig.add_trace(go.Candlestick(x=jacobs_df.index,
                open=jacobs_df['Open'],
                high=jacobs_df['High'],
                low=jacobs_df['Low'],
                close=jacobs_df['Close'], name = 'market data'))# Add titles
fig.update_layout(
    title='Bollinger Band Strategy',
    yaxis_title='Jacobs Engineering Stock Price (USD per Shares)')# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)#Show
fig.show()
