import tkinter as Tkinter
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from collections import deque
import random

class App:
	def __init__(self, master):

		self.arduinoData = serial.Serial('/dev/ttyACM0', 9600)#115200)

		frame = Tkinter.Frame(master)

		self.running = False
		self.ani = None

		#self.start = Tkinter.LabelFrame(frame, text="Start", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10)
		#self.start.grid(row=0, column=0, padx=20, pady=20)

		self.run = Tkinter.Button(master, text="RUN", bd=10, height=5, width=10, command=self.getData)
		self.run.grid(row=0, column=0, padx=5, pady=5)

		#self.stop_frame = Tkinter.LabelFrame(frame, text="STOP", borderwidth=10, relief=Tkinter.GROOVE, padx=10, pady=10 )
		#self.stop_frame.grid(row=0, column=1, padx=20, pady=20)

		self.stop = Tkinter.Button(master, text="STOP", bd=10, height=5, width=10, command=self.stopTest)
		self.stop.grid(row=0, column=1, padx=5, pady=5)

		self.fig = plt.Figure()
		self.ax1 = self.fig.add_subplot(111)
		self.line0, = self.ax1.plot([], [], lw=2)

		self.canvas = FigureCanvasTkAgg(self.fig,master=master)
		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row=0, column=4, padx=20, pady=20)
		frame.grid(row=0, column=0, padx=20, pady=20)

	def getData(self):
		if self.ani is None:
			self.k = 0
			self.arduinoData.flushInput()
			#self.arduinoData.write("<L>")
			self.start()
			retun
		else:
			#self.arduinoData.write("<L>")
			self.arduinoData.flushInput()
			self.ani.event_source.start()
			
		self.running = not self.running

	def stopTest(self):
		#self.arduinoData.write("<H>")
		if self.running:
			self.ani.event_source.stop()
		self.running = not self.running

	def resetTest(self):
		self.k = 0
		self.xdata = []
		self.ydata = []
		self.line0.set_data(self.xdata, self.ydata1)
		
		self.ax1.set_ylim(0,1)
		self.ax1.set_xlim(0,1)
		

	def start(self):
		self.xdata = []
		self.ydata = []

		self.k = 0
		self.arduinoData.flushInput()
		self.ani = animation.FuncAnimation(
			self.fig,
			self.update_graph,
			interval=1,
			repeat=True)
		#self.arduinoData.write("<L>")
		self.running = True
		self.ani._start()

	def update_graph(self, i):
		self.xdata.append(self.k)
		while (self.arduinoData.inWaiting()==0):
			pass
		x = self.arduinoData.readline()
		#strip_data = x.strip()
		split_data = x.split(",")

		self.xdata.append(split_data[1])
		self.ydata.append(split_data[0])
		self.line1.set_data(self.xdata, self.ydata)
		if self.k < 49:
			self.ax1.set_ylim(min(self.pressure1)-1, max(self.pressure3) + 1)
			self.ax1.set_xlim(0, self.k+1)
			self.ax2.set_ylim(min(self.displacement1)-1, max(self.displacement3) + 1)
			self.ax2.set_xlim(0, self.k+1)
		elif self.k >= 49:
			self.ax1.set_ylim(min(self.pressure1[self.k-49:self.k])-1, max(self.pressure3[self.k-49:self.k]) + 1)
			self.ax1.set_xlim(self.xdata[self.k-49], self.xdata[self.k-1])
			self.ax2.set_ylim(min(self.displacement1[self.k-49:self.k])-1, max(self.displacement3[self.k-49:self.k]) + 1)
			self.ax2.set_xlim(self.xdata[self.k-49], self.xdata[self.k-1])
		self.k += 1




root = Tkinter.Tk()
app = App(root)
root.mainloop()