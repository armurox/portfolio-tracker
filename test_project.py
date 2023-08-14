from project import Instrument, StockError, SellError, trade, tabulate, graph, valid_simulation
import pandas as pd
def test_instrument_creation():
    instrument = Instrument("AAPL", "stock", 100, 150.0)
    assert instrument.name == "AAPL"
    assert instrument.type == "stock"
    assert instrument.open_pos == 100
    assert instrument.curr_price == 150.0
    assert instrument.cum_pl == 0
    assert instrument.cum_cred_deb == -15000.0
    assert instrument.realized == 0
    assert instrument.unrealized == 0
    assert instrument._pos_hist == [{150.0: 100}]
    assert instrument._cum_hist == [{150.0: 0}]
    assert instrument._realized_hist == [{150.0: 0}]
    assert instrument.plot_realized == [0]
    assert instrument.plot_unrealized == [0]

def test_invalid_instrument_type():
    try:
        Instrument("AAPL", "invalid_type", 100, 150.0)
    except StockError:
        pass
    else:
        assert False, "Expected StockError but no exception was raised"

def test_buy_method():
    instrument = Instrument("AAPL", "stock", 100, 150.0)
    instrument.buy(155.0, 50)
    assert instrument.open_pos == 150
    assert instrument.curr_price == 155.0
    assert instrument.cum_pl == 500.0
    assert instrument.unrealized == 500.0
    assert instrument.cum_cred_deb == -22750.0

def test_sell_method():
    instrument = Instrument("AAPL", "stock", 100, 150.0)
    instrument.sell(145.0, 75)
    assert instrument.open_pos == 25
    assert instrument.curr_price == 145.0
    assert instrument.cum_pl == -500.0
    assert instrument.cum_cred_deb == -4125.0
    assert instrument.realized == -375.0
    assert instrument.unrealized == -125.0

# Test plot
def test_plot():
    instrument = Instrument("AAPL", "stock", 100, 150.0)
    data = pd.DataFrame()
    data["Realized P&L (usd)"] = pd.Series(instrument.plot_realized)
    data["Unrealized P&L (usd)"] = pd.Series(instrument.plot_unrealized)
    data["Total P&L (usd)"] = data["Realized P&L (usd)"] + data["Unrealized P&L (usd)"]
    assert graph(data) == 1

# Test table generation
def test_tabulate():
    instrument = Instrument("AAPL", "stock", 100, 150.0)
    data = pd.DataFrame()
    data["Realized P&L (usd)"] = pd.Series(instrument.plot_realized)
    data["Unrealized P&L (usd)"] = pd.Series(instrument.plot_unrealized)
    data["Total P&L (usd)"] = data["Realized P&L (usd)"] + data["Unrealized P&L (usd)"]
    assert tabulate(instrument)["Realized P&L (usd)"][0] == data["Realized P&L (usd)"][0]

def test_valid_simulation():
    assert valid_simulation("live") == True
    assert valid_simulation("test") == True
    assert valid_simulation("not live") == False