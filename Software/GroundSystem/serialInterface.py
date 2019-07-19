from tkinter import *
from tkinter import scrolledtext
from tkinter import scrolledtext
from tkinter import messagebox

from tkinter.ttk import *
import serial as Serial
import serial.tools.list_ports
import threading
import time
import random
import queue as Queue
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from collections import deque

class GuiPart:
	
	def __init__(self, master, receivedQueue, sendQueue, serialIn, endCommand):
		self.receivedQueue = receivedQueue
		# Set up the GUI
		self.xdata = []
		self.ydata = []
		self.ser = serialIn
		self.count = 0
		
		portList = Combobox(master, state="readonly")
		ports = serial.tools.list_ports.comports()
		portList['values']=ports
		portList.current(0)
		portList.place(y=40,x=10, width=150)
		
		baudRateCombo = Combobox(master, state="readonly")
		baudRateCombo['values'] = [9600,115200]
		baudRateCombo.current(0)
		baudRateCombo.place( y = 40, x = 170, width = 80)
		
		def openPort():
			if self.ser.is_open:
				self.ser.close()
				self.txt.insert(INSERT,'Port closed\n')
				
			temp = portList.get()
			temp = temp.split(' ')
			self.txt.insert(INSERT, temp[0] + ' - Opening Port\n')
			self.ser.port = temp[0]
			self.ser.baudrate = 9600
			self.ser.open()
			#ser.flushInput()
			if self.ser.is_open :
				self.txt.insert(INSERT, 'Port is Open \n')
			else:
				self.txt.insert(INSERT, 'Port failed to Open\n')
				
		def closePort():
			if self.ser.is_open:
				self.ser.close()
				time.sleep(.15)
				self.txt.insert(INSERT,'Port closed\n')
			else:
				self.txt.insert(INSERT,'No Port is Open\n')
				
		def updatePortList():
			ports = serial.tools.list_ports.comports()
			portList['values']=ports
			
		def sendData():
			sendQueue.put(serialInput.get())
			
		openPort_btn = Button(master, text='Open Port',command=openPort)
		openPort_btn.place(y=10,x=10)
		
		getPorts = Button(master, text='Find Ports', command=updatePortList)
		getPorts.place( x = 100, y=10)
		
		closePort_btn = Button(master, text='Close Port', command=closePort)
		closePort_btn.place(y=10, x= 190)
		
		self.txt = scrolledtext.ScrolledText(master,width=40,height=15)
		self.txt.place(y=60,x=10)
		
		serialInput = Entry(master,width=20)
		serialInput.place(x =10,y=300)
		
		
		serialSend_btn = Button(master, text='Send', command = sendData)
		serialSend_btn.place(x = 190, y=300)
		
		def on_closing():
			if messagebox.askokcancel("Quit", "Do you want to quit?"):
				master.destroy()
				if(self.ser.is_open):
					self.ser.close()
				endCommand()
		master.protocol("WM_DELETE_WINDOW",on_closing)
		# Add more GUI stuff here depending on your specific needs

		#frame = Frame(master,width=30, height=150)

		
		self.fig = plt.Figure()
		self.ax1 = self.fig.add_subplot(111)
		self.line0, = self.ax1.plot([], [], lw=2)

		self.canvas = FigureCanvasTkAgg(self.fig,master=master)
		self.canvas.draw()
		self.canvas.get_tk_widget().place(x=325,y=10,height=300,width=300)
		#frame.place(x=200,y=10)
		

				

		self.ani = animation.FuncAnimation(
					self.fig,
					self.update_graph,
					interval=1,
					repeat=True)
	
	def update_graph(self, i, ):
		if self.ser.is_open:
			self.line0.set_data(self.xdata, self.ydata)
			if  self.count >2 and len(self.xdata) < 49:
				self.ax1.set_ylim(min(self.ydata)-1, max(self.ydata) + 1)
				self.ax1.set_xlim(min(self.xdata)-1, self.count+1)
			else:
				self.ax1.set_ylim(min(self.ydata)-1, max(self.ydata) + 1)
				self.ax1.set_ylim(self.xdata[len(self.xdata)-50], self.count+1)
			
				
	def processIncoming(self):
		"""Handle all messages currently in the queue, if any."""
		while self.receivedQueue.qsize(  )>1:
			try:
				msg = self.receivedQueue.get(0)
				# Check contents of message and do whatever is needed. As a
				# simple test, print it (in real life, you would
				# suitably update the GUI's display in a richer fashion).
				self.txt.insert(INSERT, msg)
				self.txt.insert(INSERT, '\n')
				self.txt.see("end")
				self.xdata.append(int(msg[4]))
				self.ydata.append(int(msg[1]))
				self.count = int(msg[4])
				#print(msg)
			except Queue.Empty:
				# just on general principles, although we don't
				# expect this branch to be taken in this case
				pass

class ThreadedClient:
	"""
	Launch the main part of the GUI and the worker thread. periodicCall and
	endApplication could reside in the GUI part, but putting them here
	means that you have all the thread controls in a single place.
	"""
	def __init__(self, master):
		"""
		Start the GUI and the asynchronous threads. We are in the main
		(original) thread of the application, which will later be used by
		the GUI as well. We spawn a new thread for the worker (I/O).
		"""
		self.master = master

		# Create the queue
		self.receivedQueue = Queue.Queue(  )
		self.sendQueue = Queue.Queue()
		
		# Create Serial instance
		self.ser = Serial.Serial(timeout=1)
		
		# Set up the GUI part
		self.gui = GuiPart(master, self.receivedQueue, self.sendQueue,self.ser, self.endApplication)

		# Set up the thread to do asynchronous I/O
		# More threads can also be created and used, if necessary
		self.running = 1
		self.thread1 = threading.Thread(target=self.workerThread1)
		self.thread1.start(  )

		# Start the periodic call in the GUI to check if the queue contains
		# anything
		self.periodicCall(  )

	def periodicCall(self):
		"""
		Check every 200 ms if there is something new in the queue.
		"""
		self.gui.processIncoming(  )
		if not self.running:
			# This is the brutal stop of the system. You may want to do
			# some cleanup before actually shutting it down.
			import sys
			sys.exit(1)
		self.master.after(200, self.periodicCall)

	def workerThread1(self):
		"""
		This is where we handle the asynchronous I/O. For example, it may be
		a 'select(  )'. One important thing to remember is that the thread has
		to yield control pretty regularly, by select or otherwise.
		"""
		while self.running:

			if self.ser.is_open:
				#print(self.ser.port)
				time.sleep(.010)
				msg = self.ser.readline()
				msg = msg.strip()
				stringMsg = msg.decode("utf-8")
				stringMsg = stringMsg.split(',')
				self.receivedQueue.put(stringMsg)

				while self.sendQueue.qsize(  ):
					try:
						msg = self.sendQueue.get(0)
						self.ser.write((msg+'\n').encode("utf-8"))
					except Queue.Empty:
						# just on general principles, although we don't
						# expect this branch to be taken in this case
						pass
	def endApplication(self):
		self.running = 0

rand = random.Random(  )
window = Tk()
window.title("Serial port Interface")
window.geometry('350x450')

client = ThreadedClient(window)
window.mainloop(  )