import plotly.express as px
import pandas as pd
import time
import requests
import json


def get_token_candles(token_address):
    candles = None
    to_time = int(time.time()) * 1000
    from_time = (to_time - 21600) * 1000  # 6 hours

    url = "https://io.dexscreener.com/dex/chart/amm/uniswap/bars/ethereum/" + \
        token_address+"?from="+str(from_time)+"&to=" + \
        str(to_time)+"&res=15&cb=24"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    print(url)

    response = requests.get(url, headers=headers)
    if response is not None:
        data = response.json()
        print(data)
        if data['bars']:
            candles = data['bars']

    return candles


data = get_token_candles('0x9c0fF296B3eA128162359bab16b871E053a56519')
df = pd.read_json(json.dumps(data))

fig = px.line(df, x='timestamp', y=['closeUsd', 'openUsd'], title='ICICI BANK stock prices')
fig.update_layout(yaxis_tickformat = '.10f')
fig.show()

#fig.write_image("images/fig1.png")

