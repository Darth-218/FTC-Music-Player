import tkinter
import customtkinter 
from CTkListbox import *
from PIL import *


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")


# app frame
app = customtkinter.CTk()
app.geometry("1440x900")
app.title("Music player")
app.resizable(width=True, height=True)



# Frames
side_frame = customtkinter.CTkFrame(app, width=300, height=910, fg_color='white')
side_frame.grid(row=0, rowspan=3, column=0)

search_bar_frame = customtkinter.CTkFrame(app, width=1145, height=45, fg_color="gray94")
search_bar_frame.grid(row=0, column=1, columnspan=2)

link = customtkinter.CTkEntry(search_bar_frame, width=300, height=40, font=("Systemia",15), fg_color="white", border_color="grey", border_width=2, text_color="grey", corner_radius=50)
link.place(relx=0.05, rely=0.02)

main_frame = customtkinter.CTkFrame(app, width=1140, height=360 , fg_color='gray94')
main_frame.grid(row=1, columnspan=2, column=1)

player_frame = customtkinter.CTkFrame(app, width=400, height= 500, fg_color='white',)
player_frame.grid(row=2, column=2)

# Icons
img_home = customtkinter.CTkImage(dark_image=Image.open(r'c:\Users\alisa\Downloads\home (1).png'), size=(20,20))
img_browse = customtkinter.CTkImage(dark_image=Image.open(r'c:\Users\alisa\Downloads\find.png'), size=(20,20))
img_album = customtkinter.CTkImage(dark_image=Image.open(r'c:\Users\alisa\Downloads\gallery.png'), size=(20,20))
img_artists = customtkinter.CTkImage(dark_image=Image.open(r'c:\Users\alisa\Downloads\artist.png'), size=(20,20))
img_videos = customtkinter.CTkImage(dark_image=Image.open(r'c:\Users\alisa\Downloads\video.png'), size=(20,20))
img_profile = customtkinter.CTkImage(dark_image=Image.open(r'c:\Users\alisa\Downloads\user.png'), size=(80,80))
img_notification = customtkinter.CTkImage(dark_image=Image.open(r'c:\Users\alisa\Downloads\bell.png'), size=(20,20))
img_settings = customtkinter.CTkImage(dark_image=Image.open(r'c:\Users\alisa\Downloads\setting.png'), size=(20,20))
# List box command
def show_value(selected_option):
    print(selected_option)

listbox = CTkListbox(app, width=700, height=480, command=show_value, text_color='black')
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

link.insert(0,'What do you want to listen to?' )
link.bind("<FocusIn>", temp_text)

# Button functions


# Button
Home_btn = customtkinter.CTkButton(side_frame, image=img_home,  width=30, height=15, border_color='white', text='Home', text_color='black', fg_color='white', font=("Systemia",15), hover_color='grey94')
Home_btn.place(relx=0.3, rely=0.2)

Browse_btn = customtkinter.CTkButton(side_frame, image=img_browse, width=30, height=15, border_color='Yellow', text='Browse', text_color='black', fg_color='white', font=("Systemia",15),hover_color='grey94')
Browse_btn.place(relx=0.3, rely=0.3)

Album_btn = customtkinter.CTkButton(side_frame, image=img_album, width=30, height=15, border_color='Yellow', text='Album', text_color='black', fg_color='white', font=("Systemia",15), hover_color='grey94')
Album_btn.place(relx=0.3, rely=0.4)

Artists_btn = customtkinter.CTkButton(side_frame, image=img_artists,  width=30, height=15, border_color='Yellow', text='Artists', text_color='black', fg_color='white', font=("Systemia",15), hover_color='grey94')
Artists_btn.place(relx=0.3, rely=0.5)

Videos_btn = customtkinter.CTkButton(side_frame, image=img_videos, width=30, height=15, border_color='Yellow', text='Videos', text_color='black', fg_color='white', font=("Systemia",15), hover_color='grey94')
Videos_btn.place(relx=0.3, rely=0.6)

Profile_btn = customtkinter.CTkButton(side_frame, image=img_profile, text='', bg_color='white', hover_color='grey94', fg_color='white')
Profile_btn.place(relx=0.24, rely=0.06)

notification_btn = customtkinter.CTkButton(search_bar_frame, image=img_notification, text='', bg_color='grey94', hover_color='white', fg_color='grey94', border_color='white', width=20, height=20)
notification_btn.place(relx=0.87, rely=0.1)

settings_btn = customtkinter.CTkButton(search_bar_frame, image=img_settings, text='', bg_color='grey94', hover_color='white', fg_color='grey94', border_color='white', width=20, height=20)
settings_btn.place(relx=0.9, rely=0.1)
app.mainloop()