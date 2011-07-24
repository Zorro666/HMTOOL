#! /usr/bin/python

import xmlrpclib
import SimpleXMLRPCServer

def g_hm_get_client_ips():
	print "g_hm_get_client_ips"
	client_ips = "Console command: g_hm_get_client_ips\n"
	client_ips += "CLIENT_IPS\n"
	client_ips += "Client:zorro IP:localhost\n"
	client_ips += "Client:zorro2 IP:localhost\n"
	return str(client_ips)

server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 31415))
print "Hello I am a server"
#server.register_function(g_hm_get_client_ips, "g_hm_get_client_ips")
server.register_function(g_hm_get_client_ips)
server.serve_forever()

