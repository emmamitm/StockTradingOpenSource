import os, csv
import talib
import requests
import pandas as pd
from flask import Flask, request, render_template
from patterns import candlestick_patterns

app = Flask(__name__)

API_KEY = '8C6QBAFM7FT6TXOI'

def get_fresh_data(symbol, start_date, end_date):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}&outputsize=full'
    response = requests.get(url)
    data = response.json()
    
    # Extract and format the data
    time_series = data['Time Series (Daily)']
    stock_data = []
    for date, price_data in time_series.items():
        if start_date <= date <= end_date:
            stock_data.append([date, price_data['1. open'], price_data['2. high'], price_data['3. low'], price_data['4. close'], price_data['6. volume']])

    # Convert to DataFrame
    df = pd.DataFrame(stock_data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df.to_csv(f'datasets/daily/{symbol}.csv', index=False)
    return df

@app.route('/snapshot')
def snapshot():
    symbol = request.args.get('symbol', None)
    start_date = request.args.get('start', '2023-01-01')
    end_date = request.args.get('end', '2023-09-01')

    if symbol:
        get_fresh_data(symbol, start_date, end_date)
        return {"code": "success", "message": f"Data for {symbol} has been refreshed."}
    
    return {"code": "error", "message": "No symbol provided."}

@app.route('/')
def index():
    pattern = request.args.get('pattern', False)
    stocks = {}

    with open('datasets/symbols.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}

    if pattern:
        for filename in os.listdir('datasets/daily'):
            df = pd.read_csv(f'datasets/daily/{filename}')
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.')[0]

            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = results.tail(1).values[0]

                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
            except Exception as e:
                print('Failed on filename: ', filename)

    return render_template('index.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)

if __name__ == '__main__':
    app.run(debug=True)
