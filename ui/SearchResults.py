import sys
sys.path.append('./')
import customtkinter
import CTkListbox
import api_client.Youtube.youtube as yt
import api_client.Youtube.api_models as yt_models
import threading
import time
import ArtistWidget
from PIL import Image

class SearchResultsFrame(customtkinter.CTk):
    # def __init__(self, master, **kwargs):
    def __init__(self):
        # super().__init__(master, **kwargs)
        super().__init__()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        searchRequest = yt_models.SearchRequest(query="Jacob's Piano", artist_count=1, album_count=5, song_count=20)

        # searchResponseThread = threading.Thread(target=yt.search(searchRequest))
        # searchResponseThread.start()
        # searchResponseThread.join()
        # searchResponse = searchResponseThread.result

        searchResponse = yt.search(searchRequest)
        allResults = searchResponse.artists + searchResponse.albums + searchResponse.songs

        self.search_results = customtkinter.CTkScrollableFrame(self, border_color='grey34', corner_radius=10)
        self.search_results.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        for i, result in enumerate(searchResponse.artists):
            self.search_results.grid_rowconfigure(i, weight=0)
            self.resultWidget = customtkinter.CTkButton(text=result.name, 
                                                        image=customtkinter.CTkImage(dark_image=Image.open(result.cover_art),
                                                                                        size=(100,100)), 
                                                        fg_color='transparent', 
                                                        hover_color='grey34')
            self.resultWidget.grid(row=i, column=0, sticky='nsew', padx=10, pady=10)
            

        self.search_results.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))

app = SearchResultsFrame()
app.mainloop()