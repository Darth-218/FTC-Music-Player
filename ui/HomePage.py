#!/usr/bin/env /usr/bin/python3
import customtkinter
import SidePane
import TopBar

class HomePage(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=8)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=12)
        self.rowconfigure(2, weight=8)

        self.side_pane = SidePane.SidePane(self)
        self.side_pane.grid(rowspan=3, column=0, sticky='nsew', padx=5, pady=10)

        self.top_bar = TopBar.TopBar(self)
        self.top_bar.grid(row=0, column=1, columnspan=2, sticky='nsew', padx=5, pady=10)

app = HomePage()
app.mainloop()
