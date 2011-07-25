#! /usr/bin/python

import xmlrpclib
import xml.dom.minidom
import socket
import sys

def connectToServer(host, port):
	hostAddress = "http://"
	hostAddress += host
	hostAddress += ":"
	hostAddress += str(port)
	ok = False
	try:
		connect = xmlrpclib.Server(hostAddress)
	except Exception:
		print "Exception opening connection to address:", hostAddress

	try:
		connect.help()
	except socket.error:
		print "Failed to connect to address:", hostAddress
	except xmlrpclib.Fault:
		pass
		ok = True
		print "Connected to server:", hostAddress
	else:
		print "Generic failed to connect to address:", hostAddress

	return [ok, connect]

def getClientIps(serverConnection):
	clientInfos = []
	print "Sending g_hm_get_client_ips"
	result = serverConnection.g_hm_get_client_ips()
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

def testServerError():
	result = connectToServer("localhost", 31416)
	serverOK = result[0]
	if (serverOK == False):
		print "OH NOES", str(31416)
		sys.exit(-1)
	else:
		serverConnection = result[1]
		print "Connected to server"

def runTest():
	if 0:
		testServerError()

	result = connectToServer("localhost", 31415)
	serverOK = result[0]
	if (serverOK == False):
		print "OH NOES:", str(31415)
		sys.exit(-1)
	else:
		serverConnection = result[1]

	getClientIps(serverConnection)

if __name__ == '__main__':
	runTest()

