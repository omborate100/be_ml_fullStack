# import yfinance as yahooFinance
import numpy as np
import pandas as pd
from flask import Flask,jsonify,request
import pickle
from yahoo_fin.stock_info import get_data
import yfinance as yf
from flask_cors import CORS



app = Flask(__name__)
CORS(app,origins='http://localhost:3000')
model = pickle.load(open("model.pkl","rb"))

@app.route('/')
def hello_world():
    
    return 'Hello, World!'

@app.route('/stock', methods=['POST'])
def stock():
    val = request.get_json()
    # val = val.get_json('stocks')
    d = val['stocks']
    print(d)
    #--------------------------------------------------------prediction start--------------------------------------------------------
    df= get_data(d, start_date="09/08/2023", end_date="09/09/2023", index_as_date = False, interval="1d")
   
    open1 = df['open']
    high = df['high']
    low = df['low']
    volume = df['volume']
    print(open1)
    print(high)
    print(df)
    features = [open1, high, low, volume]
    float_features = [float(x) for x in features]
    features = [np.array(float_features)]
    prediction = model.predict(features)
    val = prediction[0]   
    print(val) 
    val = round(val, 2)
    #----------------------------------------------------------------prediction end----------------------------------------------------------------
    return jsonify(val)
    
@app.route('/close' , methods=['POST'])
def close():
    val1 = request.get_json()
    d1 = val1['stocks']
    
    df_visual= get_data(d1, start_date="08/25/2023", end_date="09/08/2023", index_as_date = False, interval="1d")
    # close_prices = []
    print(df_visual)
    # for index, row in df_visual.iterrows():
    #     # Append the close price from the "Close" column to the list
    #     close_prices.append(row["close"])
    # print(close_prices)
    # return close_prices
    formatted_data = []
    for index, row in df_visual.iterrows():
        # Extract the date and close price
        date = row["date"]
        close = row["close"]
        close = round(close, 2)
        volume = row["volume"]
        # Convert the date to a string in the "yyyy-MM-dd" format
        formatted_date = date.strftime("%Y-%m-%d")

        # Create a dictionary representing each data point
        data_point = {"date": formatted_date, "close": close, "volume": volume}

        # Append the data point to the list
        formatted_data.append(data_point)
    print(formatted_data)
    return formatted_data

@app.route('/predictions', methods=['POST'])
def predictions():
    val3 = request.get_json()
    d3 = val3['stocks']
    df= get_data(d3, start_date="09/08/2023", end_date="09/09/2023", index_as_date = False, interval="1d")
    open1 = df['open']
    high = df['high']
    low = df['low']
    volume = df['volume']
    print(open1)
    print(high)
    print(df)
    
    features = [open1, high, low, volume]
    float_features = [float(x) for x in features]
    features = [np.array(float_features)]
    prediction = model.predict(features)
    val = prediction[0]    
    return jsonify(val)

@app.route('/fundamental', methods=['POST'])
def fundamental():
    val7 = request.get_json()
    d7 = val7['stocks']
    # quote_table = si.get_quote_table(d7, dict_result=False)
    print("fundamental")
    print(d7)
    return d7

if __name__ == '__main__':
    app.run(debug=True)