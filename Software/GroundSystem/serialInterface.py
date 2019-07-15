
from tkinter import *
from tkinter import scrolledtext
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import *
import serial
import serial.tools.list_ports


window = Tk()
window.title("Serial port Interface")
window.geometry('350x250')

combo = Combobox(window)
combo['values']= (1,2,3,4,5,"text")
combo.current(1)
combo.grid(column=0,row=0)

txt = scrolledtext.ScrolledText(window,width=40,height=60)
txt.grid(column=0,row=6)

ports = serial.tools.list_ports.comports()
combo['values']=ports

def on_closing():
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		window.destroy()
		serial.close()

window.protocol("WM_DELETE_WINDOW",on_closing)
window.mainloop()
