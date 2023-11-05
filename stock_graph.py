from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from calc_12_avg import calc_12_avg
from datetime import datetime

def generate_graph(ticker):
    averages = calc_12_avg(ticker)
    
    dates = []
    values = []

    for month, average in averages.items():
        # Convert Pandas Timestamp to string
        month_str = month.strftime("%Y-%m-%d")
        dates.append(datetime.strptime(month_str, "%Y-%m-%d"))
        values.append(average)

    # Create a ColumnDataSource
    source = ColumnDataSource(data={"dates": dates, "values": values})

    # Create the plot
    p = figure(
        x_axis_label="Date",
        y_axis_label="Price",
        x_axis_type="datetime",
        title=f"Stock Price Ticker for {ticker}",
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

    return p  # Return the Bokeh plot object
