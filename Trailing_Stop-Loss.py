!pip install yfinance

import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime

# Download Bitcoin data
btc = yf.download('BTC-USD', start='2020-01-01', end='2023-01-01')

# Define buy price and stop-loss level
buy_price = btc['Close'][0]
stop_loss = 0.95
stop_loss_level = buy_price * stop_loss

# Create lists to store the stop-loss and sell prices
stop_loss_list = [stop_loss_level]

# Initialize variables
stop_loss_count = 0
total_losses = 0
num_bitcoins = 1
date_list = []

# Loop through Bitcoin data
for i in range(1, len(btc)):
    # Check if stop-loss should be adjusted
    if btc['Close'][i] > stop_loss_level:
        stop_loss_level = max(stop_loss_level, btc['Close'][i] * stop_loss)

        # Add the stop-loss value to the list
        stop_loss_list.append(stop_loss_level)

    # Check if stop-loss has been triggered
    if btc['Close'][i] <= stop_loss_level:
        stop_loss_count += 1

        # Calculate losses incurred
        losses = buy_price - stop_loss_level

        # Update number of Bitcoins owned
        num_bitcoins = num_bitcoins * (1 - losses / buy_price)

        # Reset buy price and stop-loss level
        buy_price = btc['Close'][i]
        stop_loss_level = buy_price * stop_loss

        # Update the date list when stop-loss triggered
        date_list.append(btc.index[i])

        # Add the new stop-loss value to the list
        stop_loss_list.append(stop_loss_level)


# Print stop-loss and losses statistics
print('Number of stop-loss triggered:', stop_loss_count)
print('Percentage of stop-loss triggered:', stop_loss_count / len(btc) * 100, '%')
print('Number of Bitcoins owned at the end of the period:', num_bitcoins)

# Convert the dates to the desired format
formatted_dates = [datetime.strftime(date, "%y-%m") for date in btc.index]

# Plot the dates as vertical lines
for date in date_list:
    plt.axvline(x=date, color='red', linestyle=':', linewidth=0.25)

# Plot Bitcoin price and stop-loss
dates = btc.index[1:]
prices = btc['Close'][1:]
plt.plot(dates, prices, color='blue', linewidth=0.5, label="Bitcoin Prices")
plt.plot(dates, stop_loss_list[:-1], color='red', linewidth=0.5, label="Trailing Stop-Loss")
plt.legend(loc="upper left")
plt.title('Bitcoin Price with Trailing Stop-Loss')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.legend()
plt.show()

# Create interactive chart with Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=dates, y=prices, name='Bitcoin Price', line=dict(width=0.75)))
fig.add_trace(go.Scatter(x=dates, y=stop_loss_list[:-1], name='Stop-Loss Level', mode='lines', line=dict(color='red', width=0.5)))

# Add vertical lines for stop-loss hits
for date in date_list:
    fig.add_shape(
        type="line",
        x0=date,
        y0=btc["Close"].min(),
        x1=date,
        y1=btc["Close"].max(),
        line=dict(color="red", width=0.25, dash="dot"),
    )

fig.update_layout(title='Bitcoin Price and Trailing Stop-Loss', xaxis_title='Date', yaxis_title='Price (USD)')
fig.show()
