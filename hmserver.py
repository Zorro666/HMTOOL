#! /usr/bin/python

import sys
import xmlrpclib
import SimpleXMLRPCServer
import shlex
import subprocess

debug = 0
gameServer = 1
gameClient = 0
host = "0.0.0.0"
portStr = "31415"

for arg in sys.argv:
	if arg == "-server":
		gameServer = 1
		gameClient = 0
	if arg == "-client":
		gameServer = 0
		gameClient = 1
	if arg == "-debug":
		debug = 1
	if arg.startswith("-port="):
			portStr = arg[len("-port="):]
	if arg.startswith("-host="):
			host = arg[len("-host="):]

print "debug=",debug
print "gameServer=",gameServer
print "gameClient=",gameClient
print "host=",host
print "portStr=",portStr

if portStr.isdigit() == False:
	print "ERROR port must be a number"
	sys.exit(-1)

port = int(portStr)
print "port=",str(port)

def status():
	print serverName+"status"
	if gameServer:
		statusResult = "Status:" + "\n"
		statusResult += "[CONSOLE] Executing console command 'status'" + "\n"
		statusResult += "-----------------------------------------" + "\n"
		statusResult += "Server Status:" + "\n"
		statusResult += "name: " + "\n"
		statusResult += "ip: NOTPC1161" + "\n"
		statusResult += "version: 1.0.0.1" + "\n"
		statusResult += "level: pvp/dst_lighthouse" + "\n"
		statusResult += "gamerules: Seizure" + "\n"
		statusResult += "players: 1/16" + "\n"
		statusResult += "time remaining: 19:10" + "\n"
		statusResult += " -----------------------------------------" + "\n"
		statusResult += "Connection Status:" + "\n"
		statusResult += "name: zorro  id: 1  ip: [10.16.5.161]NOTPC1161.INTERN.CRYTEK.DE:63146  ping: 1  state: 3 profile: 5" + "\n"
		statusResult += "name: zorro2 id: 2  ip: [10.16.5.161]NOTPC1161.INTERN.CRYTEK.DE:63146  ping: 1  state: 3 profile: 5" + "\n"
		statusResult += "name: zorro3 id: 2  ip: [10.16.5.162]NOTPC1161.INTERN.CRYTEK.DE:63146  ping: 1  state: 3 profile: 5" + "\n"

	if gameClient:
		statusResult = "Client:" + "\n"
		statusResult += "[CONSOLE] Executing console command 'status'" + "\n"
		statusResult += "-----------------------------------------" + "\n"
		statusResult += "Client Status:" + "\n"
		statusResult += "name: " + "\n"
		statusResult += "ip: NOTPC1161" + "\n"
		statusResult += "version: 1.0.0.1" + "\n"
		statusResult += "name: zorro  entID:65532" + "\n"

	return str(statusResult)

def g_hm_dump_gamestate():
	print serverName+"g_hm_dump_gamestate"
	if gameServer:
		fileName = "Server__NOTPC1161.xml"
	if gameClient:
		fileName = "Client_zorro_NOTPC1161.xml"
	f = open(fileName, 'r')
 
	gameState = "Command: g_hm_dump_gamestate" + "\n"
	gameState += "Result: [CONSOLE] Executing console command 'g_hm_dump_gamestate'" + "\n"
	gameState += f.read()
	gameState += "--------------------------------------------------------------------------------" + "\n"
	gameState += "Host Migration:DumpGameStateHM output to '%USER%/HostMigration/Server__NOTPC1161.xml'" + "\n"     

	return gameState

def jake(params):
	print serverName+"jake", params
	if gameClient:
		return "ERROR: client can't spawn servers"

	netIDs = params.split()
	resultStr = ""
	for netID in netIDs:
		clientPort = str(int(port) + int(netID))
		cmdline = "hmserver.py -client -port=" + clientPort
		print serverName+cmdline
		args = shlex.split(cmdline)
		p = subprocess.Popen(args)
		resultStr += "NetID " + netID + " client "+ clientPort + "\n"

	return resultStr

server = SimpleXMLRPCServer.SimpleXMLRPCServer((host, port), logRequests = debug)
serverName = host+":"+str(port)+":"

print serverName+""
print serverName+"Hello I am a HTTP server running on "+host+":"+str(port)
if gameServer:
	print serverName+"Acting as a fake game server"
if gameClient:
	print serverName+"Acting as a fake game client"
print serverName+""

server.register_function(g_hm_dump_gamestate)
server.register_function(status)
server.register_function(jake)
server.serve_forever()

