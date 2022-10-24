from tkinter import *
import os



#homepage settings
window = Tk()

#setting up window geometry 
window.geometry("600x600")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 600,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

#button function, closes current file and opens game file
def call_otherfile():
    os.system("main.py") #Execute new script 
    os.close() #close Current Script 

#background image
background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    -408.5, -260.5,
    image=background_img)

#button pack
img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = call_otherfile,
    relief = "flat")

b0.place(
    x = -512, y = -5,
    width = 187,
    height = 58)

window.resizable(False, False)
window.mainloop()
