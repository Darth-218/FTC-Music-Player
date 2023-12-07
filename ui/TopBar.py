import sys
sys.path.append("./")
import customtkinter

class TopBar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=8)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.searchBar = customtkinter.CTkEntry(self, placeholder_text="What do you want to listen to?", corner_radius=50)
        self.searchBar.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.notificationBtn = customtkinter.CTkButton(self, text="Notification", image="./Assets/Images/bell.png", fg_color='transparent', hover_color='grey34')
        self.notificationBtn.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        self.settingsBtn = customtkinter.CTkButton(self, text="Settings", image="./Assets/Images/setting.png", fg_color='transparent', hover_color='grey34')
        self.settingsBtn.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)