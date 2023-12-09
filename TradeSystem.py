import pandas as pd

from MarketData import MarketData


class TradeSystem:

    name: str
    description: str

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.money = 0

    def set_market_data(self, data: MarketData):
        pass

    def get_money(self):
        return self.money

    def set_money(self, money):
        self.money = money

    # Возвращает действие в зависимости от переданных данных
    def getAction(self):
        result = None
        return result
