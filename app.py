from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
import pandas as pd
import calc_12_avg as calc

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker_symbol = request.form['ticker']

        # Calculate the 12-month averages
        monthly_averages = calc.calc_12_avg(ticker_symbol)

        return render_template('result.html', ticker=ticker_symbol, averages=monthly_averages)
    
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
