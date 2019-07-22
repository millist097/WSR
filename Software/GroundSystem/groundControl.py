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
from scipy import integrate
import numpy as np
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
		self.accel_data_X = []
		self.accel_data_Y = []
		self.accel_data_Z = []
		self.gyro_data = []
		self.mag_data = []
		self.euler_data = []
		self.vel_data_X = [0]
		self.vel_data_Y = [0]
		self.vel_data_Z = [0]
		self.timeStamp = []
		
		self.ser = serialIn
		self.count = 0
		
		portList = Combobox(master, state="readonly")
		ports = serial.tools.list_ports.comports()
		portList['values']=ports
		#portList.current(0)
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
				time.sleep(.3)
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
		
		self.linAccel_y_position = 340
		accelMain_lbl = Label(master, text = 'Linear Acceleration Raw Data')
		accelMain_lbl.place(x=10, y= self.linAccel_y_position-16)
		
		accel_x_lbl = Label( master, text='X:')
		accel_x_lbl.place(x=10, y=self.linAccel_y_position+4)
		accel_x_txt = Text(master, height=1,width = 7)
		accel_x_txt.place(x = 25, y=self.linAccel_y_position)
		
		accel_y_lbl = Label(master, text='Y:')
		accel_y_lbl.place(x=85, y=self.linAccel_y_position+4)
		accel_y_txt = Text(master, height=1,width=7)
		accel_y_txt.place(x=100,y=self.linAccel_y_position)
		
		accel_z_lbl = Label(master, text='Z:')
		accel_z_lbl.place(x=160,y=self.linAccel_y_position+4)
		accel_z_txt = Text(master,height=1, width=7)
		accel_z_txt.place(x=175,y=self.linAccel_y_position)
		
		
		self.vel_y_position = 380
		velMain_lbl = Label(master, text = 'Velocity Raw Data')
		velMain_lbl.place(x=10, y= self.vel_y_position-16)
		
		vel_x_lbl = Label( master, text='X:')
		vel_x_lbl.place(x=10, y=self.vel_y_position+4)
		vel_x_txt = Text(master, height=1,width = 7)
		vel_x_txt.place(x = 25, y=self.vel_y_position)
		
		vel_y_lbl = Label(master, text='Y:')
		vel_y_lbl.place(x=85, y=self.vel_y_position+4)
		vel_y_txt = Text(master, height=1,width=7)
		vel_y_txt.place(x=100,y=self.vel_y_position)
		
		vel_z_lbl = Label(master, text='Z:')
		vel_z_lbl.place(x=160,y=self.vel_y_position+4)
		vel_z_txt = Text(master,height=1, width=7)
		vel_z_txt.place(x=175,y=self.vel_y_position)
		
		self.gyro_y_positon = 420
		gyroMain_lbl = Label(master, text = 'Gyro Raw Data')
		gyroMain_lbl.place(x=10, y= self.gyro_y_positon-16)
		
		gyro_x_lbl = Label( master, text='X:')
		gyro_x_lbl.place(x=10, y=self.gyro_y_positon+4)
		gyro_x_txt = Text(master, height=1,width = 7)
		gyro_x_txt.place(x = 25, y=self.gyro_y_positon)
		
		gyro_y_lbl = Label(master, text='Y:')
		gyro_y_lbl.place(x=85, y=self.gyro_y_positon+4)
		gyro_y_txt = Text(master, height=1,width=7)
		gyro_y_txt.place(x=100,y=self.gyro_y_positon)
		
		gyro_z_lbl = Label(master, text='Z:')
		gyro_z_lbl.place(x=160,y=self.gyro_y_positon+4)
		gyro_z_txt = Text(master,height=1, width=7)
		gyro_z_txt.place(x=175,y=self.gyro_y_positon)
		
		def on_closing():
			if messagebox.askokcancel("Quit", "Do you want to quit?"):
				master.destroy()
				if(self.ser.is_open):
					self.ser.close()
				endCommand()
		master.protocol("WM_DELETE_WINDOW",on_closing)
		# Add more GUI stuff here depending on your specific needs

		#frame = Frame(master,width=30, height=150)

		self.graphWidth = 450
		self.graphHeight = 275
		self.graphSide = 325
		
		self.fig_accel = plt.Figure()
		self.ax1 = self.fig_accel.add_subplot(111)
		self.ax1.grid()
		self.ax1.set_title('Acceleration')
		self.ax1.set_xlabel('timeStamp')
		self.ax1.set_ylabel('[m/s/s]')
		self.fig_accel.subplots_adjust(bottom=0.17)
		self.accel_line0, = self.ax1.plot([], [], lw=1, Label='X-axis')
		self.accel_line1, = self.ax1.plot([], [], lw=1, Label='Y-axis')
		self.accel_line2, = self.ax1.plot([], [], lw=1, Label='Z-axis')
		self.ax1.legend(loc='upper right')
		self.accel_canvas = FigureCanvasTkAgg(self.fig_accel,master=master)
		self.accel_canvas.draw()
		self.accel_canvas.get_tk_widget().place(x=self.graphSide,y=10,height=self.graphHeight,width=self.graphWidth)
		self.ani_accel = animation.FuncAnimation(	self.fig_accel,self.update_accel_graph,interval=1,repeat=True)
	
		self.fig_vel = plt.Figure()
		self.ax2 = self.fig_vel.add_subplot(111)
		self.ax2.grid()
		self.ax2.set_title('Velocity')
		self.ax2.set_xlabel('Time [s]')
		self.ax2.set_ylabel('[m/s]')
		self.fig_vel.subplots_adjust(bottom=.17)
		self.vel_line0, = self.ax2.plot([], [], lw=1, Label='X-axis')
		self.vel_line1, = self.ax2.plot([], [], lw=1, Label='Y-axis')
		self.vel_line2, = self.ax2.plot([], [], lw=1, Label='Z-axis')
		self.ax2.legend(loc='upper right')
		self.velocity_canvas = FigureCanvasTkAgg(self.fig_vel,master=master)
		self.velocity_canvas.draw()
		self.velocity_canvas.get_tk_widget().place(x=self.graphSide, y =20+self.graphHeight, height=self.graphHeight, width=self.graphWidth)
		self.ani_velocity = animation.FuncAnimation( self.fig_vel, self.update_velocity_graph, interval=1, repeat=True)
		
	def update_accel_graph(self, i ):
		if self.ser.is_open and len(self.timeStamp)>0:					
				
			if  len(self.timeStamp) >2 and len(self.timeStamp) < 49:
				self.accel_line0.set_data(self.timeStamp, self.accel_data_X)
				self.accel_line1.set_data(self.timeStamp, self.accel_data_Y)
				self.accel_line2.set_data(self.timeStamp, self.accel_data_Z)
				accelMin = min([min(self.accel_data_X), min(self.accel_data_Y), min(self.accel_data_Z)])
				accelMax = max([max(self.accel_data_X), max(self.accel_data_Y),max(self.accel_data_Z)])
				self.ax1.set_ylim(accelMin-1, accelMax + 1)
				self.ax1.set_xlim(min(self.timeStamp)-1, max(self.timeStamp)+1)
			else:
				self.accel_line0.set_data(self.timeStamp[-50:], self.accel_data_X[-50:])
				self.accel_line1.set_data(self.timeStamp[-50:], self.accel_data_Y[-50:])
				self.accel_line2.set_data(self.timeStamp[-50:], self.accel_data_Z[-50:])
				accelMin = min([min(self.accel_data_X[-50:]), min(self.accel_data_Y[-50:]),min(self.accel_data_Z[-50:])])
				accelMax = max([max(self.accel_data_X[-50:]), max(self.accel_data_Y[-50:]),max(self.accel_data_Z[-50:])])
				self.ax1.set_ylim(accelMin-1, accelMax+ 1)
				self.ax1.set_xlim(min(self.timeStamp[-50:])-1, max(self.timeStamp[-50:])+1)
			
	def update_velocity_graph(self, i):
		if self.ser.is_open and len(self.timeStamp)>0:

			if   len(self.timeStamp) < 49:
				self.vel_line0.set_data(self.timeStamp, self.vel_data_X)
				self.vel_line1.set_data(self.timeStamp, self.vel_data_Y)
				self.vel_line2.set_data(self.timeStamp, self.vel_data_Z)

				velMin = min([min(self.vel_data_X), min(self.vel_data_Y), min(self.vel_data_Z)])
				velMax = max([max(self.vel_data_X), max(self.vel_data_Y), max(self.vel_data_Z)])
				self.ax2.set_ylim(velMin-1, velMax + 1)
				self.ax2.set_xlim(min(self.timeStamp)-1, max(self.timeStamp)+1)
			else:
				self.vel_line0.set_data(self.timeStamp[-50:], self.vel_data_X[-50:])
				self.vel_line1.set_data(self.timeStamp[-50:], self.vel_data_Y[-50:])
				self.vel_line2.set_data(self.timeStamp[-50:], self.vel_data_Z[-50:])
				velMin = min([min(self.vel_data_X[-50:]), min(self.vel_data_Y[-50:]),min(self.vel_data_Z[-50:])])
				velMax = max([max(self.vel_data_X[-50:]), max(self.vel_data_Y[-50:]),max(self.vel_data_Z[-50:])])
				self.ax2.set_ylim(velMin-1, velMax+ 1)
				self.ax2.set_xlim(min(self.timeStamp[-50:])-1, max(self.timeStamp[-50:])+1)		
					
					
	def processIncoming(self):
		"""Handle all messages currently in the queue, if any."""
		while self.receivedQueue.qsize(  )>1:
			try:
				msg = self.receivedQueue.get(0)
				if msg[0] == 'ECHO':
					self.txt.insert(INSERT,msg)
					self.txt.insert(INSERT, '\n')
				elif msg[0] == 'DATA':
					self.txt.insert(INSERT, msg)
					self.txt.insert(INSERT, '\n')
					self.txt.see("end")
					self.accel_data_X.append(float(msg[1]))
					self.accel_data_Y.append(float(msg[2]))
					self.accel_data_Z.append(float(msg[3]))
					
					self.mag_data.append([float(msg[4]), float(msg[5]), float(msg[6])])
					self.gyro_data.append([float(msg[7]), float(msg[8]), float(msg[9])])
					self.euler_data.append([float(msg[10]), float(msg[11]), float(msg[12])])
					self.timeStamp.append(int(msg[13])/1000.0)
					self.count = int(msg[14])
					
					if len(self.timeStamp)>1:
						dt = self.timeStamp[-1]-self.timeStamp[-2]
						self.vel_data_X.append((dt*((self.accel_data_X[-1]+self.accel_data_X[-2])/2.0))+self.vel_data_X[-1])
						self.vel_data_Y.append((dt*((self.accel_data_Y[-1]+self.accel_data_Y[-2])/2.0))+self.vel_data_Y[-1])
						self.vel_data_Z.append((dt*((self.accel_data_Z[-1]+self.accel_data_Z[-2])/2.0))+self.vel_data_Z[-1])
					
				elif msg[0] == 'STATE':
					self.txt.insert(INSERT,msg)
					self.txt.insert(INSERT, '\n')
				
					
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
		#print("test")
		self.master.after(500, self.periodicCall)

	def workerThread1(self):
		"""
		This is where we handle the asynchronous I/O. For example, it may be
		a 'select(  )'. One important thing to remember is that the thread has
		to yield control pretty regularly, by select or otherwise.
		"""
		while self.running:
			time.sleep(.150)
			if self.ser.is_open:
				#print(self.ser.port)
				
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
window.title("Rocket Command")
window.geometry('950x700')

client = ThreadedClient(window)
window.mainloop(  )