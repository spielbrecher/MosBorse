import pandas as pd

from MarketData import MarketData


class TradeSystem:

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def set_market_data(self, data: MarketData):
        pass

    # Возвращает действие в зависимости от переданных данных
    def getAction(self):
        result = None
        return result
