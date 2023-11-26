import customtkinter
from CTkListbox import *


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")


# app frame
app = customtkinter.CTk()
app.geometry("1440x900")
app.title("Music player")


# Frames
side_frame = customtkinter.CTkFrame(app, width=300, height=900, fg_color='yellow')
side_frame.grid(row=0, rowspan=3, column=0)

search_bar_frame = customtkinter.CTkFrame(app, width=1140, height=45, fg_color="cyan")
search_bar_frame.grid(row=0, column=1, columnspan=2)

link = customtkinter.CTkEntry(search_bar_frame, width=300, height=40, font=("Systemia",15), fg_color="gray10", border_color="white", border_width=0.5, text_color="grey", corner_radius=50)
link.place(relx=0.37, rely=0.02)

main_frame = customtkinter.CTkFrame(app, width=1140, height=360 , fg_color='blue')
main_frame.grid(row=1, columnspan=2, column=1)

player_frame = customtkinter.CTkFrame(app, width=400, height= 500, fg_color='purple')
player_frame.grid(row=2, column=2)

# List box command
def show_value(selected_option):
    print(selected_option)

listbox = CTkListbox(app, width=700, height=480, command=show_value, text_color='black' )
listbox.grid(row=2, column=1)

listbox.insert(0, "Option 0")
listbox.insert(1, "Option 1")
listbox.insert(2, "Option 2")
listbox.insert(3, "Option 3")
listbox.insert(4, "Option 4")
listbox.insert(5, "Option 5")
listbox.insert(6, "Option 6")
listbox.insert(7, "Option 7")
listbox.insert("END", "Option 8")


# Dissapearing text in entry
def temp_text(e):
    link.delete(0, "end")

link.insert(0, "What do you want to listen to?")
link.bind("<FocusIn>", temp_text)

# Button functions

    

# Button
Home_btn = customtkinter.CTkButton(side_frame, width=30, height=15, border_color='Yellow', text='Home', text_color='black', fg_color='yellow', font=("Systemia",15))
Home_btn.place(relx=0.4, rely=0.1)

Browse_btn = customtkinter.CTkButton(side_frame, width=30, height=15, border_color='Yellow', text='Browse', text_color='black', fg_color='yellow', font=("Systemia",15))
Browse_btn.place(relx=0.39, rely=0.2)

Album_btn = customtkinter.CTkButton(side_frame, width=30, height=15, border_color='Yellow', text='Album', text_color='black', fg_color='yellow', font=("Systemia",15))
Album_btn.place(relx=0.39, rely=0.3)

Artists_btn = customtkinter.CTkButton(side_frame, width=30, height=15, border_color='Yellow', text='Artists', text_color='black', fg_color='yellow', font=("Systemia",15))
Artists_btn.place(relx=0.39, rely=0.4)

Videos_btn = customtkinter.CTkButton(side_frame, width=30, height=15, border_color='Yellow', text='Videos', text_color='black', fg_color='yellow', font=("Systemia",15))
Videos_btn.place(relx=0.39, rely=0.5)

app.mainloop()
