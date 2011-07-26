#! /usr/bin/python

import xmlrpcclient
import xml.dom.minidom
import socket
import sys

class Connection():
	def __init__(self):
		self.valid = False
		self.string = ""
		self.host = ""
		self.port = ""
		self.connection = xmlrpcclient.XMLRPCClient(self.host, self.port)

	def connectToServer(self, host, port):
		hostAddress = host
		hostAddress += ":"
		hostAddress += str(port)
		ok = False
		self.valid = False
		self.connection = xmlrpcclient.XMLRPCClient(host, port)
		try:
			self.connection.connect()
		except Exception:
			print "Exception opening connection to address:", hostAddress
			return [ok, proxy]

		result = self.connection.testConnection()
		self.host = host
		self.port = str(port)
		self.valid= True
		self.string = self.host+":"+self.port
		ok = result[0]
		return ok

	def sendConsoleCommand(self, command, params = ""):
		xml_result = self.connection.sendConsoleCommand(command, params)
		return xml_result

	def getClientIPs(self):
		xml_result = self.sendConsoleCommand("status")
		success = xml_result[0]
		if success == False:
			print "Error during status"
			return False
		result = xml_result[1]
		foundStart = 0
		for l in result.splitlines():
			if (foundStart == 1):
				parsedOK = True
				foundInfo = False

				if l == "":
					parsedOK = False
	#name: zorro  id: 1  ip: [10.16.5.161]NOTPC1161.INTERN.CRYTEK.DE:63146  ping: 1  state: 3 profile: 5
				if parsedOK:
					parsedOK = False
					nameStart = l.find("name:")
					if nameStart != -1:
							idStart = l.find("id:")
							if idStart != -1:
								client = l[nameStart+len("name:"):idStart]
								client = client.strip()
								parsedOK = True

				if parsedOK:
					parsedOK = False
					ipStart = l.find("ip:")
					if ipStart != -1:
							pingStart = l.find("ping:")
							if pingStart != -1:
								ipInfo = l[ipStart+len("ip:"):pingStart]
								ipInfo = ipInfo.strip()
	#ip: [10.16.5.161]NOTPC1161.INTERN.CRYTEK.DE:63146
								ipNumStart = ipInfo.find("[")
								if ipNumStart != -1:
									ipNumEnd = ipInfo.find("]")
									if ipNumEnd != -1:
										ip = ipInfo[ipNumStart+1:ipNumEnd]
										ip = ip.strip()
										parsedOK = True
										foundInfo = True

				if foundInfo:
					clientInfo = [client, ip]
					clientInfos.append(clientInfo)

			if l == "Connection Status:":
				foundStart = 1
				clientInfos = []

		info = ""
		for ci in clientInfos:
			infoStr = "Client:'"+ci[0]+"' IP:"+ci[1]
			print infoStr
			info += infoStr
			info += "\n"
		return [True, info]

def dumpGameState(proxy):
	return proxy.runConsoleCommand("g_hm_dump_game_state")

def runTest():
	connection = Connection()
	result = connection.connectToServer("localhost", 31415)
	if (connection.valid == False):
		print "Can't connect to server:", "localhost", str(31415)
		sys.exit(-1)

	connection.sendConsoleCommand("test")
	connection.getClientIPs()

if __name__ == '__main__':
	runTest()

