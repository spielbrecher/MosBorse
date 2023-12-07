class Trader:

    def __init__(self):
        self.money = 1000000
        self.assets = list()
        self.orders = list()
        self.deals = list()

    def get_money(self):
        return self.money

    def get_assets(self):
        return self.assets

    def get_orders(self):
        return self.orders

    def get_deals(self):
        return self.deals

    def set_money(self, money):
        self.money = money

    def add_asset(self, asset):
        self.assets.append(asset)

    def add_order(self, order):
        self.orders.append(order)

    def add_deal(self, deal):
        self.deals.append(deal)


