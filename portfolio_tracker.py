import matplotlib.pyplot as plt
import numpy as np
from helpers import usd, lookup
import pandas as pd
import sys

# Class that calculates P&L for a financial instrument, and contains the history of the P&L (used to create different financial instrument trackers)

class StockError(Exception):
    "Raised when when we have an invalid instrument type"
    pass
class SellError(Exception):
    "Raised when trying to sell more than we have"
    pass

class Instrument:
    def __init__(self, name, type, open_pos: int, curr_price: float):
        self.cum_pl = 0
        self.cum_cred_deb = -1 * (open_pos * curr_price) # No getter/ setter set
        self.curr_price = curr_price # No getter / setter set
        self.unrealized = 0
        self.realized = 0
        self._pos_hist = [{self.curr_price: open_pos}]
        self._cum_hist = [{self.curr_price: self.cum_pl}]
        self._realized_hist = [{self.curr_price: self.realized}]
        self.plot_realized = [self.realized] # no getter / setter set
        self.plot_unrealized = [self.unrealized]
        self.name = name
        self.type = type.lower()
        self.open_pos = open_pos # No getter / setter set
    def __str__(self):
        return f"pl = {self.cum_pl:.2f}, cred_deb = {self.cum_cred_deb:.2f}, unrealized = {self.unrealized:.2f}, realized = {self.realized:.2f}, open_pos = {self.open_pos}, pos_hist = {self._pos_hist}, cum_hist{self._cum_hist}"
    @property
    def cum_pl(self):
        return self._cum_pl
    @cum_pl.setter
    def cum_pl(self, cum_pl):
        self._cum_pl = cum_pl
    @property
    def unrealized(self):
        return self._unrealized
    @unrealized.setter
    def unrealized(self, unrealized):
        self._unrealized = unrealized
    @property
    def realized(self):
        return self._realized
    @realized.setter
    def realized(self, realized):
        self._realized = realized
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, type):
        if type not in ["stock"]:
            raise StockError("Invalid Financial Instrument!")
        self._type = type
    # Operator overloading for adding financial instruments together
    def __add__(self, other):
        if (other.type != self.type):
            raise TypeError("Adding together incompatible instruments")
        name = "Total"
        type = self.type
        open_pos = self.open_pos + other.open_pos
        curr_price = self.curr_price + other.curr_price
        return Instrument(name, type, open_pos, curr_price)
    # Method to update the current state of the portfolio if buying more of the instrument
    def buy(self, curr_price, amt):
        self.cum_pl += (curr_price - self.curr_price) * self.open_pos
        self.unrealized = self.cum_pl - self.realized
        self.cum_cred_deb -= curr_price * amt
        self.open_pos += amt
        self.curr_price = curr_price
        self._pos_hist.append({curr_price: amt})
        self._cum_hist.append({curr_price: self.cum_pl})
        self._realized_hist.append({curr_price: self.realized})
        self.plot_realized.append(self.realized)
        self.plot_unrealized.append(self.unrealized)
    # Method to update the current state of the portfolio if selling the instrument
    def sell(self, curr_price, amt):
        if (amt > self.open_pos):
            raise SellError
        self.cum_cred_deb += curr_price * amt
        self.open_pos -= amt
        amt_left = amt
        # Keeps track if money has been used up
        count = 0
        for hist in self._pos_hist:
            for price in hist:
                pos = hist[price]
                if hist[price] == 0:
                    break
                hist[price] -= amt_left
                if hist[price] < 0:
                    amt_left = -1 * hist[price]
                    hist[price] = 0
                else:
                    amt_left = 0
                if (count == 0):
                    count += 1
                    self.realized += (curr_price - price) * (pos - hist[price])
                    self.unrealized = (curr_price - price) * (hist[price])
                else:
                    self.realized += (curr_price - price) * (pos - hist[price])
                    self.unrealized += (curr_price - price) * (hist[price])
        self.curr_price = curr_price
        self.cum_pl = self.realized + self.unrealized
        self._cum_hist.append({self.curr_price: self.cum_pl})
        self._realized_hist.append({self.curr_price: self.realized})
        self.plot_realized.append(self.realized)
        self.plot_unrealized.append(self.unrealized)


    @classmethod
    def create(cls):
        name = input("Symbol: ")
        stock = lookup(name)
        # Check validity of stock
        if stock:
            curr_price = stock["price"]
            type = input("Type: ")
            print(f"Curr_price is: {curr_price}")
            open_pos = int(input("Starting number to buy (type 0 if you would like to run your own simulation of stock prices, with the current price not being the starting): "))
            return cls(name, type, open_pos, curr_price)
        else:
            print("Invalid symbol")
            sys.exit(1)

def main():
    # Initial set up of instrument
    while True:
        try:
            stock = Instrument.create() # essentially equivalent to a object create method, with prompts
            break
        except StockError:
            print("Invalid Financial Instrument!")

    trade(stock)

    data = tabulate(stock)
    graph(data)
    ...


# Produce a table of the data
def tabulate(instrument):
    data = pd.DataFrame()
    data["Realized P&L (usd)"] = pd.Series(instrument.plot_realized)
    data["Unrealized P&L (usd)"] = pd.Series(instrument.plot_unrealized)
    data["Total P&L (usd)"] = data["Realized P&L (usd)"] + data["Unrealized P&L (usd)"]
    print(data.to_string(index=False))
    return data


def graph(data):
    plt.title("Profit or Loss per trade")
    plt.xlabel("Trade number")
    plt.ylabel("Profit or Loss")
    plt.plot(data["Realized P&L (usd)"],"og-", label = "Realized")
    plt.plot(data["Unrealized P&L (usd)"],"ob--", label = "Unrealized")
    plt.plot(data["Total P&L (usd)"],"ok-", label = "Total")
    plt.legend()
    plt.savefig("P&L Graph.png")
    return 1
    ...



def trade(instrument):
    # Define manner of simulation
    while True:
        simulation_type = input("Would you like to live trade (type live), or test your own simulation of stock prices (type test)? ").strip()
        if not valid_simulation(simulation_type):
                continue
        break
    # Run simulation
    while True:
        try:
            if (simulation_type == "live"):
                price = lookup(instrument.name)["price"]
                print(f"The current price of the instrument is: {price}")
            else:
                price = float(input("Current price (ctrl-d at any time to terminate): ").strip())
            while True:
                choice = input("What would you like to do? (buy or sell only): ").lower()
                if (choice not in ["buy", "sell"]):
                    continue
                elif choice == "buy":
                    amt = int(input("Amount to buy: "))
                    instrument.buy(price, amt)
                    break
                else:
                    amt = int(input("Amount to sell: "))
                    instrument.sell(price, amt)
                    break
        except EOFError:
            print()
            break

def valid_simulation(type):
    if type not in ["live", "test"]:
        return False
    return True


if __name__ == "__main__":
    main()