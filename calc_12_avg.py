import pandas as pd
import yfinance as yf

def calc_12_avg(ticker_symbol):
    # Define the date range for the past 12 months
    end_date = '2023-10-31'
    start_date = pd.Timestamp(end_date) - pd.DateOffset(months=11)

    # Fetch the historical data
    data = yf.download(ticker_symbol, start=start_date, end=end_date)

    # Calculate the monthly averages
    monthly_averages = data['Adj Close'].resample('M').mean()

    # Calculate the monthly differences (i.e., monthly increase)
    monthly_changes = monthly_averages.diff().dropna()

    # Calculate the average monthly increase
    avg_monthly_increase = monthly_changes.mean()
    avg_monthly_increase = str(round(avg_monthly_increase, 2))
    return avg_monthly_increase
