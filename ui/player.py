from tkinter import Image
import customtkinter

class Player(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=1)

        self.profile_card = customtkinter.CTkFrame(self, corner_radius=50)
        self.profile_card.grid_columnconfigure(0, weight=1)
        self.profile_card.grid_rowconfigure(0, weight=4)
        self.profile_card.grid_rowconfigure(1, weight=1)
        self.profile_card.grid_rowconfigure(2, weight=1)
        self.profile_card.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # self.profile_image = customtkinter.CTkImage(self.profile_card, dark_image=Image.open(r'./Assets\Images\user.png'), size=(80,80))
        # self.profile_image.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        self.song_name = customtkinter.CTkLabel(self.profile_card, text='Song Name', font=('Systemia', 20))
        self.song_name.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)

        self.profile_name = customtkinter.CTkLabel(self.profile_card, text='User Name', font=('Systemia', 20))
        self.profile_name.grid(row=2, column=0, sticky='nsew', padx=20, pady=20)

        self.controls = customtkinter.CTkFrame(self)
        self.controls.grid_rowconfigure(0, weight=1)
        self.controls.grid_columnconfigure(0, weight=1, pad=10)
        self.controls.grid_columnconfigure(1, weight=1, pad=10)
        self.controls.grid_columnconfigure(2, weight=1, pad=10)
        self.controls.grid_columnconfigure(3, weight=1, pad=10)
        self.controls.grid_columnconfigure(4, weight=1, pad=10)
        self.controls.grid(row=1, column=0, sticky='nsew', padx=20, pady=5)

        size = 50
        radius = 25

        self.previous = customtkinter.CTkButton(self.controls, text='', command=self.button_click, corner_radius=radius, width=size-20, height=size-20)
        self.previous.grid(row=0, column=0, padx=5, pady=10)

        self.previous = customtkinter.CTkButton(self.controls, text='', command=self.button_click, corner_radius=radius, width=size-10, height=size-10)
        self.previous.grid(row=0, column=1, padx=5, pady=5)

        self.play_pause = customtkinter.CTkButton(self.controls, text='', command=self.button_click, corner_radius=radius, width=size, height=size)
        self.play_pause.grid(row=0, column=2, padx=5, pady=10)

        self.next = customtkinter.CTkButton(self.controls, text='', command=self.button_click, corner_radius=radius, width=size-10, height=size-10)
        self.next.grid(row=0, column=3, padx=5, pady=5)

        self.previous = customtkinter.CTkButton(self.controls, text='', command=self.button_click, corner_radius=radius, width=size-20, height=size-20)
        self.previous.grid(row=0, column=4, padx=5, pady=10)

    def button_click(self):
        print('Button clicked in the frame')

app = Player()
app.mainloop()