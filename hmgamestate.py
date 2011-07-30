#! /usr/bin/python

import xml.etree.ElementTree
import os.path

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

class NetEntityChildEntity():
	def __init__(self):
   #<c N="Particle_rocket_d" />
		self.name = ""

	def parse(self, netEntityChildEntityXMLnode):
		self.name = netEntityChildEntityXMLnode.get("N")
		return True

	def output(self):
		out = ""
		out += "Name:" + self.name
		return out

class NetEntity():
	def __init__(self):
		#<e AHI="010" C="BasicEntity" CC="1" F="0x0" N="rocket_cin2_4" NI="127" ORI="0.72,-0.19,0.64,0.18" P="" POS="525.0,554.5,40.3">
			#<c N="Particle_rocket_d" />
		#</e>
		self.active = 0
		self.hidden = 0
		self.invisible = 0
		self.className = ""
		self.numChildren = 0
		self.flags = 0
		self.name = ""
		self.netID = -1
		self.orient = [0.0, 0.0, 0.0]
		self.pos = [0.0, 0.0, 0.0]
		self.children = []

	def parse(self, netEntityXMLnode):
		#<e AHI="010" C="BasicEntity" CC="1" F="0x0" N="rocket_cin2_4" NI="127" ORI="0.72,-0.19,0.64,0.18" P="" POS="525.0,554.5,40.3">
			#<c N="Particle_rocket_d" />
		#</e>
		self.active = netEntityXMLnode.get("AHI")
		self.hidden = netEntityXMLnode.get("AHI")
		self.invisible = netEntityXMLnode.get("AHI")
		self.className = netEntityXMLnode.get("C")
		self.numChildren = netEntityXMLnode.get("CC")
		self.flags = netEntityXMLnode.get("F")
		self.name = netEntityXMLnode.get("N")
		self.netID = netEntityXMLnode.get("NI")
		self.orient = netEntityXMLnode.get("ORI")
		self.pos = netEntityXMLnode.get("POS")
		self.children = []

		for childNode in netEntityXMLnode:
			if childNode.tag == "c":
				childEntity = NetEntityChildEntity()
				if childEntity.parse(childNode) == False:
					print "ERROR parsing item child node"
					return False
				else:
					self.children.append(childEntity)
			else:
				print "ERROR unknown childNode tag:", childNode.tag
				return False

		#TODO: numChildren should match children array length
		return True

	def output(self):
		out = "NetEntity"
		out += " Name:" + self.name
		out += " NetID:" + self.netID
		out += " ClassName:" + self.className
		out += " Active:" + self.active
		out += " Hidden:" + self.hidden
		out += " Invisible:" + self.invisible
		out += " Flags:" + self.flags
		out += " Orient:" + self.orient
		out += " Pos:" + self.pos
		out += "\n"
		out += " NumChildren:" + self.numChildren
		for child in self.children:
			out += "\n"
			out += "  Child "
			out += child.output()
		return out

class NetActorItem():
	def __init__(self):
   	#<i NI="135" />
		self.netID = -1

	def parse(self, netActorItemXMLnode):
		self.netID = netActorItemXMLnode.get("NI")
		return True

	def output(self):
		out = ""
		out += "NetID:" + self.netID
		return out

class NetActorAmmo():
	def __init__(self):
   	#<b C="100" N="ammo_pack" />
		self.count = 0
		self.name = ""

	def parse(self, netActorAmmoXMLnode):
		self.count = netActorAmmoXMLnode.get("C")
		self.name = netActorAmmoXMLnode.get("N")
		return True

	def output(self):
		out = ""
		out += "Name:" + self.name
		out += " Count:" + self.count
		return out

class NetActorAccessory():
	def __init__(self):
   	# ??????????????????
		self.name = ""

	def parse(self, netActorAccessoryXMLnode):
		self.name = netActorAccessoryXMLnode.get("N")
		return True

	def output(self):
		out = ""
		out += "Name:" + self.name
		return out

class NetActor():
	def __init__(self):
  	#<a A="125" AC="0" BC="100" CI="137" D="0" H="125" IC="5" MA="125" MH="125" N="zorro2" NI="140">
   		#<i NI="135" />
   		#<b C="100" N="ammo_pack" />
  	#</a>
		self.name = ""
		self.netID = -1
		self.armour = 0
		self.maxArmour = 0
		self.health = 0
		self.maxHealth = 0
		self.currentItem = -1
		self.numItems = 0
		self.dead = 0
		self.numAccessories = 0
		self.numAmmos = 0
		self.items = []
		self.ammos = []
		self.accessories = []

	def parse(self, netActorXMLnode):
  	#<a A="125" AC="0" BC="100" CI="137" D="0" H="125" IC="5" MA="125" MH="125" N="zorro2" NI="140">
   		#<i NI="135" />
   		#<b C="100" N="ammo_pack" />
  	#</a>
		self.name = netActorXMLnode.get("N")
		self.netID = netActorXMLnode.get("NI")
		self.armour = netActorXMLnode.get("A")
		self.maxArmour = netActorXMLnode.get("MA")
		self.health = netActorXMLnode.get("H")
		self.maxHealth = netActorXMLnode.get("MH")
		self.currentItem = netActorXMLnode.get("CI")
		self.numItems = netActorXMLnode.get("IC")
		self.dead = netActorXMLnode.get("D")
		self.numAccessories = netActorXMLnode.get("AC")
		self.numAmmos = netActorXMLnode.get("BC")
		self.items = []
		self.ammos = []
		for childNode in netActorXMLnode:
			if childNode.tag == "i":
				item = NetActorItem()
				if item.parse(childNode) == False:
					print "ERROR parsing item child node"
					return False
				else:
					self.items.append(item)
			elif childNode.tag == "b":
				ammo = NetActorAmmo()
				if ammo.parse(childNode) == False:
					print "ERROR parsing ammo child node"
					return False
				else:
					self.ammos.append(ammo)
			elif childNode.tag == "a":
				accessory = NetActorAccessory()
				if accessory.parse(childNode) == False:
					print "ERROR parsing accessory child node"
					return False
				else:
					self.accessory.append(accessory)
			else:
				print "ERROR unknown childNode tag:", childNode.tag
				return False

		#TODO: numItems should match items array length
		#TODO: numAmmos should match ammos array length - but it won't until the output from game is fixed
		#TODO: numAccessories should match accessories array length
		return True

	def output(self):
		out = "NetActor"
		out += " Name:" + self.name
	 	out += " NetID:" + self.netID 
	 	out += " Dead:" + self.dead
		out += " Health:" + self.health
		out += " MaxHealth:" + self.maxHealth 
		out += " Armour:" + self.armour
		out += " MaxArmour:" + self.maxArmour
		out += " CurrentItem:" + self.currentItem
		out += "\n"
		out += " NumItems:" + self.numItems
		for item in self.items:
			out += "\n"
			out += "  Item "
			out += item.output()
		out += "\n"
		out += " NumAmmos:" + self.numAmmos
		for ammo in self.ammos:
			out += "\n"
			out += "  Ammo "
			out += ammo.output()
		out += "\n"
		out += " NumAccessories:" + self.numAccessories 
		for accessory in self.accessories:
			out += "\n"
			out += "  Accessory "
			out += accessory.output()

		return out

class GameStateInfo():
	def __init__(self):
		self.nickname = ""
 		#<global numNetAct="3" numNetEnt="135" />
		self.numNetActors = 0
		self.numNetEntities = 0

		self.netActors = []
		self.netEntities = []

	def parseNetEntities(self, netEntitiesXMLnode):
		self.numNetEntities = 0
		self.netEntities = []

		for netEntityXMLnode in netEntitiesXMLnode:
			if netEntityXMLnode.tag != "e":
				print "ERROR unknown netEntityXMLnode tag:", netEntityXMLnode.tag
				return False
			netEntity = NetEntity()
			if netEntity.parse(netEntityXMLnode) == True:
				self.numNetEntities += 1
				self.netEntities.append(netEntity)
			else:
				print "ERROR parsing NetEntities"
				return False;

		return True

	def parseNetActors(self, netActorsXMLnode):
		self.numNetActors = 0
		self.netActors = []

		for netActorXMLnode in netActorsXMLnode:
			if netActorXMLnode.tag != "a":
				print "ERROR unknown netActorXMLnode tag:", netActorXMLnode.tag
				return False
			netActor = NetActor()
			if netActor.parse(netActorXMLnode) == True:
				self.numNetActors += 1
				self.netActors.append(netActor)
			else:
				print "ERROR parsing NetActors"
				return False;

		return True

	def parseGlobal(self, globalXMLnode):
		# <global numNetAct="3" numNetEnt="135" />
		self.numNetActors = globalXMLnode.get("numNetAct")
		self.numNetEntities = globalXMLnode.get("numNetEnt")
		return True

	def parse(self, nickname, gameStateXML):
		self.nickname = nickname

		self.numNetEntities = 0
		self.numNetActors = 0

		self.netEntities = []
		self.netActors = []

		for gameStateNode in gameStateXML:
			if gameStateNode.tag == "net_entities":
				if self.parseNetEntities(gameStateNode) == False:
					print "ERROR parsing NetEntities"
					return False
			elif gameStateNode.tag == "net_actors":
				if self.parseNetActors(gameStateNode) == False:
					print "ERROR parsing NetActors"
					return False
			elif gameStateNode.tag == "global":
				if self.parseGlobal(gameStateNode) == False:
					print "ERROR parsing global"
					return False
			else:
				print "ERROR unknown nodeTag:", gameStateNode.tag
				return False

		return True

	def output(self):
		out = "\n"
		out += "nickaname:" + self.nickname + "\n"
		out += "NumNetEntities:" + self.numNetEntities + "\n"
		out += "numNetActors:" + self.numNetActors + "\n"
		out += "NetEntities" + "\n"
		for netEntity in self.netEntities:
			out += netEntity.output()
			out += "\n"
		out += "NetActors" + "\n"
		for netActor in self.netActors:
			out += netActor.output()
			out += "\n"
		out += "\n"
		return out

