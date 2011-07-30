#! /usr/bin/python

import xml.etree.ElementTree
import os.path
from hmgamestate import GameStateInfo 

# Example file for parsing
#<HM_GameState>
# <net_entities>
#  <e AHI="000" C="SpawnPoint" CC="0" F="0x0" N="ResultViewPlayerSpawn_2" NI="1" ORI="0.00,0.00,0.93,0.37" P="" POS="102.4,83.0,40.9" />
#  <e AHI="010" C="BasicEntity" CC="1" F="0x0" N="Helicopter_body1" NI="2" ORI="-0.22,-0.07,0.59,0.77" P="BasicEntity2" POS="319.0,55.0,-15.7">
#   <c N="Sound_Helicopter" />
# </e>
# </net_entities>
# <net_actors>
#  <a A="125" AC="0" BC="100" CI="137" D="0" H="125" IC="1" MA="125" MH="125" N="zorro" NI="129">
#   <i NI="135" />
#   <b C="100" N="ammo_pack" />
# </a>
# </net_actors>
# <global numNetAct="3" numNetEnt="135" />
#</HM_GameState>

class HMParse():
	def __init__(self):
		self.serverXML = None
		self.clientXMLs = []
		self.serverGameStateInfo = GameStateInfo()
		self.clientGameStateInfos = [GameStateInfo()]

	def loadClientXMLs(self, clientFileNames):
		self.clientGameStateInfos = []
		for clientFileName in clientFileNames:
			self.loadClientXML(clientFileName)

	def loadClientXML(self, clientFileName):
		print "loadClientXML:", clientFileName
		if os.path.isfile(clientFileName) == False:
			print "file does't exist:", clientFileName
			return
		clientXML = xml.etree.ElementTree.parse(clientFileName).getroot()
		# "GameState_2011_07_29_15_41_zorro_2_10.16.5.161_31544.xml"
		tokens = clientFileName.split("_")
		nickname = "Client " + "_".join(tokens[6:-2])
		print "Tokens:", tokens
		print "File:", clientFileName, "nickname:", nickname
		clientXML = xml.etree.ElementTree.parse(clientFileName).getroot()
		clientXMLstring = xml.etree.ElementTree.tostring(clientXML)
		self.addClientXML(nickname, clientXMLstring)

	def addClientXML(self, nickname, clientXMLstring):
		print "addClientXML"
		clientXML = xml.etree.ElementTree.XML(clientXMLstring)
		self.parseClientXML(nickname, clientXML)

	def parseClientXML(self, nickname, clientXML):
		result = self.parseHMGameStateXML(nickname, clientXML)
		if result[0] == False:
			print "parseServerXML failed"
			return

		print "parseClientXML succeeded"
		self.clientXMLs.append(clientXML)
		clientGameStateInfo = result[1]
		self.clientGameStateInfos.append(clientGameStateInfo)

		print clientGameStateInfo.output()

	def loadServerXML(self, serverFileName):
		print "loadServerXML:", serverFileName
		if os.path.isfile(serverFileName) == False:
			print "file does't exist:", serverFileName
			return
		serverXML = xml.etree.ElementTree.parse(serverFileName).getroot()
		serverXMLstring = xml.etree.ElementTree.tostring(serverXML)
		self.setServerXML(serverXMLstring)

	def setServerXML(self, serverXMLstring):
		print "serServerXML"
		self.serverXML = xml.etree.ElementTree.XML(serverXMLstring)
		self.parseServerXML()

	def parseServerXML(self):
		result = self.parseHMGameStateXML("Server", self.serverXML)
		if result[0] == False:
			print "parseServerXML failed"
			self.serverXML = None
			return
		print "parseServerXML succeeded"
		self.serverGameStateInfo = result[1]
		print self.serverGameStateInfo.output()

	def parseHMGameStateXML(self, nickname, gameStateXML):
		gameStateInfo = GameStateInfo()
		if gameStateXML.tag != "HM_GameState":
			print "ERROR can't find HM_GameState:"+gameStateXML.tag
			return [False, gameStateInfo]

		success = gameStateInfo.parse(nickname, gameStateXML)
		return [success, gameStateInfo]

def runTest():
	thisA = HMParse()
	thisA.loadServerXML("Jake.xml")
	thisA.loadServerXML("GameState_2011_07_29_15_41_Server_localhost_31415.xml")
	gameStateA = thisA.serverGameStateInfo

	thisA.loadClientXMLs(["GameState_2011_07_29_15_41_zorro_2_10.16.5.161_31544.xml"])
	gameStateB = thisA.clientGameStateInfos[0]
	print ""
	print "############# Comparing state #####################"
	print ""
	res = gameStateA.compare(gameStateB)
	print res[1]

if __name__ == '__main__':
	runTest()
