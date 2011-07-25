#! /usr/bin/python

import xmlrpcclient
import xml.dom.minidom
import socket
import sys

def connectToServer(host, port):
	hostAddress = host
	hostAddress += ":"
	hostAddress += str(port)
	ok = False
	proxy = xmlrpcclient.XMLRPCClient()
	try:
		proxy.connect(host, port)
	except Exception:
		print "Exception opening connection to address:", hostAddress
		return [ok, proxy]

	result = proxy.testConnection()
	ok = result[0]
	return [ok, proxy]

def sendConsoleCommand(serverConnection, command, params=""):
	xml_result = serverConnection.sendConsoleCommand(command, params)
	return xml_result

def getClientIps(serverConnection):
	clientInfos = []
	print "Sending g_hm_get_client_ips"
	xml_result = sendConsoleCommand(serverConnection, "g_hm_get_client_ips")
	success = xml_result[0]
	if success == False:
		print "Error during g_hm_get_client_ips"
		return False

	result = xml_result[1]
	foundStart=0
	for l in result.splitlines():
		if (foundStart == 1):
			data = l.split()
			client = data[0].split(":")[1]
			ip = data[1].split(":")[1]
			clientInfo = [client, ip]
			clientInfos.append(clientInfo)
		if (l == "CLIENT_IPS"):
			foundStart=1
			clientInfos = []

	for ci in clientInfos:
		print "Client:", ci[0], "IP:", ci[1]

	return True

def dumpGameState(proxy):
	return proxy.runConsoleCommand("g_hm_dump_game_state")

def runTest():
	result = connectToServer("localhost", 31415)
	serverOK = result[0]
	if (serverOK == False):
		print "Can't connect to server:", "localhost", str(31415)
		sys.exit(-1)
	else:
		serverConnection = result[1]

	serverConnection.runConsoleCommand("test")
	getClientIps(serverConnection)

if __name__ == '__main__':
	runTest()

