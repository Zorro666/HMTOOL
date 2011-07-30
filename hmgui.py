#! /usr/bin/python

import Tkinter 
import hmclient
from hmparse import HMParse

class HMGUI(Tkinter.Frame):
	def __init__(self, master = None):
		Tkinter.Frame.__init__(self, master)
		self.TEXT_clientNames = []
		self.TEXT_clientIPs = []
		self.TEXT_clientNetIDs = []
		self.TEXT_clientNetPorts = []
		self.grid()
		self.createWidgets()
		self.appTitle = "HM Tool"
		self.clientConnections = []
		self.serverConnection = None
		self.currentConnection = None
		self.master.bind('<Escape>', self.userQuit)
		self.serverInfo = ["", "", "", ""]
		self.clientDetails = []
		self.selectedClient = None

	def setTitle(self, title):
		fullTitle = self.appTitle + ":" + title
		fullTitle += " ServerIP:"+self.serverInfo[1]
		fullTitle += " ServerPort:"+self.serverInfo[3]
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

	def setServerIP(self, serverIP):
		self.TEXT_serverIP.config(state = Tkinter.NORMAL)
		self.TEXT_serverIP.delete(1.0, Tkinter.END)
		self.TEXT_serverIP.insert(Tkinter.END, serverIP)
		self.TEXT_serverIP.config(state = Tkinter.DISABLED)

	def setServerPort(self, serverPort):
		self.TEXT_serverPort.config(state = Tkinter.NORMAL)
		self.TEXT_serverPort.delete(1.0, Tkinter.END)
		self.TEXT_serverPort.insert(Tkinter.END, serverPort)
		self.TEXT_serverPort.config(state = Tkinter.DISABLED)

	def setServerSelected(self, selected):
		if selected:
			fgColour = "red"
		else:
			if self.serverConnection == None:
				fgColour = "black"
			else:
				fgColour = "blue"

		self.TEXT_serverIP.config(fg = fgColour)
		self.TEXT_serverPort.config(fg = fgColour)
		if selected == True:
			self.setClientSelected(None)
			self.updateClientsDisplay()
			self.currentConnection = self.serverConnection

	def clearClients(self):
		for w in self.TEXT_clientNames:
			w.config(state = Tkinter.NORMAL)
			w.delete(1.0, Tkinter.END)
			w.config(state = Tkinter.DISABLED)
		for w in self.TEXT_clientIPs:
			w.config(state = Tkinter.NORMAL)
			w.delete(1.0, Tkinter.END)
			w.config(state = Tkinter.DISABLED)
		for w in self.TEXT_clientNetIDs:
			w.config(state = Tkinter.NORMAL)
			w.delete(1.0, Tkinter.END)
			w.config(state = Tkinter.DISABLED)
		for w in self.TEXT_clientPorts:
			w.config(state = Tkinter.NORMAL)
			w.delete(1.0, Tkinter.END)
			w.config(state = Tkinter.DISABLED)

	def addClientEntry(self, clientDetail, selected, connected):
		if selected:
			fgColour = "red"
		else:
			if connected:
				fgColour = "blue"
			else:
				fgColour = "black"

		index = 0
		for w in self.TEXT_clientNames:
			clientName = w.get(1.0, Tkinter.END)
			clientName = clientName.strip()
			if len(clientName) == 0:
				break
			index += 1

		if index >= len(self.TEXT_clientNames):
			print "No space in client names"
			return

		self.TEXT_clientNames[index].config(state = Tkinter.NORMAL, fg = fgColour)
		self.TEXT_clientNames[index].insert(Tkinter.END, clientDetail[0])
		self.TEXT_clientNames[index].config(state = Tkinter.DISABLED)
		self.TEXT_clientIPs[index].config(state = Tkinter.NORMAL, fg = fgColour)
		self.TEXT_clientIPs[index].insert(Tkinter.END, clientDetail[1])
		self.TEXT_clientIPs[index].config(state = Tkinter.DISABLED)
		self.TEXT_clientNetIDs[index].config(state = Tkinter.NORMAL, fg = fgColour)
		self.TEXT_clientNetIDs[index].insert(Tkinter.END, clientDetail[2])
		self.TEXT_clientNetIDs[index].config(state = Tkinter.DISABLED)
		self.TEXT_clientPorts[index].config(state = Tkinter.NORMAL, fg = fgColour)
		self.TEXT_clientPorts[index].insert(Tkinter.END, clientDetail[3])
		self.TEXT_clientPorts[index].config(state = Tkinter.DISABLED)

	def setClientSelected(self, clientDetail):
		self.selectedClient = clientDetail
		if clientDetail != None:
			self.setServerSelected(False)

	def serverConnect(self):
		self.connectHTTPServer()
		self.getClientDetails()

	def connectHTTPServer(self):
		HTTPServerName = self.ENTRY_HTTPServerIP.get()
		HTTPServerPort = self.ENTRY_HTTPServerPort.get()
		self.connectToHTTPServer(HTTPServerName, HTTPServerPort)

	def closeClientConnections(self):
		for con in self.clientConnections:
			con.close()

		del self.clientConnections
		self.clientConnections = []
		del self.clientDetails
		self.clientDetails = []

	def connectToHTTPServer(self, IP, port):
		cd = ["", IP, "", port]
		if self.isConnected(cd):
			print "Already connected"
			return

		connection = hmclient.Connection()
		result = connection.connectToHTTPServer(IP, port)
		self.currentConnection = None

		if result == False:
			self.consolePrint("ERROR failed to connect to HTTP server")
			self.consolePrint("ERROR IP:"+IP+" port:"+port)
		else:
			self.currentConnection = connection
			self.BUTTON_connectHTTPServer["text"] = "Connected to:" + self.currentConnection.string
			self.consolePrint("START #####################################################", noprefix = True)
			self.consolePrint("Connected to HTTPServer")

			if self.currentConnection.isServer():
				self.closeClientConnections()
				self.clearClients()
				result = self.currentConnection.getServerIP()
				if result[0] == True:
					print "ServerIP:"+result[1]
					self.setServerIP(result[1])
					self.setServerPort(port)
					self.consolePrint("ServerIP:"+result[1])
				self.serverConnection = self.currentConnection
				self.serverInfo = [IP, result[1], "", port]
				self.setServerSelected(True)
				self.consolePrint("is a server")
				self.setTitle("Connected to a server " + self.currentConnection.string)

			result = self.currentConnection.isClient()
			if result[0]:
				self.clientConnections.append(connection)
				clientName = result[1]
				clientIP = IP
				serverBasePort = int(self.serverInfo[3])
				clientNetID = str(int(port) - serverBasePort)
				clientPort = port
				self.consolePrint("A client: Name:" + clientName +" IP:" + clientIP + " NetID:" + clientNetID + " Port:" + clientPort)
				self.currentConnection.setDetail(clientName, clientIP, clientNetID, clientPort)
				self.setTitle("Connected to a client " + self.currentConnection.string)

				selectedClient = None
				for cd in self.clientDetails:
					# Match on NetID only!
					if cd[2] == clientNetID:
						cd[3] = port
						selectedClient = cd
						break;
				self.consolePrint(str(selectedClient))
				self.setClientSelected(selectedClient)
				self.updateClientsDisplay()

			self.consolePrint("END #####################################################", noprefix = True)

	def sendCommand(self):
		commandParams = self.ENTRY_command.get()
		commandParamsList = commandParams.split()
		command = commandParamsList.pop(0)
		params = " ".join(commandParamsList)
		self.consolePrint("#### sendCommand " + command + " " + params + " #####", noprefix = True)
		self.sendCommandInternal(command, params)

	def broadcastCommand(self):
		commandParams = self.ENTRY_command.get()
		commandParamsList = commandParams.split()
		command = commandParamsList.pop(0)
		params = " ".join(commandParamsList)
		self.consolePrint("#### broadcastCommand " + command + " " + params + " #####", noprefix = True)

		oldCurrent = self.currentConnection

		self.currentConnection = self.serverConnection
		self.sendCommandInternal(command, params)
		for con in self.clientConnections:
			self.currentConnection = con
			self.sendCommandInternal(command, params)

		self.currentConnection = oldCurrent

	def sendCommandInternal(self, command, params):
		if self.testConnection(command) == False:
			return

		if self.currentConnection.valid == False:
			self.consolePrint("ERROR: HTTP server not connected")
			return

		if command == "":
			self.consolePrint("ERROR: NULL command")
			return

		rpc_result = self.currentConnection.sendConsoleCommand(command, params)
		success = rpc_result[0]
		result = rpc_result[1]
		self.consolePrint("START #####################################################", noprefix=True)
		self.consolePrint("Sent Command:"+command)
		self.consolePrint("Params:"+params)
		self.consolePrint("Command Result:"+str(success))
		self.consolePrint(result)
		self.consolePrint("END #####################################################", noprefix=True)

	def getClientDetails(self):
		if self.testConnection("GetClientDetails") == False:
			return
		rpc_result = self.serverConnection.getClientDetailsList(forceUpdate=True)
		success = rpc_result[0]
		result = rpc_result[1]
		self.consolePrint("START #####################################################", noprefix=True)
		self.consolePrint("GetClientDetails")
		self.consolePrint("Result:"+str(success))
		self.consolePrint(result)
		for cd in result:
			clientPort = str(0)
			if len(cd[2]) > 0:
				clientPort = str(int(self.serverInfo[3]) + int(cd[2]))
			cd[3] = clientPort
			self.consolePrint("Name:"+cd[0]+" IP:"+cd[1]+" NetID:"+cd[2]+" Port:"+cd[3])
		self.consolePrint("END #####################################################", noprefix=True)
		self.clientDetails = result
		self.updateClientsDisplay()

	def updateClientsDisplay(self):
		self.clearClients()
		for cd in self.clientDetails:
			selected = False
			if self.selectedClient != None:
#				print "Selected or not"
#				print "cd[0]:", cd[0], " self.selectedClient[0]:", self.selectedClient[0]
#				print "cd[1]:", cd[1], " self.selectedClient[1]:", self.selectedClient[1]
#				print "cd[2]:", cd[2], " self.selectedClient[2]:", self.selectedClient[2]
#				print "cd[3]:", cd[3], " self.selectedClient[3]:", self.selectedClient[3]
				# Match on name & IP & net ID & port number
				if cd[0] == self.selectedClient[0] and cd[1] == self.selectedClient[1] and cd[2] == self.selectedClient[2] and cd[3] == self.selectedClient[3]:
					selected = True

			connected = self.isClientConnected(cd)
			self.addClientEntry(cd, selected, connected)

	def isConnected(self, cd):
		conDetail = self.serverInfo
		if conDetail == None:
			return False

		print "conDetail:", conDetail
		print "cd:", cd
		if conDetail[1] == cd[1] and conDetail[3] == cd[3]:
				return True
		for con in self.clientConnections:
			# Match on IP & port number 
			if con != None:
				conDetail = con.getDetail()
				if conDetail[1] == cd[1] and conDetail[3] == cd[3]:
					return True

		return False

	def isServerConnected(self, cd):
		conDetail = self.serverInfo
		if conDetail == None:
			return False

		print "conDetail:", conDetail
		print "cd:", cd
		if conDetail[1] == cd[1] and conDetail[3] == cd[3]:
				return True

		return False

	def isClientConnected(self, cd):
		connected = False
		for con in self.clientConnections:
			# Match on name & IP & net ID & port number 
			if con != None:
				conDetail = con.getDetail()
#				print "Connected or not"
#				print "cd[0]:", cd[0], " conDetail[0]:", conDetail[0]
#				print "cd[1]:", cd[1], " conDetail[1]:", conDetail[1]
#				print "cd[2]:", cd[2], " conDetail[2]:", conDetail[2]
#				print "cd[3]:", cd[3], " conDetail[3]:", conDetail[3]
				if conDetail[0] == cd[0] and conDetail[1] == cd[1] and conDetail[2] == cd[2] and conDetail[3] == cd[3]:
						connected = True
						break
		return connected

	def getClientIPs(self):
		if self.testServerConnection("GetClientIPs") == False:
			return

		rpc_result = self.serverConnection.getClientIPs()
		success = rpc_result[0]
		result = rpc_result[1]
		self.consolePrint("START #####################################################", noprefix=True)
		self.consolePrint("GetClientIPs")
		self.consolePrint("Result:"+str(success))
		self.consolePrint(result)
		self.consolePrint("END #####################################################", noprefix=True)

		self.clientDetails = []
		for ci in result:
			clientName = ci[0]
			clientIP = ci[1]
			clientNetID = ""
			clientPort = ""
			self.clientDetails.append([clientName, clientIP, clientNetID, clientPort])

		self.updateClientsDisplay()

	def testServerConnection(self, info):
		valid = True
		if self.serverConnection == None:
			valid = False
		else:
			if self.serverConnection.valid == False:
				valid = False

		if valid == False:
			self.consolePrint("START #####################################################", noprefix=True)
			self.consolePrint(info)
			self.consolePrint("ERROR: HTTP server not connected")
			self.consolePrint("END #####################################################", noprefix=True)
			return False

		return True

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

	def checkServerConnection(self):
		oldConnection = self.currentConnection
		self.currentConnection = self.serverConnection
		connected = True
		if self.testConnection("checkServerConnections") == False:
			print "currentConnection: testConnection is false"
			connected = False
		elif self.serverConnection.testConnection() == False:
				print "serverConnection: testConnection is false"
				connected = False

		if connected == False:
			if oldConnection == self.serverConnection:
				if oldConnection != None:
					oldConnection.close()
					oldConnection = None

			if self.serverConnection != None:
				self.serverConnection.close()
				self.serverConnection = None
				self.serverInfo = None

		self.currentConnection = oldConnection
		return True

	def checkOneClientConnection(self, IP, port):
		for con in self.clientConnections:
			if con != None:
				conIP = con.getIP()
				conPort = con.getPort()
				if conIP == IP and conPort == port:
					print "checkOneClient found it"
					if con.testConnection() == True:
						print "checkOneClient found it: connected"
						return True

		print "checkOneClient False"
		return False;

	def checkConnections(self):
		print "checkConnections"
		selected = False
		print "curIP", self.currentConnection.getIP()
		print "curPort", self.currentConnection.getPort()
		print "serverConIP", self.serverConnection.getIP()
		print "serverCoPnort", self.serverConnection.getPort()
		if self.currentConnection == self.serverConnection:
			print "Server is selected"
			selected = True

		connected = self.checkServerConnection()
		if connected == False:
			selected = False

		self.setServerSelected(selected)

		for i in range(16):
			clientName = str(self.TEXT_clientNames[i].get(1.0, Tkinter.END).strip())
			clientIP = str(self.TEXT_clientIPs[i].get(1.0, Tkinter.END).strip())
			clientNetID = str(self.TEXT_clientNetIDs[i].get(1.0, Tkinter.END).strip())
			clientPort = str(self.TEXT_clientPorts[i].get(1.0, Tkinter.END).strip())
			cd = [clientName, clientIP, clientNetID, clientPort]

			if len(clientName) == 0:
				continue
			if len(clientIP) == 0:
				continue
			if len(clientNetID) == 0:
				continue
			if len(clientPort) == 0:
				continue

			print "checkConnections:[", i, "]", cd
			if self.isClientConnected(cd) == False:
				print "checkConnections client not connected"
			if self.checkOneClientConnection(clientIP, clientPort) == False:
				print "checkConnections client test connection is false"
				for con in self.clientConnections:
					if con != None:
						conIP = con.getIP()
						conPort = con.getPort()
						if conIP == clientIP and conPort == clientPort:
							con.close()
							self.clientConnections.remove(con)
						if self.currentConnection.getIP() == clientIP and self.currentConnection.getPort == clientPort:
							print "Closing current connection"
							self.currentConnection.close()
							self.currentConnection = None
						if self.selectedClient != None:
							if self.selectedClient[1] == clientIP and self.selectedClient[3] == clientPort:
								print "Selected client not connected: resetting"
								self.setClientSelected(None)
			self.updateClientsDisplay()


	def getGameState(self):
		if self.testConnection("GetGameState") == False:
			return None

		if self.currentConnection == self.serverConnection:
			prefix = "Server"
		else:
			# Get the right client name
			prefix = "Client"
			conIP = self.currentConnection.getIP()
			conPort = self.currentConnection.getPort()
			for i in range(16):
				clientName = str(self.TEXT_clientNames[i].get(1.0, Tkinter.END).strip())
				clientIP = str(self.TEXT_clientIPs[i].get(1.0, Tkinter.END).strip())
				clientNetID = str(self.TEXT_clientNetIDs[i].get(1.0, Tkinter.END).strip())
				clientPort = str(self.TEXT_clientPorts[i].get(1.0, Tkinter.END).strip())

				if len(clientName) == 0:
					continue
				if len(clientIP) == 0:
					continue
				if len(clientPort) == 0:
					continue

				if conIP == clientIP and conPort == clientPort:
					prefix = clientName

		rpc_result = self.currentConnection.getGameState(saveToFile=True, filePrefix=prefix)
		success = rpc_result[0]
		result = rpc_result[1]
		self.consolePrint("START #####################################################", noprefix=True)
		self.consolePrint("GetGameState")
		self.consolePrint("Result:"+str(success))
		self.consolePrint(result)
		self.consolePrint("END #####################################################", noprefix=True)

		return result

	def getClientList(self):
		if self.testServerConnection("GetClientList") == False:
			return

		rpc_result = self.serverConnection.getClientList()
		success = rpc_result[0]
		result = rpc_result[1]
		self.consolePrint("START #####################################################", noprefix=True)
		self.consolePrint("GetClientList")
		self.consolePrint("Result:"+str(success))
		self.consolePrint(result)
		for ci in result:
			self.consolePrint("Name:"+ci[0]+" NetID:"+ci[1])
		self.consolePrint("END #####################################################", noprefix=True)

		self.clientDetails = []
		for ci in result:
			clientName = ci[0]
			clientIP = ""
			clientNetID = ""
			clientPort = ""
			self.clientDetails.append([clientName, clientIP, clientNetID, clientPort])

		self.updateClientsDisplay()

	def compareGameStates(self):
		self.consolePrint("START ################## compareGameStates ###################################", noprefix = True)
		self.connectHTTPServer()
		self.getClientDetails()

		# Spawn client HTTP servers
		oldConnection = self.currentConnection
		self.currentConnection = self.serverConnection
		self.sendCommandInternal("jake", "129 140 150")
		self.currentConnection = oldConnection

		# Try to connect to them
		for i in range(16):
			self.clientClick(None, i)

		# Output and compare game state for all the connections
		oldConnection = self.currentConnection
		self.currentConnection = self.serverConnection
		hmparse = HMParse()

		gameStateXMLstring = self.getGameState()
		hmparse.setServerXML(gameStateXMLstring)
		hmparse.clearClientXMLs()

		for con in self.clientConnections:
			if con != None:
				if con.valid == True:
					self.currentConnection = con
					gameStateXMLstring = self.getGameState()
					nickname = con.getDetail()[0]
					if len(nickname) > 0:
						hmparse.addClientXML(nickname, gameStateXMLstring)
		self.currentConnection = oldConnection

		res = hmparse.compareServerToAllClients()
		for nickname in res[1]:
			compareResult = hmparse.compareServerToClientByNickname(nickname)
			if compareResult[0] == False:
				self.consolePrint("###### Compare Server to " + nickname + " ######")
				self.consolePrint(str(compareResult[1]))

		if res[0] == False:
			self.consolePrint(str("Server different to clients:") + str(res[1]))
		else:
			self.consolePrint("Server identical to clients")
		self.consolePrint("END ################## compareGameStates ###################################", noprefix = True)

	def returnKey(self, event):
		self.sendCommand()

	def userQuit(self, event):
		self.quit()

	def serverClick(self, event):
		serverIP = str(self.TEXT_serverIP.get(1.0, Tkinter.END).strip())
		serverPort = str(self.TEXT_serverPort.get(1.0, Tkinter.END).strip())
		cd = ["", serverIP, "", serverPort]
		print "serverClick:", cd

		if len(serverIP) == 0:
			return
		if len(serverPort) == 0:
			return

		if self.isServerConnected(cd) == False:
			print "serverClick not connected : reconnecting"
			self.connectToHTTPServer(serverIP, serverPort)
		else:
			self.setServerSelected(True)

		if self.checkServerConnection() == False:
			self.setServerSelected(False)

	def clientClick(self, event, i):
		clientName = str(self.TEXT_clientNames[i].get(1.0, Tkinter.END).strip())
		clientIP = str(self.TEXT_clientIPs[i].get(1.0, Tkinter.END).strip())
		clientNetID = str(self.TEXT_clientNetIDs[i].get(1.0, Tkinter.END).strip())
		clientPort = str(self.TEXT_clientPorts[i].get(1.0, Tkinter.END).strip())
		cd = [clientName, clientIP, clientNetID, clientPort]
		print "clientClick[", i, "]", cd

		if len(clientName) == 0:
			return
		if len(clientIP) == 0:
			return
		if len(clientNetID) == 0:
			return
		if len(clientPort) == 0:
			return

		if self.isClientConnected(cd) == False:
			print "clientClick not connected"
			self.connectToHTTPServer(clientIP, clientPort)
		else:
			self.setClientSelected(cd)
			self.updateClientsDisplay()
			for con in self.clientConnections:
				conIP = con.getIP()
				conPort = con.getPort()
				if conIP == clientIP and conPort == clientPort:
					self.currentConnection = con;

	def clientNameClick(self, event):
		w = event.widget
		i = self.TEXT_clientNames.index(w)
		self.clientClick(event, i)

	def clientIPClick(self, event):
		w = event.widget
		i = self.TEXT_clientIPs.index(w)
		self.clientClick(event, i)

	def clientNetIDClick(self, event):
		w = event.widget
		i = self.TEXT_clientNetIDs.index(w)
		self.clientClick(event, i)

	def clientPortClick(self, event):
		w = event.widget
		i = self.TEXT_clientPorts.index(w)
		self.clientClick(event, i)

	def createWidgets(self):
		serverClientBoxWidth = 15
		serverClientIPBoxWidth = 16
		disableBGcolour = "#CCCCCC"
		disableFGcolour = "#000000"

		curRow = 0
		curCol = 0
		self.LABEL_serverIP = Tkinter.Label(self, text = "Server IP")
		self.LABEL_serverIP.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1
		self.LABEL_serverPort = Tkinter.Label(self, text = "Server Port")
		self.LABEL_serverPort.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1
		self.BUTTON_getIPs = Tkinter.Button(self, text = "Server Connect", command = self.serverConnect)
		self.BUTTON_getIPs.grid(row = curRow, column = curCol, columnspan = 2)
		curCol += 1
		curCol += 1
		self.LABEL_HTTPServerIP = Tkinter.Label(self, text = "HTTP Server IP")
		self.LABEL_HTTPServerIP.grid(row = curRow, column = curCol, columnspan = 1, sticky="e")
		curCol += 1
		self.ENTRY_HTTPServerIP = Tkinter.Entry(self)
		self.ENTRY_HTTPServerIP.insert(0, "localhost")
		self.ENTRY_HTTPServerIP.grid(row = curRow, column = curCol, columnspan = 1, sticky="w")
		curCol += 1

		self.LABEL_HTTPServerPort = Tkinter.Label(self, text = "HTTP Server Port")
		self.LABEL_HTTPServerPort.grid(row = curRow, column = curCol, sticky="e")
		curCol += 1
		self.ENTRY_HTTPServerPort = Tkinter.Entry(self, width = 7)
		self.ENTRY_HTTPServerPort.insert(0, "31415")
		self.ENTRY_HTTPServerPort.grid(row = curRow, column = curCol, sticky="w")
		curCol += 1

		self.BUTTON_connectHTTPServer = Tkinter.Button(self, text = "Connect HTTP Server", command = self.connectHTTPServer)
		self.BUTTON_connectHTTPServer.grid(row = curRow, column = curCol, columnspan=2, sticky="w")
		curCol += 2

		curRow += 1
		curCol = 0
		self.TEXT_serverIP = Tkinter.Text(self, state = Tkinter.DISABLED, width = serverClientIPBoxWidth, height = 1, bg = disableBGcolour, fg = disableFGcolour)
		self.TEXT_serverIP.grid(row = curRow, column = curCol, columnspan = 1)
		self.TEXT_serverIP.bind('<ButtonRelease-1>', self.serverClick)
		curCol += 1
		self.TEXT_serverPort = Tkinter.Text(self, state = Tkinter.DISABLED, width = serverClientBoxWidth, height = 1, bg = disableBGcolour, fg = disableFGcolour)
		self.TEXT_serverPort.grid(row = curRow, column = curCol, columnspan = 1)
		self.TEXT_serverPort.bind('<ButtonRelease-1>', self.serverClick)
		curCol += 1
		self.BUTTON_checkConnections = Tkinter.Button(self, text = "Check Connections", command = self.checkConnections)
		self.BUTTON_checkConnections.grid(row = curRow, column = curCol, columnspan = 2)
		curCol += 2
		self.LABEL_command = Tkinter.Label(self, text = "Command")
		self.LABEL_command.grid(row = curRow, column = curCol, columnspan = 1, sticky="e")
		curCol += 1
		self.ENTRY_command = Tkinter.Entry(self, width = 60)
		self.ENTRY_command.insert(0, "")
		self.ENTRY_command.grid(row = curRow, column = curCol, columnspan = 3, sticky="w")
		self.ENTRY_command.bind('<Return>', self.returnKey)
		curCol += 3
		self.BUTTON_quit = Tkinter.Button(self, text = "Send", command = self.sendCommand)
		self.BUTTON_quit.grid(row = curRow, column = curCol)
		curCol += 1
		self.BUTTON_quit = Tkinter.Button(self, text = "Broadcast", command = self.broadcastCommand)
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

		numClients = 16
		self.TEXT_clientNames = []
		self.TEXT_clientIPs = []
		self.TEXT_clientNetIDs = []
		self.TEXT_clientPorts = []
		for i in range(numClients):
			curRow += 1
			curCol = 0
			TEXT_clientName = Tkinter.Text(self, state = Tkinter.DISABLED, width = serverClientBoxWidth, height = 1, bg = disableBGcolour)
			TEXT_clientName.grid(row = curRow, column = curCol)
			TEXT_clientName.bind('<ButtonRelease-1>', self.clientNameClick)
			self.TEXT_clientNames.append(TEXT_clientName)
			curCol += 1
			TEXT_clientIP = Tkinter.Text(self, state = Tkinter.DISABLED, width = serverClientIPBoxWidth, height = 1, bg = disableBGcolour)
			TEXT_clientIP.grid(row = curRow, column = curCol)
			TEXT_clientIP.bind('<ButtonRelease-1>', self.clientIPClick)
			self.TEXT_clientIPs.append(TEXT_clientIP)
			curCol += 1
			TEXT_clientNetID = Tkinter.Text(self, state = Tkinter.DISABLED, width = 6, height = 1, bg = disableBGcolour)
			TEXT_clientNetID.grid(row = curRow, column = curCol)
			TEXT_clientNetID.bind('<ButtonRelease-1>', self.clientNetIDClick)
			self.TEXT_clientNetIDs.append(TEXT_clientNetID)
			curCol += 1
			TEXT_clientPort = Tkinter.Text(self, state = Tkinter.DISABLED, width = 6, height = 1, bg = disableBGcolour)
			TEXT_clientPort.grid(row = curRow, column = curCol)
			TEXT_clientPort.bind('<ButtonRelease-1>', self.clientPortClick)
			self.TEXT_clientPorts.append(TEXT_clientPort)
			curCol += 1

		curRow = textSavedRow
		curCol = 4
		self.TEXT_console = Tkinter.Text(self, state = Tkinter.DISABLED, width = 110, height = 24, bg = disableBGcolour)
		self.TEXT_console.grid(row = curRow, column = curCol, rowspan = 20, columnspan = 7)
		curCol += 7

		curRow += 20
		curCol = 0
		self.BUTTON_quit = Tkinter.Button(self, text = "QUIT", fg = "red", command = self.quit)
		self.BUTTON_quit.grid(row = curRow, column = curCol, columnspan = 1)
		curCol += 1
		self.BUTTON_getGameState = Tkinter.Button(self, text = "Output Game State", command = self.getGameState)
		self.BUTTON_getGameState.grid(row = curRow, column = curCol, columnspan = 2, sticky="w")
		curCol += 2
		self.BUTTON_getIPs = Tkinter.Button(self, text = "Compare Game States", command = self.compareGameStates)
		self.BUTTON_getIPs.grid(row = curRow, column = curCol, columnspan=2, sticky="w")
		curCol += 2
		self.BUTTON_getClientList = Tkinter.Button(self, text = "Server Get Client List", command = self.getClientList)
		self.BUTTON_getClientList.grid(row = curRow, column = curCol, columnspan=1, sticky="w")
		curCol += 1
		self.BUTTON_getIPs = Tkinter.Button(self, text = "Server Get Client IPs", command = self.getClientIPs)
		self.BUTTON_getIPs.grid(row = curRow, column = curCol, columnspan=1,sticky="w")
		curCol += 1
		self.BUTTON_getIPs = Tkinter.Button(self, text = "Server Get Client Details", command = self.getClientDetails)
		self.BUTTON_getIPs.grid(row = curRow, column = curCol, columnspan=2, sticky="w")
		curCol += 2

		curRow += 1
		curCol = 0

root = Tkinter.Tk()
app = HMGUI(master = root)
app.setTitle("Disconnected")
app.mainloop()
root.destroy()
