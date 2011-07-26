#! /usr/bin/python

import sys
import xmlrpclib
import SimpleXMLRPCServer

debug = 0
gameServer = 1
gameClient = 0

for arg in sys.argv:
	if arg == "-server":
		gameServer = 1
		gameClient = 0
	if arg == "-client":
		gameServer = 0
		gameClient = 1
	if arg == "-debug":
		debug = 1

def status():
	print "status"
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

def g_hm_dump_game_state():
	print "g_hm_dump_game_state"
	if gameServer:
		fileName = "Server__NOTPC1161.xml"
	if gameClient:
		fileName = "Client_jake_NOTPC1161.xml"
	f = open(fileName, 'r')
	gameState = f.read()

	return gameState

server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 31415), logRequests = debug)
print "Hello I am a HTTP server"
if gameServer:
	print "Acting as a fake game server"
if gameClient:
	print "Acting as a fake game client"

server.register_function(g_hm_dump_game_state)
server.register_function(status)
server.serve_forever()

