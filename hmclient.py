#! /usr/bin/python

import xmlrpcclient
import xml.etree.ElementTree
import datetime
import socket
import sys

class Connection():
	def __init__(self):
		self.valid = False
		self.string = ""
		self.host = ""
		self.port = ""
		self.connection = xmlrpcclient.XMLRPCClient(self.host, self.port)
		self.clientDetails = []
		self.detail = ["", "", "", ""]

	def getHost(self):
		return self.host

	def getIP(self):
		return self.host

	def getPort(self):
		return self.port

	def getDetail(self):
		return self.detail

	def setDetail(self, name, IP, netID, port):
		self.detail = [name, IP, netID, port]

	def connectToHTTPServer(self, host, port):
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

	def testConnection(self):
		result = self.connection.testConnection()
		ok = result[0]
		return ok

	def close(self):
		self.connection.close()
		self.valid = False
		self.string = ""
		self.host = ""
		self.port = ""
		self.clientDetails = []
		self.detail = ["", "", "", ""]

	def sendConsoleCommand(self, command, params = ""):
		rpc_result = self.connection.sendConsoleCommand(command, params)
		return rpc_result

	def getClientIPs(self):
		rpc_result = self.sendConsoleCommand("status")
		success = rpc_result[0]
		if success == False:
			print "Error during status"
			return [False, ""]
		result = rpc_result[1]
		foundStart = 0
		clientInfos = []
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

		self.clientDetails = []
		for ci in clientInfos:
			# Name, IP, NetID, port
			cd = [ci[0], ci[1], "", ""]
			self.clientDetails.append(cd)

		self.dumpClientDetails()

		info = ""
		for ci in clientInfos:
			infoStr = "Client:'"+ci[0]+"' IP:"+ci[1]
			#print infoStr
			info += infoStr
			info += "\n"
		return [True, clientInfos]

	def getServerIP(self):
		rpc_result = self.sendConsoleCommand("status")
		success = rpc_result[0]
		if success == False:
			print "Error during status"
			return [False, ""]
		result = rpc_result[1]
		foundServer = 0
		serverIP = ""
		for l in result.splitlines():
				if l == "Server Status:":
					foundServer = 1
				if foundServer == 1:
					ipStart = l.find("ip:")
					if ipStart == 0:
						ipInfo = l[ipStart+len("ip:"):]
						ipInfo = ipInfo.strip()
						serverIP = ipInfo
							
		return [True, serverIP]

	def getClientList(self):
		result = self.getGameState()
		if result[0] == False:
			print "Error during getGameState"
			return [False, ""]

		clientList = []

		gameStateXML = xml.etree.ElementTree.XML(result[1])
		if gameStateXML.tag != "HM_GameState":
			print "ERROR"+gameStateXML.tag
			return [False, clientList]
		for node in gameStateXML:
			if node.tag == "net_actors":
				print "Found net_actors"
				for netActor in node:
					netID = netActor.get("NI")
					name = netActor.get("N")
					ci = [name, netID]
					clientList.append(ci)

		for ci in clientList:
			# Name, IP, NetID, port
			for cd in self.clientDetails:
				if cd[0] == ci[0]:
					cd[2] = ci[1]
					break
			
#		for ci in clientList:
#			print "Name:", ci[0], " NetID:",ci[1]

		self.dumpClientDetails()

		return [True, clientList]

	def dumpClientDetails(self):
		print "ClientDetails"
		for cd in self.clientDetails:
			infoStr = "Client Name:'"+cd[0]+"' IP:"+cd[1]+ " NetID:"+cd[2]+ " Port:"+cd[3]
			print infoStr

	def getClientDetailsList(self, forceUpdate = False):
		if len(self.clientDetails) > 0:
			if forceUpdate == False:
				return [True, self.clientDetails]

		result = self.getClientIPs()
		if result[0] == False:
			self.clientDetails = []
			return [False, ""]
		result = self.getClientList()
		if result[0] == False:
			self.clientDetails = []
			return [False, ""]

		return [True, self.clientDetails]

	def getGameState(self, saveToFile = False, filePrefix = ""):
		rpc_result = self.sendConsoleCommand("g_hm_dump_gamestate")
		success = rpc_result[0]
		if success == False:
			print "Error during g_hm_dump_gamestate"
			return [False, ""]
		result = rpc_result[1]

		xml_start = result.find("<HM_GameState")
		xml_end = result.find("</HM_GameState")
		xml_data = result[xml_start:xml_end+len("</HM_GameState>")]
		if saveToFile == True:
			gameStateXML = xml.etree.ElementTree.XML(xml_data)
			if gameStateXML.tag != "HM_GameState":
				print "ERROR"+gameStateXML.tag
			else:
				now = datetime.datetime.now()
				nowString = now.strftime("%Y_%m_%d_%H_%M")
				print "now=", str(now)
				print "nowString =", nowString
				filename = "GameState_"
 				filename += nowString
				filename += "_" 
 				filename += filePrefix 
				filename += "_" 
				filename += self.host 
				filename += "_" 
				filename += self.port 
				filename += ".xml"
				xmlOutput = "<?xml version='1.0' ?>" + "\n"
				xmlOutput += xml.etree.ElementTree.tostring(gameStateXML)
				f = open(filename, "w")
				f.write(xmlOutput)
				f.close()
				print "Save Game State XML output to:", filename

		return [True, xml_data]

	def isServer(self):
		rpc_result = self.sendConsoleCommand("status")
		success = rpc_result[0]
		if success == False:
			print "Error during status"
			return False
		result = rpc_result[1]
		for l in result.splitlines():
				if l == "Server Status:":
					return True;
		return False

	def isClient(self):
		rpc_result = self.sendConsoleCommand("status")
		success = rpc_result[0]
		if success == False:
			print "Error during status"
			return False
		result = rpc_result[1]
		clientName = ""
		isClient = False
		for l in result.splitlines():
				if l == "Client Status:":
					isClient = True
				#name: zorro  entID:65532
				if isClient:
					nameStart = l.find("name:")
					if nameStart == 0:
						nameEnd = l.find("entID:")
#						print "nameStart:", nameStart
#						print "nameEnd:", nameEnd
						if nameEnd > nameStart:
							name = l[nameStart+len("name:"):nameEnd]
#							print "name found:", name
							clientName = name.strip()
							break

		return [isClient, clientName]

def runTest():
	connection = Connection()
	result = connection.connectToHTTPServer("localhost", 31415)
	if (connection.valid == False):
		print "Can't connect to server:", "localhost", str(31415)
		sys.exit(-1)

	connection.sendConsoleCommand("test")
	connection.getClientIPs()

if __name__ == '__main__':
	runTest()

