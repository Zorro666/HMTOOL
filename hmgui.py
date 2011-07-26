#! /usr/bin/python

import Tkinter 
import hmclient

class HMGUI(Tkinter.Frame):
	def __init__(self, master = None):
		Tkinter.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()
		self.appTitle = "HM Tool"
		self.connections = []
		self.activeConnection = None

	def setTitle(self, title):
		fullTitle = self.appTitle + ":" + title
		self.master.title(fullTitle)

	def consolePrint(self, output):
		if self.activeConnection != None:
			self.TEXT_console.insert(Tkinter.END,"Server:")
			self.TEXT_console.insert(Tkinter.END,self.activeConnection.string)
			self.TEXT_console.insert(Tkinter.END," ")
		self.TEXT_console.insert(Tkinter.END,output)
		self.TEXT_console.insert(Tkinter.END,"\n")
		self.TEXT_console.see(Tkinter.END)

	def connectServer(self):
		serverName = self.ENTRY_serverIP.get()
		serverPort = self.ENTRY_serverPort.get()
		connection = hmclient.Connection()
		result = connection.connectToServer(serverName, serverPort)

		if result == False:
			self.consolePrint("ERROR failed to connect to server")
		else:
			self.connections.append(connection)
			self.currentConnection = connection
			self.BUTTON_connectServer["text"] = "Connected to:"+self.currentConnection.string
			self.BUTTON_connectServer["command"] = self.connectServer
			self.consolePrint("Connected to server")
			self.setTitle("Connected to "+self.currentConnection.string)

	def sendCommand(self):
		if self.currentConnection.valid == False:
			self.consolePrint("ERROR: server not connected")
			return

		command = self.ENTRY_command.get()
		if command == "":
			self.consolePrint("ERROR: NULL command")
			return

		xml_result = self.currentConnection.sendConsoleCommand(command)
		success = xml_result[0]
		result = xml_result[1]
		self.consolePrint("Sent Command:"+command)
		self.consolePrint("Command Result:"+str(success))
		self.consolePrint(result)

	def getClientIPs(self):
		xml_result = self.currentConnection.getClientIPs()
		success = xml_result[0]
		result = xml_result[1]
		self.consolePrint("GetClientIPs")
		self.consolePrint("Result:"+str(success))
		self.consolePrint(result)

	def returnKey(self, event):
		self.sendCommand()

	def createWidgets(self):
		curRow = 0
		curCol = 0
		self.LABEL_serverIP = Tkinter.Label(self, text = "Server IP")
		self.LABEL_serverIP.grid(row = curRow, column = curCol)
		curCol += 1
		self.ENTRY_serverIP = Tkinter.Entry(self)
		self.ENTRY_serverIP.insert(0, "localhost")
		self.ENTRY_serverIP.grid(row = curRow, column = curCol)
		curCol += 1

		self.LABEL_serverPort = Tkinter.Label(self, text = "Server Port")
		self.LABEL_serverPort.grid(row = curRow, column = curCol)
		curCol += 1
		self.ENTRY_serverPort = Tkinter.Entry(self)
		self.ENTRY_serverPort.insert(0, "31415")
		self.ENTRY_serverPort.grid(row = curRow, column = curCol)
		curCol += 1

		self.BUTTON_connectServer = Tkinter.Button(self, text = "Connect Server", command = self.connectServer)
		self.BUTTON_connectServer.grid(row = curRow, column = curCol)
		curCol += 1

		curRow += 1
		curCol = 0
		self.LABEL_command = Tkinter.Label(self, text = "Command")
		self.LABEL_command.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1
		self.ENTRY_command = Tkinter.Entry(self, width = 60)
		self.ENTRY_command.insert(0, "")
		self.ENTRY_command.grid(row = curRow, column = curCol, columnspan = 3)
		self.ENTRY_command.bind('<Return>', self.returnKey)
		curCol += 3
		self.BUTTON_quit = Tkinter.Button(self, text = "Send Command", command = self.sendCommand)
		self.BUTTON_quit.grid(row = curRow, column = curCol)
		curCol += 1

		curRow += 1
		curCol = 0
		self.TEXT_console = Tkinter.Text(self)
		self.TEXT_console.grid(row = curRow, columnspan = 10)
		curCol += 1

		curRow += 1
		curCol = 0
		self.BUTTON_quit = Tkinter.Button(self, text = "QUIT", fg = "red", command = self.quit)
		self.BUTTON_quit.grid(row = curRow, column = curCol)
		curCol += 1
		self.BUTTON_getIPs = Tkinter.Button(self, text = "Get Client IPs", command = self.getClientIPs)
		self.BUTTON_getIPs.grid(row = curRow, column = curCol)
		curCol += 1

		curRow += 1
		curCol = 0

root = Tkinter.Tk()
app = HMGUI(master = root)
app.setTitle("Disconnected")
app.mainloop()
root.destroy()
