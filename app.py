import os
import csv
import requests
import pandas as pd
from flask import Flask, request, render_template
import yfinance as yf
import talib 
from patterns import candlestick_patterns
app = Flask(__name__)
def get_fresh_data(symbol):
    df = yf.download(symbol, start='2024-01-01', end='2024-09-28')
    df.to_csv(f'datasets/daily/{symbol}.csv')
    return df
@app.route('/')
def index():
    stocks = {}
    with open('datasets/symbols.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}
    symbol = request.args.get('symbol', None)
    pattern = request.args.get('pattern', None)
    
    if symbol:
        get_fresh_data(symbol)  # Fetch and overwrite dataset

    results = None  # Initialize results
    if symbol and pattern:
        df = pd.read_csv(f'datasets/daily/{symbol}.csv')

        # Ensure the required columns exist
        if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):

            pattern_function = getattr(talib, pattern)
            try:
                # Get the pattern results and print them for debugging
                raw_results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                # Store results with corresponding dates
                results = []
                for i in range(len(raw_results)):
                    if raw_results[i] != 0:
                        results.append((df['Date'][i], raw_results[i]))
            except Exception as e:
                print(f'Error calculating pattern: {e}')

    return render_template('index.html', 
                           candlestick_patterns=candlestick_patterns, 
                           stocks=stocks, 
                           symbol=symbol, 
                           pattern=pattern, 
                           results=results)

if __name__ == '__main__':
    app.run(debug=True)
