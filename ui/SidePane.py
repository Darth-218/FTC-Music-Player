import customtkinter
from PIL import Image

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

        self.profileBtn = customtkinter.CTkButton(self, text="Profile", fg_color='transparent', hover_color='grey34')
        self.homeBtn = customtkinter.CTkButton(self,
                                                text="Home",
                                                fg_color='transparent',
                                                hover_color='grey34',
                                                image=customtkinter.CTkImage(dark_image=Image.open('./Assets/Images/home.png'), size=(20,20)))
        self.browseBtn = customtkinter.CTkButton(self,
                                                text="Browse",
                                                fg_color='transparent',
                                                hover_color='grey34',
                                                image=customtkinter.CTkImage(dark_image=Image.open('./Assets/Images/find.png'), size=(20,20)))
        self.albumBtn = customtkinter.CTkButton(self,
                                                text="Albums",
                                                fg_color='transparent',
                                                hover_color='grey34',
                                                image=customtkinter.CTkImage(dark_image=Image.open('./Assets/Images/gallery.png'), size=(20,20)))
        self.artistsBtn = customtkinter.CTkButton(self,
                                                text="Artists",
                                                fg_color='transparent',
                                                hover_color='grey34',
                                                image=customtkinter.CTkImage(dark_image=Image.open('./Assets/Images/artist.png'), size=(20,20)))
        self.videosBtn = customtkinter.CTkButton(self,
                                                text="Videos",
                                                fg_color='transparent', 
                                                hover_color='grey34',
                                                image=customtkinter.CTkImage(dark_image=Image.open('./Assets/Images/video.png'), size=(20,20)))

        xpadding = 10
        ypadding = 10

        self.profileBtn.grid(row=0, column=0, sticky='nsew', padx=xpadding, pady=ypadding)
        self.homeBtn.grid(row=1, column=0, sticky='ew', padx=xpadding, pady=ypadding)
        self.browseBtn.grid(row=2, column=0, sticky='ew', padx=xpadding, pady=ypadding)
        self.albumBtn.grid(row=3, column=0, sticky='ew', padx=xpadding, pady=ypadding)
        self.artistsBtn.grid(row=4, column=0, sticky='ew', padx=xpadding, pady=ypadding)
        self.videosBtn.grid(row=5, column=0, sticky='ew', padx=xpadding, pady=ypadding)
