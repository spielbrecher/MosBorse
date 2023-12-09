import pandas as pd
from MarketData import MarketData
from TradeSystem import TradeSystem
from Order import Order
from OrderType import ORDER_TYPE

'''
Количество сделок: количество сделок, открытых торговой системой за период тестирования.
Процент прибыльных сделок: процент сделок, которые закрылись с прибылью.
Процент убыточных сделок: процент сделок, которые закрылись с убытком.
Средний размер прибыли: средний размер прибыли от одной сделки.
Средний размер убытка: средний размер убытка от одной сделки.
Средний срок сделки: среднее время нахождения сделки в открытом состоянии.
Максимальная прибыль: максимальная прибыль от одной сделки.
Максимальный убыток: максимальный убыток от одной сделки.

Также можно использовать более сложные параметры, такие как:
Средний коэффициент прибыльности: среднее соотношение прибыли к убытку для всех сделок.
Средняя доходность: средняя прибыль от одной сделки за единицу времени.
Средняя волатильность: средняя степень колебания цены инструмента за единицу времени.
Средний риск: средняя величина убытка от одной сделки.
'''


class Tester:
    def __init__(self, data: MarketData, trade_system: TradeSystem, money: float):
        self.data = data
        self.trade_system = trade_system
        self.orders = []

    def test(self, start):
        self.orders = []
        candles = pd.DataFrame(self.data.get_candles())
        orders_count = 0
        buy_price = 0
        sell_price = 0
        money_list = []
        money_list.append(self.trade_system.get_money())

        for i in range(start, len(candles)):
            # Получаем данные за текущую дату
            current_data = candles[:i]
            money = self.trade_system.get_money()

            # Получаем заявку от торговой системы
            self.trade_system.set_candles(current_data)
            order: Order = self.trade_system.get_action('10:00:00')
            if order:
                self.orders.append(order)
                buy_price = order.price * order.lots
                orders_count += 1
            order: Order = self.trade_system.get_action('23:59:59')
            if order:
                self.orders.append(order)
                sell_price = order.price * order.lots
                trade_profit = sell_price - buy_price
                money += trade_profit
                money_list.append(money)
                self.trade_system.set_money(money)
                orders_count += 1
        print(f"Orders count {orders_count}")
        return money_list

    def get_statistics(self):
        profit = 0  # Прибыль
        orders_count = len(self.orders)  # Количество сделок
        profitable_trades_count = 0  # Количество прибыльных сделок
        losing_trades_count = 0  # Количество убыточных сделок
        max_profit = 0  # Максимальная прибыль от сделки
        max_loss = 0  # Максимальный убыток от сделки
        mean_profit = 0  # Средняя прибыль от сделки
        mean_loss = 0  # Средний убыток от сделки
        profits = []
        losses = []

        buy_price = 0
        sell_price = 0


        for order in self.orders:
            if order.type == ORDER_TYPE.BUY:
                buy_price = order.price * order.lots
            elif order.type == ORDER_TYPE.SELL:
                sell_price = order.price * order.lots
                profit += sell_price - buy_price
                #  Подсчет количества прибыльных и убыточных сделок, максимальной прибыли и убытка
                trade_profit = sell_price - buy_price

                if trade_profit > 0:
                    profits.append(trade_profit)
                    profitable_trades_count += 1
                    if max_profit < trade_profit:
                        max_profit = trade_profit
                else:
                    losses.append(trade_profit)
                    losing_trades_count += 1
                    if max_loss > trade_profit:
                        max_loss = trade_profit

                buy_price = 0
                sell_price = 0

        trades_count = round(orders_count / 2)
        average_profit = 0
        if len(profits) > 0:
            average_profit = sum(profits)/len(profits)
        average_loss = 0
        if len(losses) > 0:
            average_loss = sum(losses) / len(losses)

        profitability = sum(profits) / -sum(losses)

        return {
            "profit": profit,
            "trades": trades_count,
            "profitable trades": profitable_trades_count,
            "profitable trades %": profitable_trades_count / trades_count * 100,
            "losing trades": losing_trades_count,
            "losing trades %": losing_trades_count / trades_count * 100,
            "Max profit on trade": max_profit,
            "Max loss on trade": max_loss,
            "Average profit on trade": average_profit,
            "Average loss on trade": average_loss,
            "Profitability": profitability
        }
