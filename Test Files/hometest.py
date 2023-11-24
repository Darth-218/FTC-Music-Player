import customtkinter as ctk
from customtkinter import CTk, CTkFrame

win_width , win_height = 1440, 900

root = CTk()
root.title("Niggaplayer")
root.geometry(f"{win_width}x{win_height}")

# Frames

search_frame = CTkFrame(root, width=win_width, height=60, fg_color="yellow")
search_frame.grid(row=0, columnspan=3)

side_lib_list = CTkFrame(root, width=240, height=750, fg_color="black")
side_lib_list.grid(row=1, column=0, rowspan=2)

lyrics_frame = CTkFrame(root, width=900, height=750, fg_color="blue")
lyrics_frame.grid(row=1, column=1, rowspan=2)

cover_frame = CTkFrame(root, width=300, height=250, fg_color="red")
cover_frame.grid(row=1, column=2)

queue_frame = CTkFrame(root, width=300, height=500, fg_color="green")
queue_frame.grid(row=2, column=2)

player_frame = CTkFrame(root, width=win_width, height=210, fg_color="orange")
player_frame.grid(row=3, columnspan=3)


root.mainloop()
