#! /usr/bin/python

import Tkinter 
import hmclient

class HMGUI(Tkinter.Frame):
	def consolePrint(self, output):
		self.TEXT_console.insert(Tkinter.END,output)
		self.TEXT_console.insert(Tkinter.END,"\n")

	def connectServer(self):
		serverName=self.ENTRY_serverIP.get()
		serverPort=self.ENTRY_serverPort.get()
		serverStr=serverName+":"+serverPort
		result = hmclient.connectToServer(serverName, serverPort)
		self.serverOK = result[0]
		if (self.serverOK == False):
			self.consolePrint("Failed to connect to server:"+serverStr)
		else:
			self.serverConnection = result[1]
			self.serverName=serverName
			self.serverPort=serverPort
			self.BUTTON_connectServer["text"] = "Connected to:"+serverStr
			self.BUTTON_connectServer["command"] = self.connectServer
			self.consolePrint("Connected to server:"+serverStr)

	def createWidgets(self):
		self.LABEL_serverIP = Tkinter.Label(self)
		self.LABEL_serverIP["text"] = "Server IP"
		self.LABEL_serverIP.grid(row=0,column=0)
		self.ENTRY_serverIP = Tkinter.Entry(self)
		self.ENTRY_serverIP.insert(0, "localhost")
		self.ENTRY_serverIP.grid(row=0,column=1)

		self.LABEL_serverPort= Tkinter.Label(self)
		self.LABEL_serverPort["text"] = "Server Port"
		self.LABEL_serverPort.grid(row=0,column=2)
		self.ENTRY_serverPort= Tkinter.Entry(self)
		self.ENTRY_serverPort.insert(0, "31415")
		self.ENTRY_serverPort.grid(row=0,column=3)

		self.BUTTON_connectServer = Tkinter.Button(self)
		self.BUTTON_connectServer["text"] = "Connect Server"
		self.BUTTON_connectServer["command"] = self.connectServer
		self.BUTTON_connectServer.grid(row=0,column=4)

		self.TEXT_console = Tkinter.Text(self)
#		self.TEXT_console["text"] = "console output"
		self.TEXT_console.grid(row=1,columnspan=5)

		self.BUTTON_quit = Tkinter.Button(self)
		self.BUTTON_quit["text"] = "QUIT"
		self.BUTTON_quit["fg"]   = "red"
		self.BUTTON_quit["command"] =  self.quit
		self.BUTTON_quit.grid(row=2, column=0)

	def __init__(self, master=None):
		Tkinter.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()
		self.serverOK=False

root = Tkinter.Tk()
app = HMGUI(master=root)
app.master.title("HM Tool")
#app.master.maxsize(400, 300)
app.mainloop()
root.destroy()
