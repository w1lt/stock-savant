from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.io import output_notebook
from datetime import datetime

# Data
dates = [
    "2022-11-30",
    "2022-12-31",
    "2023-01-31",
    "2023-02-28",
    "2023-03-31",
    "2023-04-30",
    "2023-05-31",
    "2023-06-30",
    "2023-07-31",
    "2023-08-31",
    "2023-09-30",
    "2023-10-31",
]
values = [
    147.40110778808594,
    137.29092298235213,
    135.20216789245606,
    150.4717704371402,
    154.54204260784647,
    164.59555294639185,
    172.2935333251953,
    184.0348161969866,
    192.1520217895508,
    180.9973615563434,
    177.00250091552735,
    174.85428728376115,
]

# Convert date strings to datetime objects
dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

# Create a ColumnDataSource
source = ColumnDataSource(data={"dates": dates, "values": values})

# Create the plot
output_file("stock_price_ticker.html", title="Stock Price Ticker")

p = figure(
    x_axis_label="Date",
    y_axis_label="Price",
    x_axis_type="datetime",
    title="Stock Price Ticker",
    width=800,
    height=300,
    toolbar_location=None,
    background_fill_color="#f0f0f0",
    border_fill_color="#ffffff",
)

p.grid.grid_line_alpha = 0.6
p.grid.grid_line_dash = "dotted"

p.line("dates", "values", source=source, line_width=2, line_color="#007bff")

# Remove the x-axis major label ticks
p.xaxis.major_label_overrides = {}

# Show the plot
show(p)
