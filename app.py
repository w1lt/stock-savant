from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
import pandas as pd
import calc_12_avg as calc
import stock_graph
from bokeh.embed import components

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker_symbol = request.form['ticker']

        # Calculate the 12-month averages
        try:
            monthly_averages = calc.calc_12_avg(ticker_symbol)
        except:
            return render_template('index.html', error=True)

        stock_plot = stock_graph.generate_graph(ticker_symbol)
        script, div = components(stock_plot)

        return render_template('result.html', ticker=ticker_symbol, averages=monthly_averages, script=script, div=div)
    
    return render_template('index.html')

@app.route('/graph/<ticker>', methods=['GET'])
def show_graph(ticker):
    stock_plot = stock_graph.generate_graph(ticker)
    script, div = components(stock_plot)
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
    app.run(debug=True)
