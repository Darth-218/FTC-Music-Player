import customtkinter

class SideBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.button = customtkinter.CTkButton(self, text='Click me in the frame', command=self.button_click)
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

    def button_click(self):
        print('Button clicked in the frame')

class Home(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1920x1080')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.button = customtkinter.CTkButton(self, text='Click me', command=self.button_click)
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

        self.frame = SideBar(self)
        self.frame.grid(row=0, column=1, sticky='nsew')
    def button_click(self):
        print('Button clicked')

app = Home()
app.mainloop()