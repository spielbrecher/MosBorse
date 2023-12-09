import datetime as dt

from MarketData import MarketData
from Order import Order
from OrderType import ORDER_TYPE
from TradeSystem import TradeSystem
import pandas as pd
from moexalgo import Market, Ticker
import numpy as np
from Indicator import Indicator

class OneDaySystem(TradeSystem):

    def __init__(self, data: MarketData, money: float, lot_size: int):
        self.lot_size = lot_size
        self.money = money
        self.set_market_data(data)
        self.add_data()

    def set_market_data(self, data: MarketData):
        self.data = data
        # Акции SBER
        sber = Ticker('SBER')
        self.candles = sber.candles(date=self.data.date_begin, till_date=self.data.date_end, period='D')
        self.df = pd.DataFrame(self.candles)

    def set_ticker(self, ticker: str):
        self.ticker = Ticker(ticker)

    def set_candles(self, candles: pd.DataFrame):
        self.candles = candles
        self.df = pd.DataFrame(self.candles)

    def get_action(self, time: dt.datetime) -> Order:
        self.add_data()
        buy = False
        sell = False
        result = self.df['Buy_Signal'][len(self.df) - 1]
        if time == '10:00:00':
            # at start
            buy = True
        elif time == str(self.df['end'][len(self.df) - 1].time()):
            # at the end
            sell = True
        else:
            sell = True

        if result==1:
            # create an Order
            order = Order()
            order.id = '12345'  # Magic number
            order.datetime = dt.datetime.now()  # Current time
            order.lots = self.get_lots()
            if buy:
                order.type = ORDER_TYPE.BUY
                order.price = self.df['open'][len(self.df) - 1]
            elif sell:
                order.type = ORDER_TYPE.SELL
                order.price = self.df['close'][len(self.df) - 1]

            order.instrument = 'SBER'
            order.isExecuted = False
            return order

        return None  # Если нет сигнала, то ничего не возвращаем

    def get_lots(self):
        # Считаем цену 1 лота
        close = self.df['close'][len(self.df)-1]
        lot_price = self.lot_size * close
        lots = round(self.money / lot_price)
        return lots

    def add_profit_on_buy_indicator(self, df, crossover_col):
        # Добавляет колонку с индикатором прибыли на покупку
        df["Profit_On_Buy"] = np.where(
            df[crossover_col].shift(1) == 1,
            df["close"] - df["open"],
            0
        )
        return df

    def add_buy_signal(self, df, col):
        """
        Добавляет колонку с сигналом на покупку 1 - покупка, 0 - нет

        """
        df["Buy_Signal"] = np.where(
            df[col].shift(1) == 1,
            1,
            0
        )
        return df

    def add_data(self):
        indicator = Indicator()
        self.df = indicator.simple_moving_average(df=self.df, price_col="close", period=5)
        self.df = indicator.crossover_indicator(self.df, sma_col="SMA_5")
        self.df = self.add_profit_on_buy_indicator(self.df, "Crossover")
        self.df = self.add_buy_signal(self.df, "Crossover")