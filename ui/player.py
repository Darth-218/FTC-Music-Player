#!/usr/bin/env /usr/bin/python3
import customtkinter
from PIL import Image


class Player(customtkinter.CTk):
    selected_song = None
    isPlaying = False

    def __init__(self):
        # selected_song = song
        super().__init__()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.profile_card = customtkinter.CTkFrame(self, corner_radius=30)
        self.profile_card.grid_columnconfigure(0, weight=1)
        self.profile_card.grid_rowconfigure(0, weight=4)
        self.profile_card.grid_rowconfigure(1, weight=1)
        self.profile_card.grid_rowconfigure(2, weight=1)
        self.profile_card.grid_rowconfigure(3, weight=1)
        self.profile_card.grid(row=0, column=0, sticky='nsew', padx=20, pady=5)

<<<<<<< Updated upstream
        self.song_image = customtkinter.CTkLabel(
            self.profile_card,
            text='',
            image=customtkinter.CTkImage(
                dark_image=Image.open('././Assets/Images/songTest.jpg'),
                size=(200, 200)),
            corner_radius=50)
=======
        self.song_image = customtkinter.CTkLabel(self.profile_card,text='', image=customtkinter.CTkImage(dark_image=Image.open('../Assets/Images/songTest.jpg'), size=(200,200)), corner_radius=50)
>>>>>>> Stashed changes
        self.song_image.grid(row=0, column=0, sticky='nsew', padx=20, pady=5)

        # self.song_name = customtkinter.CTkLabel(self.profile_card, text=selected_song.name, font=('Systemia', 20))
        self.song_name = customtkinter.CTkLabel(
            self.profile_card, text='selected_song.name', font=('Systemia', 20))
        self.song_name.grid(row=1, column=0, sticky='nsew', padx=20, pady=0)

        # self.profile_name = customtkinter.CTkLabel(self.profile_card, text=selected_song.artist, font=('Systemia', 20))
        self.profile_name = customtkinter.CTkLabel(
            self.profile_card,
            text='selected_song.artist',
            font=('Systemia', 15, 'bold'),
            text_color='gray')
        self.profile_name.grid(row=2, column=0, sticky='nsew', padx=20, pady=0)

        self.timeFrame = customtkinter.CTkFrame(self, corner_radius=30)
        self.timeFrame.grid_columnconfigure(0, weight=1)
        self.timeFrame.grid_columnconfigure(1, weight=1)
        self.timeFrame.grid_rowconfigure(0, weight=1)
        self.timeFrame.grid_rowconfigure(1, weight=1)
        self.timeFrame.grid(row=1, column=0, sticky='nsew', padx=20, pady=5)

        self.slider = customtkinter.CTkSlider(self.timeFrame, corner_radius=10)
        self.slider.grid(row=0, column=0, columnspan=2,
                         sticky='nsew', padx=20, pady=5)
        self.position = customtkinter.CTkLabel(
            self.timeFrame, text='00:00', font=('Systemia', 10))
        self.position.grid(row=1, column=0, sticky='w', padx=20, pady=0)
        self.duration = customtkinter.CTkLabel(
            self.timeFrame, text='00:00', font=('Systemia', 10))
        self.duration.grid(row=1, column=1, sticky='e', padx=20, pady=0)

        self.controls = customtkinter.CTkFrame(self, corner_radius=30)
        self.controls.grid_rowconfigure(0, weight=1)
        self.controls.grid_columnconfigure(0, weight=1, pad=10)
        self.controls.grid_columnconfigure(1, weight=1, pad=10)
        self.controls.grid_columnconfigure(2, weight=1, pad=10)
        self.controls.grid_columnconfigure(3, weight=1, pad=10)
        self.controls.grid_columnconfigure(4, weight=1, pad=10)
        self.controls.grid(row=2, column=0, sticky='nsew', padx=20, pady=5)

        size = 50
        radius = 25

<<<<<<< Updated upstream
        self.shuffle = customtkinter.CTkButton(
            self.controls,
            text='',
            image=customtkinter.CTkImage(dark_image=Image.open(
                '././Assets/Images/shuffle.png')),
            command=self.button_click,
            corner_radius=radius,
            width=size-20,
            height=size-20,
            fg_color="transparent")
        self.shuffle.grid(row=0, column=0, padx=5, pady=10)

        self.previous = customtkinter.CTkButton(
            self.controls,
            text='',
            image=customtkinter.CTkImage(dark_image=Image.open(
                '././Assets/Images/skip_previous.png')),
            command=self.button_click,
            corner_radius=radius,
            width=size-10,
            height=size-10,
            fg_color="transparent")
        self.previous.grid(row=0, column=1, padx=5, pady=5)

        self.play_pause = customtkinter.CTkButton(
            self.controls, text='',
            image=customtkinter.CTkImage(dark_image=Image.open(
                '././Assets/Images/play_arrow.png')),
            command=self.button_click,
            corner_radius=radius,
            width=size, height=size, fg_color="white")
        self.play_pause.grid(row=0, column=2, padx=5, pady=10)

        self.next = customtkinter.CTkButton(
            self.controls,
            text='',
            image=customtkinter.CTkImage(dark_image=Image.open(
                '././Assets/Images/skip_next.png')),
            command=self.button_click,
            corner_radius=radius,
            width=size-10,
            height=size-10,
            fg_color="transparent")
        self.next.grid(row=0, column=3, padx=5, pady=5)

        self.repeat = customtkinter.CTkButton(
            self.controls,
            text='',
            image=customtkinter.CTkImage(dark_image=Image.open(
                '././Assets/Images/repeat.png')),
            command=self.button_click,
            corner_radius=radius,
            width=size-20,
            height=size-20,
            fg_color="transparent")
=======
        self.shuffle = customtkinter.CTkButton(self.controls, text='', image= customtkinter.CTkImage(dark_image=Image.open('../Assets/Images/shuffle.png')), command=self.button_click, corner_radius=radius, width=size-20, height=size-20, fg_color="transparent")
        self.shuffle.grid(row=0, column=0, padx=5, pady=10)

        self.previous = customtkinter.CTkButton(self.controls, text='', image= customtkinter.CTkImage(dark_image=Image.open('../Assets/Images/skip_previous.png')), command=self.button_click, corner_radius=radius, width=size-10, height=size-10, fg_color="transparent")
        self.previous.grid(row=0, column=1, padx=5, pady=5)

        self.play_pause = customtkinter.CTkButton(self.controls, text='', image= customtkinter.CTkImage(dark_image=Image.open('../Assets/Images/play_arrow.png')), command=self.button_click, corner_radius=radius, width=size, height=size, fg_color="white")
        self.play_pause.grid(row=0, column=2, padx=5, pady=10)

        self.next = customtkinter.CTkButton(self.controls, text='', image= customtkinter.CTkImage(dark_image=Image.open('../Assets/Images/skip_next.png')), command=self.button_click, corner_radius=radius, width=size-10, height=size-10, fg_color="transparent")
        self.next.grid(row=0, column=3, padx=5, pady=5)

        self.repeat = customtkinter.CTkButton(self.controls, text='', image= customtkinter.CTkImage(dark_image=Image.open('../Assets/Images/repeat.png')), command=self.button_click, corner_radius=radius, width=size-20, height=size-20, fg_color="transparent")
>>>>>>> Stashed changes
        self.repeat.grid(row=0, column=4, padx=5, pady=10)

    def button_click(self):
        print('Button clicked in the frame')


app = Player()
app.mainloop()
