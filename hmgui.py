#! /usr/bin/python

import Tkinter 
import hmclient

class HMGUI(Tkinter.Frame):
	def consolePrint(self, output):
		self.TEXT_console.insert(Tkinter.END,"Server:")
		self.TEXT_console.insert(Tkinter.END,self.serverStr)
		self.TEXT_console.insert(Tkinter.END," ")
		self.TEXT_console.insert(Tkinter.END,output)
		self.TEXT_console.insert(Tkinter.END,"\n")
		self.TEXT_console.see(Tkinter.END)

	def connectServer(self):
		serverName=self.ENTRY_serverIP.get()
		serverPort=self.ENTRY_serverPort.get()
		self.serverStr=serverName+":"+serverPort
		result = hmclient.connectToServer(serverName, serverPort)
		self.serverOK = result[0]
		if (self.serverOK == False):
			self.consolePrint("ERROR failed to connect to server")
		else:
			self.serverConnection = result[1]
			self.serverName=serverName
			self.serverPort=serverPort
			self.BUTTON_connectServer["text"] = "Connected to:"+self.serverStr
			self.BUTTON_connectServer["command"] = self.connectServer
			self.consolePrint("Connected to server")

	def sendCommand(self):
		command = self.ENTRY_command.get()
		xml_result = hmclient.sendConsoleCommand(self.serverConnection, command)
		success = xml_result[0]
		result = xml_result[1]
		self.consolePrint("Sent Command:"+command)
		self.consolePrint("Command Result:"+str(success))
		self.consolePrint(result)

	def createWidgets(self):
		curRow=0
		curCol=0
		self.LABEL_serverIP = Tkinter.Label(self)
		self.LABEL_serverIP["text"] = "Server IP"
		self.LABEL_serverIP.grid(row=curRow, column=curCol)
		curCol+=1
		self.ENTRY_serverIP = Tkinter.Entry(self)
		self.ENTRY_serverIP.insert(0, "localhost")
		self.ENTRY_serverIP.grid(row=curRow, column=curCol)
		curCol+=1

		self.LABEL_serverPort = Tkinter.Label(self)
		self.LABEL_serverPort["text"] = "Server Port"
		self.LABEL_serverPort.grid(row=curRow, column=curCol)
		curCol+=1
		self.ENTRY_serverPort = Tkinter.Entry(self)
		self.ENTRY_serverPort.insert(0, "31415")
		self.ENTRY_serverPort.grid(row=curRow, column=curCol)
		curCol+=1

		self.BUTTON_connectServer = Tkinter.Button(self)
		self.BUTTON_connectServer["text"] = "Connect Server"
		self.BUTTON_connectServer["command"] = self.connectServer
		self.BUTTON_connectServer.grid(row=curRow, column=curCol)
		curCol+=1

		curRow+=1
		curCol=0
		self.LABEL_command = Tkinter.Label(self)
		self.LABEL_command["text"] = "Command"
		self.LABEL_command.grid(row=curRow, column=curCol, columnspan=1)
		curCol+=1
		self.ENTRY_command = Tkinter.Entry(self)
		self.ENTRY_command["width"] = 60
		self.ENTRY_command.insert(0, "")
		self.ENTRY_command.grid(row=curRow, column=curCol, columnspan=3)
		curCol+=3
		self.BUTTON_quit = Tkinter.Button(self)
		self.BUTTON_quit["text"] = "Send Command"
		self.BUTTON_quit["command"] = self.sendCommand
		self.BUTTON_quit.grid(row=curRow, column=curCol)
		curCol+=1

		curRow+=1
		curCol=0
		self.TEXT_console = Tkinter.Text(self)
		self.TEXT_console.grid(row=curRow, columnspan=5)
		curCol+=1

		curRow+=1
		curCol=0
		self.BUTTON_quit = Tkinter.Button(self)
		self.BUTTON_quit["text"] = "QUIT"
		self.BUTTON_quit["fg"] = "red"
		self.BUTTON_quit["command"] = self.quit
		self.BUTTON_quit.grid(row=curRow, column=curCol)
		curCol+=1

		curRow+=1
		curCol=0

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
