import csv
import matplotlib.pyplot as plt
import argparse
import numpy as np
from tabulate import tabulate
import pandas as pd

# Class that calculates P&L for a financial instrument, and contains the history of the P&L (used to create different financial instrument trackers)
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
        if type not in ["stock", "future"]:
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


    @classmethod
    def create(cls):
        name = input("Name: ")
        type = input("Type: ")
        open_pos = int(input("Starting number to buy: "))
        curr_price = float(input("Current price: "))
        return cls(name, type, open_pos, curr_price)


def main():

    while True:
        try:
            stock = Instrument.create() #Instrument("AAPL", "Stock", 3000, 46.78)
            break
        except StockError:
            print("Invalid Financial Instrument!")

    trade(stock)

    # Run some buy and sell tests
    graph(stock)
    # stock.buy(45.91, 1000)
    # print(stock)
    # stock.sell(47.63, 1200)
    # print(stock)
    # stock.buy(46.15, 500)
    # print(stock)
    # stock.sell(48.55, 1100)
    # print(stock)
    # stock.sell(49.20, 700)
    # print(stock)
    # stock.sell(48.55, 1500)
    # print(stock)
    # graph(stock)
    ...





def graph(instrument):
    data = pd.DataFrame(instrument.plot_realized)
    print(data)
    plt.title('Realized profit per trade')
    plt.xlabel('Trade number')
    plt.ylabel('Realized profit')
    plt.plot(data)
    plt.savefig("trial plot.png")
    ...



def trade(instrument):
    while True:
        try:
            choice = input("What would you like to do? (buy or sell only), ctrl-d to terminate: ").lower()
            if (choice not in ["buy", "sell"]):
                continue
            elif choice == "buy":
                price = float(input("Current price: "))
                amt = int(input("Amount to buy: "))
                instrument.buy(price, amt)
            else:
                price = float(input("Current price: "))
                amt = int(input("Amount to sell: "))
                instrument.sell(price, amt)
        except EOFError:
            break


if __name__ == "__main__":
    main()