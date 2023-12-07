import tkinter
import tkinter.messagebox
import customtkinter
from MarketData import MarketData
from pandastable import Table, TableModel

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
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
        self.sidebar_frame = customtkinter.CTkFrame(self, width=10, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, pady=(1,1), sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Лаборатория\nСтратегий", font=customtkinter.CTkFont(family="Arial", size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Создать стратегию", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Тестировать", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Опубликовать", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Тема:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Масштаб:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, corner_radius=10)
        self.tabview.grid(row=0, column=1, padx=(5, 1), pady=(0, 1), sticky="nsew")
        self.tabview.add("Рынок")
        self.tabview.add("Стратегии")
        self.tabview.add("Тестирование")
        self.tabview.tab("Рынок").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Стратегии").grid_columnconfigure(0, weight=1)

        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Рынок"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Рынок"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Стратегии"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # set default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        self.market = MarketData()
        self.tickets = self.market.get_stocks_list()

        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Рынок"), values=self.tickets)
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))


if __name__ == "__main__":
    app = App()
    app.mainloop()
