#! /usr/bin/python

from Tkinter import *

class Application(Frame):
	def connectServer(self):
		print "connectServer"

	def createWidgets(self):
		self.BUTTON_quit = Button(self)
		self.BUTTON_quit["text"] = "QUIT"
		self.BUTTON_quit["fg"]   = "red"
		self.BUTTON_quit["command"] =  self.quit

		self.BUTTON_quit.pack(side=LEFT)

		self.BUTTON_connectServer = Button(self)
		self.BUTTON_connectServer["text"] = "Connect Server"
		self.BUTTON_connectServer["command"] = self.connectServer
		self.BUTTON_connectServer.pack(side=LEFT)

		self.FRAME_Frame(self)
		self.TEXT_console = Text(self)
#		self.TEXT_console["text"] = "console output"
		self.TEXT_console.pack(side=BOTTOM, fill=X)

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

root = Tk()
app = Application(master=root)
app.master.title("HM Tool")
app.master.maxsize(400, 300)
app.mainloop()
root.destroy()
