# thsi is just a demo i haven't developed fully
import pandas as pd
import numpy as np
import datetime as dt
import yfinance as data  # to read data from the net
import matplotlib.pyplot as plt
# import pandas_datareader as data # to read data from the net
start = "2000-01-01"
end = dt.datetime.today().strftime("%Y-%m-%d")
df = data.download("AAPL", start=start, end=end)
print(df.head())
print(df.tail())
df = df.reset_index() #resets the data
df = df.drop(["Date"], axis = 1)
print(df.head())
#plt.plot(df["Close"],color = "blue",label = " close")
#plt.plot(df["Open"],color = "red",label = "open")
#plt.legend()
#plt.show()
moving_average_of_100 = df.Close.rolling(100).mean()
moving_average_of_200 = df.Close.rolling(200).mean()

moving_average_of_100
moving_average_of_200

plt.figure(figsize = (12,6))
plt.plot(df["Close"],color = "green",label = " close")
plt.plot(df["Open"],color = "aqua",label = "open")
plt.plot(moving_average_of_100,color = "red",label = "moving_average_of_100")
plt.plot(moving_average_of_200,color = "blue",label = "moving_average_of_200")
plt.legend()
plt.show()
#moving_average_of_200 = df.Close.rolling(200).mean()
#moving_average_of_200 = 