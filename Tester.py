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
Эти параметры могут дать более полную картину эффективности торговой системы, чем только прибыльность. Например, если торговая система делает много сделок, но при этом процент прибыльных сделок низкий, то такая система может быть неэффективной.

Также можно использовать более сложные параметры, такие как:

Средний коэффициент прибыльности: среднее соотношение прибыли к убытку для всех сделок.
Средняя доходность: средняя прибыль от одной сделки за единицу времени.
Средняя волатильность: средняя степень колебания цены инструмента за единицу времени.
Средний риск: средняя величина убытка от одной сделки.
'''


class Tester:
    def __init__(self, data: MarketData, trade_system: TradeSystem):
        self.data = data
        self.trade_system = trade_system
        self.orders = []

    def test(self, start):
        self.orders = []
        candles = pd.DataFrame(self.data.get_candles())
        orders_count = 0
        for i in range(start, len(candles)):
            # Получаем данные за текущую дату
            current_data = candles[:i]
            # Получаем заявку от торговой системы
            self.trade_system.set_candles(current_data)
            order: Order = self.trade_system.get_action('10:00:00')
            if order:
                self.orders.append(order)
                orders_count += 1
            order: Order = self.trade_system.get_action('23:59:59')
            if order:
                self.orders.append(order)
                orders_count += 1
        print(f"Orders count {orders_count}")

    def get_statistics(self):
        profit = 0  # Прибыль
        trades_count = len(self.orders)  # Количество сделок
        profitable_trade_count = 0  # Количество прибыльных сделок
        losing_trade_count = 0  # Количество убыточных сделок

        buy_price = 0
        sell_price = 0

        for order in self.orders:
            if order.type == ORDER_TYPE.BUY:
                buy_price = order.price * order.lots
            elif order.type == ORDER_TYPE.SELL:
                sell_price = order.price * order.lots
                profit += sell_price - buy_price
                buy_price = 0
                #  Подсчет количества прибыльных и убыточных сделок
                if sell_price > buy_price:
                    profitable_trade_count += 1
                else:
                    losing_trade_count += 1

        return {
            "profit": profit,
            "trades": trades_count
        }
