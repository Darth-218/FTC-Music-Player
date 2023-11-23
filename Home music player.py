import tkinter
import customtkinter


# system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# our app frame
app = customtkinter.CTk()
app.geometry("1440x900")
app.title("Music player")

# Variables
border_radius = 10

# Frames

frame_1 = customtkinter.CTkFrame(app,fg_color='black')
frame_1.pack(expand=True,fill='both')


frame_2 = customtkinter.CTkFrame(frame_1,corner_radius=border_radius)
frame_2.pack(side="right", fill="both", expand=True, padx=(150,420), pady=(40,95))

frame_3 = customtkinter.CTkFrame(frame_1,width=120, height=200, corner_radius=border_radius)
frame_3.place(relx=0.0135, rely=0.045)

frame_4 = customtkinter.CTkFrame(frame_1, width=120, height=555, corner_radius=border_radius)
frame_4.place(relx=0.0135, rely=0.28)

frame_5 = customtkinter.CTkFrame(frame_1,width=1440, height=90, fg_color='gray')
frame_5.place(relx=0, rely=0.9)

frame_6 = customtkinter.CTkFrame(frame_1,width=360, height=760, corner_radius=border_radius)
frame_6.place(relx=0.715, rely=0.045)

# Link input
link = customtkinter.CTkEntry(frame_2, width=350, height=40, font=("Systemia",15), fg_color="gray10", border_color="white", border_width=0.5, text_color="grey", corner_radius=border_radius)
link.place(relx=0.05, rely=0.02)

# Dissapearing text in entry
def temp_text(e):
    link.delete(0, "end")

link.insert(0, "What do you want to listen to?")
link.bind("<FocusIn>", temp_text)





# Run app
app.mainloop()

