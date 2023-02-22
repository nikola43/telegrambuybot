import plotly.express as px
import pandas as pd
import time
import requests
import json
import numpy as np
from sklearn.linear_model import LinearRegression


def get_token_candles(token_address):
    candles = None
    to_time = int(time.time()) * 1000
    from_time = (to_time - 21600) * 1000  # 6 hours

    url = "https://io.dexscreener.com/dex/chart/amm/uniswap/bars/ethereum/" + \
        token_address+"?from="+str(from_time)+"&to=" + \
        str(to_time)+"&res=5&cb=24"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    print(url)

    response = requests.get(url, headers=headers)
    if response is not None:
        data = response.json()
        # print(data)
        if data['bars']:
            candles = data['bars']

    return candles


data = get_token_candles('0xcbd4fae71751b48e0c9dd5b275a8cba199cf347a')



# convert the data to a numpy array
X = np.array([[d['timestamp']] for d in data])
y = np.array([float(d['closeUsd']) for d in data])

# create the linear regression model and fit it to the data
model = LinearRegression()
model.fit(X, y)

# loop through the data and predict the price for each timestamp
for d in data:
    d['predicted_price'] = model.predict(np.array([[d['timestamp']]]))[0]
    print("{:,.18f}".format(float(d['predicted_price'])))
    

# predict the price for a future timestamp (in milliseconds)
#future_timestamp = data[len(data) - 1]['timestamp'] + 3600 * 1000
#print(future_timestamp)
#future_price = model.predict(np.array([[future_timestamp]]))[0]

# calculate the change percentage
#change = (future_price - float(data[len(data) - 1]['close'])) / float(data[len(data) - 1]['close']) * 100

# conver future timestamp to human readable format
#future_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(future_timestamp / 1000))

#print('Predicted price at timestamp', future_timestamp, 'is',str("{:,.18f}".format(float(future_price))) + " " + str(change))


df = pd.read_json(json.dumps(data))

fig = px.line(df, x='timestamp', y=['closeUsd', 'predicted_price'], title='Predicted price')
fig.update_layout(yaxis_tickformat = '.10f')
fig.show()

# fig.write_image("images/fig1.png")
