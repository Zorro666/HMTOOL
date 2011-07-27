#!/usr/bin/python

import xml.etree.ElementTree
import httplib
import hashlib
import socket

serverDebug=1
serverDebug=0
password="password"

unknownCommand = "$6[Warning] Unknown command: "
isNotSupported = "is not supported"

result_commandNotFound = 0
result_retryCommand = 1
result_success = 2

class XMLRPCClient():
	def __init__(self, host, port):
		global serverDebug
		self.serverDebug = serverDebug
		self.serverAddress = host
		self.serverAddress += ":"
		self.serverAddress += str(port)
		self.host = host
		self.port = port

	def connect(self):
		self.proxy = httplib.HTTPConnection(self.host, self.port);
		self.proxy.set_debuglevel(self.serverDebug)

	def xmlrpc(self, function, params = ""):
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

		xmlrpcResult = xml.etree.ElementTree.XML(result)
		if xmlrpcResult.tag != "methodResponse":
			print "xmlrpc ERROR bad root node", xmlrpcResult.tag, "should be methodResponse"
			return [False, ""]

		xmlrpc_return_string = ""

		for node in xmlrpcResult:
			if node.tag == "fault":
				print "xmlrpc ERROR fault node found"
				faultStr = ""
				for value in node:
					if value.tag != "value":
						print "xmlrpc ERROR fault.value node not found"
						return [False, xmlrpc_return_string]
					for struct in value:
						if struct.tag != "struct":
							print "xmlrpc ERROR fault.value.struct node not found"
							return [False, xmlrpc_return_string]
						for member in struct:
							if member.tag != "member":
								print "xmlrpc ERROR fault.value.struct.member node not found"
								return [False, xmlrpc_return_string]
							nameStr = ""
							valueStr = ""
							for data in member:
								if data.tag == "name":
									nameStr = data.text
								if data.tag == "value":
									valueStr = data[0].text

							if len(nameStr) > 0:
								faultStr += "Name:" + nameStr + " Value:" + valueStr + "\n"

				xmlrpc_return_string = faultStr
				print "Fault:"
				print xmlrpc_return_string
				return [True, xmlrpc_return_string]

			if node.tag == "params":
				for param in node:
					if param.tag != "param":
						print "xmlrpc ERROR params.param node not found"
						return [False, xmlrpc_return_string]
					for value in param:
						if value.tag != "value":
							print "xmlrpc ERROR params.param.value node not found"
							return [False, xmlrpc_return_string]
						valueStr = value[0].text
						xmlrpc_return_string += valueStr

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

	def processResult(self, command, result):
		index = result.find(unknownCommand)
		if (index == 0):
			print "Command:", command, "Function not found"
			return result_commandNotFound

		index = result.find(isNotSupported)
		if (index > 0):
			print "Command:", command, "Function not found"
			return result_commandNotFound

		if (result == "Illegal Command"):
			print "Command:", command, "Not authenticated"
			self.authenticate()
			return result_retryCommand
		print "Command:", command
		print "Result:", result
		return result_success

	def testConnection(self):
		return self.sendConsoleCommand("r_width")

	def sendConsoleCommand(self, command, params = ""):
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
			status = self.processResult(command, result)
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

