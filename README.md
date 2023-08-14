# Financial Instrument Portfolio Tracker
## Video Demo: https://youtu.be/Uahc-dyq9h0
## Description:
This Python Command Line Application provides a framework for tracking and managing the profit and loss (P&L) of financial instruments, specifically stocks. The code calculates both realized and unrealized P&L, maintains a history of P&L changes, and generates visualizations of the results. It interacts with users to simulate live trading (with actual stock prices looked up using the Yahoo Finance API) or customized simulations of stock price changes.

## Features

- **Instrument Class**: The `Instrument` class represents a financial instrument and includes properties to track its P&L, open positions, and historical data. (Design note: Interestingly, it took me some time to settle on a way of storing what the instrument was, and how it would run. I decided evetually to settle on a class implementation, as, in the future, if I choose to support other financial instruments, they can inherit many of the Instument class's features.)

- **Error Handling**: Custom exceptions (`StockError` and `SellError`) are raised for invalid financial instrument types and excessive sell amounts, respectively.

- **Operator Overloading**: The `Instrument` class supports operator overloading for adding compatible financial instruments together.

- **Buy and Sell Methods**: Methods within the `Instrument` class allow for updating the portfolio's state when buying or selling an instrument.

- **Portfolio Tracking**: The code tracks both realized and unrealized P&L over time, maintaining historical data for analysis.

- **User Interaction**: Users can select between live trading and custom simulations to test different scenarios.

- **Data Visualization**: The `graph` function generates a plot showing the realized, unrealized, and total P&L for each trade.

## Usage

1. Run the code in a Python environment that has the necessary dependencies (matplotlib, numpy, pandas) (use pip install -r requirements.txt to install them).

2. Upon running the code, the program will prompt you to enter the financial instrument's symbol, type (stock or future), and starting position (0 to run custom simulations).

3. Based on your selection, the program will either fetch the current price (live trading) or prompt you to enter the current price.

4. You can then choose to buy or sell the instrument and input the corresponding amount.

5. The program will update the portfolio's state accordingly and provide options for further actions.

6. After completing trading actions, the program will generate a table and a plot illustrating the P&L changes over trades.

## Note

This code serves as a basic framework for tracking financial instrument P&L and conducting simulations. Depending on your needs, you can further enhance the code by adding more features, refining error handling, or integrating with real-time data sources.

Please make sure to have the necessary dependencies installed before running the code (`matplotlib`, `numpy`, `pandas`).

---
Additionally, please note the the functions in the helpers.py file were not written by me. They were created for Problem Set 9 of CS50 2023, and have been imported as a helper library here, for stock price lookup from the Yahoo Finance API. helpers.py ©2023 David J. Malan/ Harvard