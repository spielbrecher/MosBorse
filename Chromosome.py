from MarketData import MarketData
from OneDaySystem import OneDaySystem
from Tester import Tester
from TradeSystem import TradeSystem


class Chromosome:

    def __init__(self, genes: list):
        self.system: TradeSystem = None
        self.genes = genes
        self.genes.append(5)
        self.health = 0

    def valuation(self):
        market = MarketData(date_begin='2020-01-10', date_end='2023-11-24')
        market.load_asset_data("SBER")
        self.system = OneDaySystem(data=market, money=10000, lot_size=10, period=self.genes[0])  # Задаем параметры
        tester = Tester(market, self.system, 10000)
        statistics = tester.get_statistics()
        self.health = statistics['profit']





