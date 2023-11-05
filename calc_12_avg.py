import pandas as pd
import yfinance as yf
import statistics

def calc_12_avg(ticker_symbol):
    # Define the date range for the past 12 months
    end_date = '2023-10-31'
    start_date = pd.Timestamp(end_date) - pd.DateOffset(months=11)

    # Fetch the historical data
    data = yf.download(ticker_symbol, start=start_date, end=end_date)

    # Calculate the monthly averages
    monthly_averages = data['Adj Close'].resample('M').mean()

    # Calculate the monthly differences (i.e., monthly increase)
    last_11_month_avg_prices = monthly_averages.tail(11).tolist()
    monthly_changes = monthly_averages.diff().dropna()

    # Calculate the average monthly increase
    avg_monthly_change = monthly_changes.mean()
    avg_monthly_change = int(round(avg_monthly_change, 2))

    monthly_stdev = statistics.stdev(last_11_month_avg_prices)  # Standard deviation of sentiments

    #find b value of y=mx+b for month 11
    average_slope = avg_monthly_change/11
    b = monthly_averages[10] - (average_slope*11) # y(of 11th month) - average_slope*x(of 11th month)

    return [avg_monthly_change, monthly_stdev, average_slope, b]