import os
import threading
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk

# Extracting current path of the application
current_path = os.getcwd()
import yt_music_downloader

# -------------------------------------CREATING FUNCTIONS-------------------------------------
def download_song():
  song = entry.get()
  if song == '':
    return
  print(song)
  sub_btn.config(text="Please wait...", state=DISABLED)
  threading.Thread(target=download_song_thread, args=(song,)).start()

def download_song_thread(song):
  return_value = yt_music_downloader.download_song(song)
  entry.delete(0, END)
  output.insert('1.0', f"{return_value}\n\n")
  entry.focus_force()
  root.after(0, reset_button_text)

def reset_button_text():
  sub_btn.config(text="Download", state=NORMAL)


# -------------------------------------CONFIGURING THE WINDOW-------------------------------------
root = Tk()
root.title("Song Downloader")
root.geometry("700x550")

try:
  path = f"{current_path}\\icon.jpeg"
  image = Image.open(path)
  photo = ImageTk.PhotoImage(image)
  root.iconphoto(False, photo)
except:
  pass

# TO STYLE THE LABEL
style = ttk.Style()
style.configure('TEntry', foreground = 'red')


# -------------------------------------LABELS, ENTRY AND MORE -------------------------------------
song_name = StringVar()
lbl_song_name = Label(root, text="Enter the song name below: ", font=("Arial", 25))

entry = ttk.Entry(root, textvariable = song_name, font=('calibre',21,'bold'), justify= CENTER)
entry.bind('<Return>', lambda event: download_song())

sub_btn = ttk.Button(root, text = 'Download', command = download_song)

output_frame = Frame(root, bg='light grey' )
output_lbl = Label(output_frame, text="Output:", font=("Arial"))
scrollbar = Scrollbar(output_frame)
scrollbar.pack(side=RIGHT, fill=Y)
output = Text(output_frame, yscrollcommand=scrollbar.set, font=('calibre'), background="light grey")
scrollbar.config(command=output.yview)


# -------------------------------------ADDING ELEMENTS TO THE MAIN WINDOW-------------------------------------
lbl_song_name.pack(pady=20)
entry.focus_force()
entry.pack(side = TOP, ipadx = 30, ipady = 8)
sub_btn.pack(side = TOP, ipadx = 30, ipady = 10, pady=20)
output_frame.pack(side=BOTTOM, ipadx = 500, ipady = 200)
output_lbl.pack()
output.pack(side=LEFT, fill=BOTH, expand=True)

root.mainloop()
