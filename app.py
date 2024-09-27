import os
import csv
import requests
import pandas as pd
from flask import Flask, request, render_template
import yfinance as yf
import talib  # Make sure you have the TA-Lib package installed
from patterns import candlestick_patterns

app = Flask(__name__)

def get_fresh_data(symbol):
    df = yf.download(symbol, start='2023-01-01', end='2023-09-01')
    df.to_csv(f'datasets/daily/{symbol}.csv')
    return df

@app.route('/')
def index():
    stocks = {}
    # Load symbols from the CSV file
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
            # Print the first few rows of the data to verify it's correct
            print(df[['Date', 'Open', 'High', 'Low', 'Close']].head())

            pattern_function = getattr(talib, pattern)
            try:
                # Get the pattern results and print them for debugging
                raw_results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                print(f'Pattern results for {symbol} using {pattern}: {raw_results}')

                # Store results with corresponding dates
                results = []
                for i in range(len(raw_results)):
                    if raw_results[i] != 0:  # Only keep non-zero results
                        results.append((df['Date'][i], raw_results[i]))

                print(f"Filtered results with dates: {results}")

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
