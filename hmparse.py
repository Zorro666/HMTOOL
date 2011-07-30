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

	def loadServerXML(self, serverFileName):
		print "loadServerXML:", serverFileName
		if os.path.isfile(serverFileName) == False:
			print "file does't exist:", serverFileName
			return
		self.serverXML = xml.etree.ElementTree.parse(serverFileName).getroot()
		self.parseServerXML()

	def setServerXML(self, serverXMLstring):
		print "serServerXML"
		self.serverXML = xml.etree.ElementTree.XML(serverXMLstring)
		self.parseServerXML()

	def parseServerXML(self):
		result = self.parseHMGameStateXML("Server", self.serverXML)
		if result[0] == False:
			print "parseServerXML failed"
			self.serverXML = None
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
	this = HMParse()
	this.loadServerXML("Jake.xml")
	this.loadServerXML("GameState_2011_07_29_07_09_Server_localhost_31415.xml")

if __name__ == '__main__':
	runTest()
