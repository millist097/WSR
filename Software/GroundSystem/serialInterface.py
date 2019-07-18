
from tkinter import *
from tkinter import scrolledtext
from tkinter import scrolledtext
from tkinter import messagebox

from tkinter.ttk import *
import serial
import serial.tools.list_ports
import threading


ser = serial.Serial()


window = Tk()
window.title("Serial port Interface")
window.geometry('350x450')

combo = Combobox(window)
ports = serial.tools.list_ports.comports()
combo['values']=ports
combo.current(0)
combo.place(y=40,x=10)



def clicked():
	temp = combo.get()
	temp = temp.split(' ')
	txt.insert(INSERT, temp[0] + ' - Opening Port\n')
	ser.port = temp[0]
	ser.baudrate = 9600
	ser.open()
	if ser.is_open :
		txt.insert(INSERT, 'Port is Open \n')
	else:
		txt.insert(INSERT, 'Port failed to Open\n')
		
btn = Button(window, text='Open Port',command=clicked)
btn.place(y=10,x=10)

def testPort():
	txt.insert(INSERT,ser.is_open)
	
btn2 = Button(window, text='Test Port', command = testPort)
btn2.place(y=10,x=135)


txt = scrolledtext.ScrolledText(window,width=40,height=15)
txt.place(y=60,x=10)



def on_closing():
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		window.destroy()
		if(ser.is_open):
			ser.close()
window.protocol("WM_DELETE_WINDOW",on_closing)
window.mainloop()
