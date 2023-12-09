from moexalgo import Market, Ticker
import pandas as pd


class MarketData:

    def __init__(self, date_begin, date_end):
        self.stocks = Market('stocks')
        self.date_begin = date_begin
        self.date_end = date_end


    def load_asset_data(self, asset_name):
        # Акции SBER
        self.asset = Ticker(asset_name)
        # Все акции
        self.candles = self.asset.candles(date=self.date_begin, till_date=self.date_end, period='D')

    def get_candles(self):
        return self.candles

    def get_stocks_list(self):
        df = pd.DataFrame(self.stocks.tradestats(date=self.date_end))
        return df[['secid']].unique()

    def get_tradestats(self):
        return pd.DataFrame(self.stocks.tradestats(date=self.date_end))
