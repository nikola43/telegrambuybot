import numpy as np
from sklearn.linear_model import LinearRegression

# define the input data (price history)
data = [
    {
        "timestamp": 1677061800000,
        "open": "0.000000001804",
        "openUsd": "0.000002959",
        "high": "0.000000001884",
        "highUsd": "0.000003090",
        "low": "0.000000001852",
        "lowUsd": "0.000003037",
        "close": "0.000000001884",
        "closeUsd": "0.000003090",
        "volumeUsd": "485.29"
    },
    {
        "timestamp": 1677062700000,
        "open": "0.000000001884",
        "openUsd": "0.000003090",
        "high": "0.000000002167",
        "highUsd": "0.000003558",
        "low": "0.000000001885",
        "lowUsd": "0.000003098",
        "close": "0.000000001885",
        "closeUsd": "0.000003098",
        "volumeUsd": "3275.58"
    },
    {
        "timestamp": 1677063600000,
        "open": "0.000000001885",
        "openUsd": "0.000003098",
        "high": "0.000000001873",
        "highUsd": "0.000003078",
        "low": "0.000000001873",
        "lowUsd": "0.000003078",
        "close": "0.000000001873",
        "closeUsd": "0.000003078",
        "volumeUsd": "72.89"
    },
    {
        "timestamp": 1677064500000,
        "open": "0.000000001873",
        "openUsd": "0.000003078",
        "high": "0.000000001734",
        "highUsd": "0.000002850",
        "low": "0.000000001703",
        "lowUsd": "0.000002799",
        "close": "0.000000001703",
        "closeUsd": "0.000002799",
        "volumeUsd": "1045.10"
    }
]

# convert the data to a numpy array
X = np.array([[d['timestamp']] for d in data])
y = np.array([float(d['close']) for d in data])

# create the linear regression model and fit it to the data
model = LinearRegression()
model.fit(X, y)

# predict the price for a future timestamp (in milliseconds)
future_timestamp = 1677065400000
future_price = model.predict(np.array([[future_timestamp]]))[0]

print('Predicted price at timestamp', future_timestamp, 'is', future_price)
