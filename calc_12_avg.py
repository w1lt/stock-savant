import yfinance as yf
import pandas as pd

def calc_12_avg(ticker_symbol):
    # Define the date range for the past 12 months
    end_date = '2023-10-31'
    start_date = pd.Timestamp(end_date) - pd.DateOffset(months=11)

    # Fetch the historical data
    data = yf.download(ticker_symbol, start=start_date, end=end_date)

    # Calculate the monthly averages
    monthly_averages = data['Adj Close'].resample('M').mean()

    # Print the monthly averages
    return monthly_averages
