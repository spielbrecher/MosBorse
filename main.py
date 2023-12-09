import tkinter
import tkinter.messagebox
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from MarketData import MarketData
from pandastable import Table, TableModel, config
import pandas as pd

from OneDaySystem import OneDaySystem
from Tester import Tester
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Strategy lab")
        self.geometry(f"{1280}x{900}")
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
        self.sidebar_button_2 = tk.Button(self.sidebar_frame, text="Тестировать", command=self.sidebar_button_test_event)
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

        self.tabMarket.grid_columnconfigure(3, weight=1)  # configure grid of individual tabs
        self.tabMarket.grid_rowconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabStrategy.grid_columnconfigure(0, weight=1)
        self.tabTester.grid_columnconfigure(0, weight=1)

        # List with Tickers
        self.market = MarketData(date_begin='2020-01-10', date_end='2023-11-24')
        self.tickets = self.market.get_stocks_list()
        self.list_tickets = tk.Listbox(self.tabMarket)
        self.scrollbar = tk.Scrollbar(self.tabMarket, orient="vertical")
        # Размещаем список и полосу прокрутки на форме с помощью grid
        self.scrollbar.config(command=self.list_tickets.yview)
        self.list_tickets.config(yscrollcommand=self.scrollbar.set)
        self.list_tickets.bind("<<ListboxSelect>>", self.on_select)
        for value in self.tickets:
            self.list_tickets.insert(tk.END, value)
        self.list_tickets.grid(row=0, column=0, padx=1, pady=(1, 1), sticky="ns")
        self.scrollbar.grid(row=0, column=1, padx=1, pady=(1, 1), sticky="ns")
        self.market.load_asset_data('SBER')
        self.plot_price()

        self.label_results = tk.Label(self.tabTester, text="Результаты тестирования")
        self.label_results.grid(row=0, column=0, padx=10, pady=10)
        self.label_results_content = tk.Label(self.tabTester, text="")
        self.label_results_content.grid(row=1, column=2, padx=10, pady=10)

        self.style = tk.ttk.Style()
        self.style.theme_use("clam")
        print(self.style.theme_names())
        print(self.style.theme_use())

    def sidebar_button_test_event(self):
        result, money_list = test()
        # Изменение денег
        figure, ax = plt.subplots()
        ax.set_title('Деньги')
        ax.plot(money_list)
        canvas = FigureCanvasTkAgg(figure, master=self.tabTester)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, padx=1, pady=(1, 1), sticky="nsew")
        # Прибыльные - убыточные
        fig, ax = plt.subplots()
        name = ["Прибыльные, %", "Убыточные, %"]
        value = [result["profitable trades %"], result["losing trades %"]]
        bar_labels = ['green', 'red']
        bar_colors = ['tab:green', 'tab:red']
        ax.bar(name, value, label=bar_labels, color=bar_colors)
        ax.set_ylabel('%')
        ax.set_title('Прибыльные/Убыточные сделки %')
        canvas = FigureCanvasTkAgg(fig, master=self.tabTester)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, columnspan=1, padx=1, pady=(1, 1), sticky="nsew")
        # Max Прибыль - убыток
        fig, ax = plt.subplots()
        name = ["Прибыль", "Убыток"]
        value = [result["Max profit on trade"], abs(result["Max loss on trade"])]
        bar_labels = ['green', 'red']
        bar_colors = ['tab:green', 'tab:red']
        ax.bar(name, value, label=bar_labels, color=bar_colors)
        ax.set_ylabel('Рубли')
        ax.set_title('Max Прибыль/Убыток')
        canvas = FigureCanvasTkAgg(fig, master=self.tabTester)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=1, padx=1, pady=(1, 1), sticky="nsew")
        # Avg Прибыль - убыток
        fig, ax = plt.subplots()
        name = ["Прибыль", "Убыток"]
        value = [result["Average profit on trade"], abs(result["Average loss on trade"])]
        bar_labels = ['green', 'red']
        bar_colors = ['tab:green', 'tab:red']
        ax.bar(name, value, label=bar_labels, color=bar_colors)
        ax.set_ylabel('Рубли')
        ax.set_title('Средняя Прибыль/Убыток')
        canvas = FigureCanvasTkAgg(fig, master=self.tabTester)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1, columnspan=1, padx=1, pady=(1, 1), sticky="nsew")

        text = ""
        for key, value in result.items():
            val = format(value, '.2f')
            text += f"{key} = {val}\n"

        self.label_results_content.config(text=text)

    def sidebar_button_event(self):
        pass

    def plot_price(self):
        candles = pd.DataFrame(self.market.get_candles())
        candles_visible = candles.loc[len(candles)-20:len(candles)-1]
        candles_visible.begin = candles_visible.begin.astype(str)
        # create figure
        figure = plt.figure()

        # define width of candlestick elements
        width = .4
        width2 = .05

        # define up and down prices
        up = candles_visible[candles_visible.close >= candles_visible.open]
        down = candles_visible[candles_visible.close < candles_visible.open]

        # define colors to use
        col1 = 'green'
        col2 = 'red'

        # plot up prices
        plt.bar(up.index, up.close - up.open, width, bottom=up.open, color=col1)
        plt.bar(up.index, up.high - up.close, width2, bottom=up.close, color=col1)
        plt.bar(up.index, up.low - up.open, width2, bottom=up.open, color=col1)

        # plot down prices
        plt.bar(down.index, down.close - down.open, width, bottom=down.open, color=col2)
        plt.bar(down.index, down.high - down.open, width2, bottom=down.open, color=col2)
        plt.bar(down.index, down.low - down.close, width2, bottom=down.close, color=col2)

        # rotate x-axis tick labels
        plt.xticks(ticks=candles_visible.index, labels=candles_visible['begin'], rotation=25, ha='right')
        # display candlestick chart
        canvas = FigureCanvasTkAgg(figure, master=self.tabMarket)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, columnspan=2, padx=1, pady=(1, 1), sticky="nsew")

    def on_select(self, event):
        # Получаем выбранный элемент списка
        selected_item = self.list_tickets.get(self.list_tickets.curselection())
        print(selected_item)
        self.market.load_asset_data(selected_item)
        self.plot_price()

def test_one_day():
    # One day system
    market = MarketData(date_begin='2020-01-10', date_end='2023-11-24')
    market.load_asset_data("SBER")
    system = OneDaySystem(data=market, money=10000, lot_size=10, period=5)  # Задаем параметры системы
    tester = Tester(market, system, 10000)
    money_list = tester.test(10)
    statistics = tester.get_statistics()
    return statistics, money_list

def test():
    result = test_one_day()
    return result


if __name__ == "__main__":
    test()
    app = App()
    app.mainloop()

