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
		self.currentConnection = None
		self.master.bind('<Escape>', self.userQuit)

	def setTitle(self, title):
		fullTitle = self.appTitle + ":" + title
		self.master.title(fullTitle)

	def consolePrint(self, output, noprefix=False):
		self.TEXT_console.config(state = Tkinter.NORMAL)
		if self.currentConnection != None:
			if noprefix == False:
				self.TEXT_console.insert(Tkinter.END,"HTTP Server:")
				self.TEXT_console.insert(Tkinter.END,self.currentConnection.string)
				self.TEXT_console.insert(Tkinter.END," ")
		self.TEXT_console.insert(Tkinter.END,output)
		self.TEXT_console.insert(Tkinter.END,"\n")
		self.TEXT_console.see(Tkinter.END)
		self.TEXT_console.config(state = Tkinter.DISABLED)

	def setServerEntry(self, serverName):
		self.TEXT_serverName.config(state = Tkinter.NORMAL)
		self.TEXT_serverName.delete(1.0, Tkinter.END)
		self.TEXT_serverName.insert(Tkinter.END, serverName)
		self.TEXT_serverName.config(state = Tkinter.DISABLED)

	def clearClients(self):
		self.TEXT_clientNames.config(state = Tkinter.NORMAL)
		self.TEXT_clientNames.delete(1.0, Tkinter.END)
		self.TEXT_clientNames.config(state = Tkinter.DISABLED)
		self.TEXT_clientIPs.config(state = Tkinter.NORMAL)
		self.TEXT_clientIPs.delete(1.0, Tkinter.END)
		self.TEXT_clientIPs.config(state = Tkinter.DISABLED)

	def addClientEntry(self, clientDetail):
		self.TEXT_clientNames.config(state = Tkinter.NORMAL)
		self.TEXT_clientNames.insert(Tkinter.END, clientDetail[0])
		self.TEXT_clientNames.insert(Tkinter.END, "\n")
		self.TEXT_clientNames.config(state = Tkinter.DISABLED)
		self.TEXT_clientIPs.config(state = Tkinter.NORMAL)
		self.TEXT_clientIPs.insert(Tkinter.END, clientDetail[1])
		self.TEXT_clientIPs.insert(Tkinter.END, "\n")
		self.TEXT_clientIPs.config(state = Tkinter.DISABLED)

	def connectHTTPServer(self):
		HTTPServerName = self.ENTRY_HTTPServerIP.get()
		HTTPServerPort = self.ENTRY_HTTPServerPort.get()
		connection = hmclient.Connection()
		result = connection.connectToHTTPServer(HTTPServerName, HTTPServerPort)

		if result == False:
			self.consolePrint("ERROR failed to connect to HTTP server")
		else:
			self.connections.append(connection)
			self.currentConnection = connection
			self.BUTTON_connectHTTPServer["text"] = "Connected to:" + self.currentConnection.string
			self.BUTTON_connectHTTPServer["command"] = self.connectHTTPServer
			self.consolePrint("START #####################################################", noprefix = True)
			self.consolePrint("Connected to HTTPServer")
			self.setTitle("Connected to " + self.currentConnection.string)
			self.consolePrint("END #####################################################", noprefix = True)
			if self.currentConnection.isServer():
				self.setServerEntry(HTTPServerName)
			if self.currentConnection.isClient():
				self.addClientEntry(HTTPServerName)

	def sendCommand(self):
		command = self.ENTRY_command.get()
		if self.testConnection(command) == False:
			return

		if self.currentConnection.valid == False:
			self.consolePrint("ERROR: HTTP server not connected")
			return

		if command == "":
			self.consolePrint("ERROR: NULL command")
			return

		xml_result = self.currentConnection.sendConsoleCommand(command)
		success = xml_result[0]
		result = xml_result[1]
		self.consolePrint("START #####################################################", noprefix=True)
		self.consolePrint("Sent Command:"+command)
		self.consolePrint("Command Result:"+str(success))
		self.consolePrint(result)
		self.consolePrint("END #####################################################", noprefix=True)

	def getClientDetails(self):
		if self.testConnection("GetClientDetails") == False:
			return
		xml_result = self.currentConnection.getClientDetailsList(forceUpdate=True)
		success = xml_result[0]
		result = xml_result[1]
		self.consolePrint("START #####################################################", noprefix=True)
		self.consolePrint("GetClientDetails")
		self.consolePrint("Result:"+str(success))
		self.consolePrint(result)
		for cd in result:
			self.consolePrint("Name:"+cd[0]+" IP:"+cd[1]+" NetID:"+cd[2]+" Port:"+cd[3])
		self.consolePrint("END #####################################################", noprefix=True)
		self.clearClients()
		for cd in result:
			self.addClientEntry(cd)

	def getClientIPs(self):
		if self.testConnection("GetClientIPs") == False:
			return

		xml_result = self.currentConnection.getClientIPs()
		success = xml_result[0]
		result = xml_result[1]
		self.consolePrint("START #####################################################", noprefix=True)
		self.consolePrint("GetClientIPs")
		self.consolePrint("Result:"+str(success))
		self.consolePrint(result)
		self.consolePrint("END #####################################################", noprefix=True)
		self.clearClients()
		for ci in result:
			clientName = ci[0]
			self.addClientEntry([clientName, "", "", ""])

	def testConnection(self, info):
		valid = True
		if self.currentConnection == None:
			valid = False
		else:
			if self.currentConnection.valid == False:
				valid = False

		if valid == False:
			self.consolePrint("START #####################################################", noprefix=True)
			self.consolePrint(info)
			self.consolePrint("ERROR: HTTP server not connected")
			self.consolePrint("END #####################################################", noprefix=True)
			return False

		return True


	def getGameState(self):
		if self.testConnection("GetGameState") == False:
			return

		xml_result = self.currentConnection.getGameState()
		success = xml_result[0]
		result = xml_result[1]
		self.consolePrint("START #####################################################", noprefix=True)
		self.consolePrint("GetGameState")
		self.consolePrint("Result:"+str(success))
		self.consolePrint(result)
		self.consolePrint("END #####################################################", noprefix=True)

	def getClientList(self):
		if self.testConnection("GetClientList") == False:
			return

		xml_result = self.currentConnection.getClientList()
		success = xml_result[0]
		result = xml_result[1]
		self.consolePrint("START #####################################################", noprefix=True)
		self.consolePrint("GetClientList")
		self.consolePrint("Result:"+str(success))
		self.consolePrint(result)
		for ci in result:
			self.consolePrint("Name:"+ci[0]+" NetID:"+ci[1])
		self.consolePrint("END #####################################################", noprefix=True)

		self.clearClients()
		for ci in result:
			clientName = ci[0]
			self.addClientEntry([clientName,"", "", ""])

	def returnKey(self, event):
		self.sendCommand()

	def userQuit(self, event):
		self.quit()

	def createWidgets(self):
		serverClientBoxWidth = 15
		serverClientIPBoxWidth = 16
		disableBGcolour = "#CCCCCC"
		disableFGcolour = "#000000"

		curRow = 0
		curCol = 0
		self.LABEL_serverName = Tkinter.Label(self, text = "Server Name")
		self.LABEL_serverName.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1
		self.LABEL_clientIP = Tkinter.Label(self, text = "Server IP")
		self.LABEL_clientIP.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1

		curCol += 2
		self.LABEL_HTTPServerIP = Tkinter.Label(self, text = "HTTP Server IP")
		self.LABEL_HTTPServerIP.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1
		self.ENTRY_HTTPServerIP = Tkinter.Entry(self)
		self.ENTRY_HTTPServerIP.insert(0, "localhost")
		self.ENTRY_HTTPServerIP.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1

		self.LABEL_HTTPServerPort = Tkinter.Label(self, text = "HTTP Server Port")
		self.LABEL_HTTPServerPort.grid(row = curRow, column = curCol)
		curCol += 1
		self.ENTRY_HTTPServerPort = Tkinter.Entry(self, width = 5)
		self.ENTRY_HTTPServerPort.insert(0, "31415")
		self.ENTRY_HTTPServerPort.grid(row = curRow, column = curCol)
		curCol += 1

		self.BUTTON_connectHTTPServer = Tkinter.Button(self, text = "Connect HTTP Server", command = self.connectHTTPServer)
		self.BUTTON_connectHTTPServer.grid(row = curRow, column = curCol)
		curCol += 1

		curRow += 1
		curCol = 0
		self.TEXT_serverName = Tkinter.Text(self, state = Tkinter.DISABLED, width = serverClientBoxWidth, height = 1, bg = disableBGcolour, fg = disableFGcolour)
		self.TEXT_serverName.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1
		self.TEXT_serverIP = Tkinter.Text(self, state = Tkinter.DISABLED, width = serverClientIPBoxWidth, height = 1, bg = disableBGcolour)
		self.TEXT_serverIP.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 3
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
		textSavedRow = curRow
		curCol = 0
		self.LABEL_clientNames = Tkinter.Label(self, text = "Client Details")
		self.LABEL_clientNames.grid(row = curRow, column = curCol, columnspan = 4)
		curRow += 1
		curCol = 0
		self.LABEL_clientName = Tkinter.Label(self, text = "Name")
		self.LABEL_clientName.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1
		self.LABEL_clientIP = Tkinter.Label(self, text = "IP")
		self.LABEL_clientIP.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1
		self.LABEL_clientNetID = Tkinter.Label(self, text = "NetID")
		self.LABEL_clientNetID.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1
		self.LABEL_clientPort = Tkinter.Label(self, text = "Port")
		self.LABEL_clientPort.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1

		curRow += 1
		curCol = 0
		self.TEXT_clientNames = Tkinter.Text(self, state = Tkinter.DISABLED, width = serverClientBoxWidth, height = 16, bg = disableBGcolour)
		self.TEXT_clientNames.grid(row = curRow, column = curCol, rowspan=16)
		curCol += 1
		self.TEXT_clientIPs = Tkinter.Text(self, state = Tkinter.DISABLED, width = serverClientIPBoxWidth, height = 16, bg = disableBGcolour)
		self.TEXT_clientIPs.grid(row = curRow, column = curCol, rowspan=16)
		curCol += 1
		self.TEXT_clientNetIDs = Tkinter.Text(self, state = Tkinter.DISABLED, width = 5, height = 16, bg = disableBGcolour)
		self.TEXT_clientNetIDs.grid(row = curRow, column = curCol, rowspan=16)
		curCol += 1
		self.TEXT_clientPorts = Tkinter.Text(self, state = Tkinter.DISABLED, width = 5, height = 16, bg = disableBGcolour)
		self.TEXT_clientPorts.grid(row = curRow, column = curCol, rowspan=16)
		curCol += 1

		curRow = textSavedRow
		curCol = 4
		self.TEXT_console = Tkinter.Text(self, state = Tkinter.DISABLED, width = 100, height = 18, bg = disableBGcolour)
		self.TEXT_console.grid(row = curRow, column = curCol, rowspan = 20, columnspan = 7)
		curCol += 7

		curRow += 20
		curCol = 0
		self.BUTTON_quit = Tkinter.Button(self, text = "QUIT", fg = "red", command = self.quit)
		self.BUTTON_quit.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 4
		self.BUTTON_getIPs = Tkinter.Button(self, text = "Get Client Details", command = self.getClientDetails)
		self.BUTTON_getIPs.grid(row = curRow, column = curCol)
		curCol += 1
		self.BUTTON_getIPs = Tkinter.Button(self, text = "Get Client IPs", command = self.getClientIPs)
		self.BUTTON_getIPs.grid(row = curRow, column = curCol)
		curCol += 1
		self.BUTTON_getGameState = Tkinter.Button(self, text = "Get Game State", command = self.getGameState)
		self.BUTTON_getGameState.grid(row = curRow, column = curCol)
		curCol += 1
		self.BUTTON_getClientList = Tkinter.Button(self, text = "Get Client List", command = self.getClientList)
		self.BUTTON_getClientList.grid(row = curRow, column = curCol)
		curCol += 1

		curRow += 1
		curCol = 0

root = Tkinter.Tk()
app = HMGUI(master = root)
app.setTitle("Disconnected")
app.mainloop()
root.destroy()
