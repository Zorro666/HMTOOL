#! /usr/bin/python

import xmlrpclib
import SimpleXMLRPCServer

def test():
	print "test"

def status():
	print "status"
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
	return str(statusResult)

def g_hm_get_client_ips():
	print "g_hm_get_client_ips"
	client_ips = "Console command: g_hm_get_client_ips\n"
	client_ips += "CLIENT_IPS\n"
	client_ips += "Client:zorro IP:localhost\n"
	client_ips += "Client:zorro2 IP:localhost\n"
	return str(client_ips)

server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 31415), logRequests = 1)
print "Hello I am a server"
server.register_function(g_hm_get_client_ips)
server.register_function(test)
server.register_function(status)
server.serve_forever()

