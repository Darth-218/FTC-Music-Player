import customtkinter

class SidePane(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=8)
        self.grid_columnconfigure(0, weight=1)

        self.profileBtn = customtkinter.CTkButton(self, text="Profile")
        self.homeBtn = customtkinter.CTkButton(self, text="Home")
        self.browseBtn = customtkinter.CTkButton(self, text="Browse")
        self.albumBtn = customtkinter.CTkButton(self, text="Album")
        self.artistsBtn = customtkinter.CTkButton(self, text="Artists")
        self.videosBtn = customtkinter.CTkButton(self, text="Videos")

        xpadding = 10
        ypadding = 10

        self.profileBtn.grid(row=0, column=0, sticky='nsew', padx=xpadding, pady=ypadding)
        self.homeBtn.grid(row=1, column=0, sticky='ew', padx=xpadding, pady=ypadding)
        self.browseBtn.grid(row=2, column=0, sticky='ew', padx=xpadding, pady=ypadding)
        self.albumBtn.grid(row=3, column=0, sticky='ew', padx=xpadding, pady=ypadding)
        self.artistsBtn.grid(row=4, column=0, sticky='ew', padx=xpadding, pady=ypadding)
        self.videosBtn.grid(row=5, column=0, sticky='ew', padx=xpadding, pady=ypadding)
