import tkinter
import tkinter.messagebox
import tkinter as tk
from MarketData import MarketData
from pandastable import Table, TableModel, config
import pandas as pd

from OneDaySystem import OneDaySystem


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Strategy lab")
        self.geometry(f"{1280}x{640}")
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
#        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 0), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = tk.Frame(self, width=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, pady=(1,1), sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = tk.Label(self.sidebar_frame, text="Лаборатория\nСтратегий", font=tk.font.BOLD)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = tk.Button(self.sidebar_frame, text="Создать стратегию", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = tk.Button(self.sidebar_frame, text="Тестировать", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = tk.Button(self.sidebar_frame, text="Опубликовать", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # create tabview
        self.tabview = tk.ttk.Notebook(self)
        self.tabview.grid(row=0, column=1, padx=(5, 1), pady=(0, 1), sticky="nsew")
        self.tabMarket = tk.ttk.Frame(self.tabview)
        self.tabStrategy = tk.ttk.Frame(self.tabview)
        self.tabTester = tk.ttk.Frame(self.tabview)
        self.tabview.add(self.tabMarket, text="Рынок")
        self.tabview.add(self.tabStrategy, text="Стратегии")
        self.tabview.add(self.tabTester, text="Тестирование")

        self.tabMarket.grid_columnconfigure(0, weight=0)  # configure grid of individual tabs
        self.tabStrategy.grid_columnconfigure(0, weight=0)
        self.tabTester.grid_columnconfigure(0, weight=0)

        # Pandas Table
        self.market = MarketData()
        self.tickets = self.market.get_stocks_list()
        self.table = pt = Table(self.tabMarket, dataframe=self.tickets, showtoolbar=False, showstatusbar=False)
        self.table.grid(row=1, column=1, padx=20, pady=(10, 10))
        pt.show()

        # set some options
        options = {'colheadercolor': 'green', 'floatprecision': 5}
        config.apply_options(options, pt)
        pt.show()

        #self.combobox_1 = tk.ttk.Combobox(self.tabMarket, values=["Value 1", "Value 2", "Value Long....."])
        #self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = tk.Label(self.tabStrategy, text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        self.style = tk.ttk.Style()
        self.style.theme_use("clam")
        print(self.style.theme_names())
        print(self.style.theme_use())

    def sidebar_button_event(self):
        pass


def test_one_day():
    # One day system
    market = MarketData(date_begin='2020-01-10', date_end='2023-11-24')
    system = OneDaySystem(data=market, money=10000, lot_size=10)  # Задаем параметры системы
    action = system.get_action('10:00:00')
    if action!=None:
        print(f'{action.id} {action.instrument} {action.datetime} {action.type} {action.lots}')
    else:
        print("None")

def test():
    test_one_day()


if __name__ == "__main__":
    # app = App()
    # app.mainloop()
    test()
