from typing import Optional, Tuple, Union
import customtkinter
import api_client.Youtube.api_models as yt_models

class ArtistWidget(customtkinter.CTkFrame):
    def __init__(self, master, artist:yt_models.OnlineArtist):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        
        self.image=customtkinter.CTkLabel(self, image=artist.cover_art, width=100, height=100)
        self.image.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        self.artist_name = customtkinter.CTkLabel(self, text=artist.name, font=('Helvetica', 20))
        self.artist_name.grid(row=0, column=1, sticky='w', padx=10, pady=10)