#!/usr/bin/python

import xml.parsers.expat
import httplib
import hashlib
import socket

serverDebug=1
serverDebug=0
password="password"

unknownCommand = "$6[Warning] Unknown command: "

result_commandNotFound = 0
result_retryCommand = 1
result_success = 2

xmlrpc_return_string = ""

# 3 handler functions
def xml_start_element(name, attrs):
	global serverDebug
	if serverDebug:
		print 'Start element:', name, attrs

def xml_end_element(name):
	global serverDebug
	if serverDebug:
		print 'End element:', name

def xml_char_data(data):
	global xmlrpc_return_string
	xmlrpc_return_string += str(data)
	global serverDebug
	if serverDebug:
		print xmlrpc_return_string
		print 'Character data:', repr(data)

class XMLRPCClient():
	def connect(self, host, port):
		self.proxy = httplib.HTTPConnection(host, port);
		global serverDebug
		self.proxy.set_debuglevel(serverDebug)
		self.serverDebug = serverDebug

		self.serverAddress = host
		self.serverAddress += ":"
		self.serverAddress += str(port)

	def xmlrpc(self, function, params=""):
		postBody = "<?xml version='1.0'?>\n"
		postBody += "<methodCall>\n"
		postBody += "<methodName>"
		postBody += function
		postBody += "</methodName>\n"

		postBody += "<params>\n"

		if len(params) > 0:
			postBody += "<param>"
			postBody += "<value>"
			postBody += "<string>"
			postBody += params

		if len(params) > 0:
			postBody += "</string>"
			postBody += "</value>"
			postBody += "</param>\n"

		postBody += "</params>\n"
		postBody += "</methodCall>\n"

		postHeaders = {"Content-Type" : "text/xml"}
		command = "'"
		command += function
		if params != "":
			command += " "
			command += params
		command += "'"

		try:
			self.proxy.request("POST", "/RPC2", postBody, postHeaders)
		except socket.error:
			print "xmlrpc:", command, ": Socket error connecting to server:", self.serverAddress
			return [False,""]
		except httplib.ResponseNotReady:
			print "xmlrpc:", command, ": Server not connected:", self.serverAddress
			return [False,""]
		except httplib.CannotSendRequest:
			print "xmlrpc:", command, ": Server not connected:", self.serverAddress
			return [False,""]
#		else:
#			print "xmlrpc:", command, ": Generic failed to post request to server:", self.serverAddress
#			return [False,""]

		response = self.proxy.getresponse()
		result = response.read()

		if self.serverDebug:
			print "XMLRPC Response:"
			print result
			print "len=", len(result)

		if response.status == httplib.NOT_FOUND:
			result_commandNotFound = 0
			return [True, unknownCommand]

		global xmlrpc_return_string
		xmlrpc_return_string = ""

		xmlp = xml.parsers.expat.ParserCreate()
		xmlp.StartElementHandler = xml_start_element
		xmlp.EndElementHandler = xml_end_element
		xmlp.CharacterDataHandler = xml_char_data

		xmlp.Parse(result)

		if self.serverDebug:
			print "START New Reply:"
			print xmlrpc_return_string
			print "END New Reply:"

		return [True, xmlrpc_return_string]

	def authenticate(self):
		print "Authenticating...."
		print "Calling challenge()"
		xmlrpc_result = self.xmlrpc("challenge")
		success = xmlrpc_result[0]
		if success == False:
			print "Authenticate: xmlrpc failed"
			return False

		result = xmlrpc_result[1]
		print "Result:", result
		challengeResponse = result

		challengeAnswer = challengeResponse+":"+password
		m = hashlib.md5()
		m.update(challengeAnswer)
		authenticateDigest = m.hexdigest()

		print "Calling authenticate(",authenticateDigest,")"
		result = self.xmlrpc("authenticate", authenticateDigest)
		print "Result:", result
		return True

	def processResult(self, result):
		index = result.find(unknownCommand)
		if (index == 0):
			print "    Function not found"
			return result_commandNotFound
		if (result == "Illegal Command"):
			print "Not authenticated"
			self.authenticate()
			return result_retryCommand
		print "Result:", result
		return result_success

	def testConnection(self):
		return self.sendConsoleCommand("r_width")

	def sendConsoleCommand(self, command, params=""):
		rpcCommand = "'"
		rpcCommand += command
		if params != "":
			rpcCommand += " "
			rpcCommand += params
		rpcCommand += "'"
		status = result_retryCommand
		while (status  == result_retryCommand):
			print "Calling", rpcCommand, "on Server:", self.serverAddress
			xmlrpc_result = self.xmlrpc(command, params)
			success = xmlrpc_result[0]
			if success == False:
				print "sendConsoleCommand: xmlrpc failed"
				return [False, ""]
			result = xmlrpc_result[1]
			status = self.processResult(result)
		return [True, result]

def runTest():
	proxy = XMLRPCClient()
	proxy.connect("localhost", 81)

	proxy.testConnection(proxy)
	proxy.authenticate()
	proxy.testConnection(proxy)

	dumpGameState(proxy)

if __name__ == '__main__':
	runTest()

