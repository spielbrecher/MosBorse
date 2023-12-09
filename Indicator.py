import pandas as pd
import numpy as np


class Indicator:

    def __init__(self):
        pass

    # SMA
    def simple_moving_average(self, df: pd.DataFrame, price_col: str, period: int):
        close = df[price_col]
        close_sma = close.rolling(window=period).mean()
        df["SMA_" + str(period)] = close_sma
        return df

    #  Crossover of SMA - индикатор показывает, что текущее значение SMA больше предыдущего
    def crossover_indicator(self, df: pd.DataFrame, sma_col: str):
        # df - DataFrame, sma_col - колонка с рассчитанным значением SMA
        df["Crossover"] = np.where(
            df[sma_col].diff(1) > 0,
            1,
            0
        )
        return df
