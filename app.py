from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])


def get_stock_price_movement(company_ticker):
    try:
        data = yf.download(company_ticker, period="1d", interval="1m")
        percentage_change = ((data['Close'][-1] - data['Open'][0]) / data['Open'][0]) * 100
    except:
        percentage_change = 0

    return percentage_change

def get_pe_ratio(company_ticker):
    try:
        ticker_data = yf.Ticker(company_ticker)
        pe_ratio = ticker_data.info["trailingPE"]
    except:
        pe_ratio = None
    
    return pe_ratio

def predict_company_performance(company_ticker):
    stock_movement = get_stock_price_movement(company_ticker)
    pe_ratio = get_pe_ratio(company_ticker)

    if pe_ratio is None:
        return f"Couldn't fetch data for {company_ticker}. Please try again."

    score = 0
    if pe_ratio < 15:
        score += 1
    elif pe_ratio < 25:
        score += 0.5

    score += 0.3 * (stock_movement / 10)

    if score > 1.2:
        performance = "EXCELLENT"
    elif score > 0.8:
        performance = "GOOD"
    elif score > 0.4:
        performance = "AVERAGE"
    else:
        performance = "POOR"

    return f"Predicted performance for {company_ticker}: {performance}"

def index():
    prediction = None

    if request.method == 'POST':
        # For demonstration, we're treating the input as a company ticker
        prediction = predict_company_performance(request.form['company_ticker'].upper())

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)