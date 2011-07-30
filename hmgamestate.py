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

	def compare(self, rhs):
		result = ""
		if self.name != rhs.name:
			result += "name is different"
 			result += " LHS:"
			result += self.name
 			result += " RHS:"
			result += rhs.name
			result += "\n"
			return [False, result]
		return [True, result]

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
		self.posTolerances = [float(0.1), float(0.1), float(1.0)]
		self.orientTolerances = [float(0.1), float(0.1), float(1.0), float(2.0)]

	def parse(self, netEntityXMLnode):
		#<e AHI="010" C="BasicEntity" CC="1" F="0x0" N="rocket_cin2_4" NI="127" ORI="0.72,-0.19,0.64,0.18" P="" POS="525.0,554.5,40.3">
			#<c N="Particle_rocket_d" />
		#</e>
		ahi = netEntityXMLnode.get("AHI")
		self.active = ahi[0:1]
		self.hidden = ahi[1:2]
		self.invisible = ahi[2:3]
		self.className = netEntityXMLnode.get("C")
		self.numChildren = netEntityXMLnode.get("CC")
		self.flags = netEntityXMLnode.get("F")
		self.name = netEntityXMLnode.get("N")
		self.netID = netEntityXMLnode.get("NI")
		orient = netEntityXMLnode.get("ORI")
		orientList = orient.split(",")
		self.orient = [float(orientList[0]), float(orientList[1]), float(orientList[2]), float(orientList[3])]
		pos = netEntityXMLnode.get("POS")
		posList = pos.split(",")
		self.pos = [float(posList[0]), float(posList[1]), float(posList[2])]
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
		out += " NetID:" + str(self.netID)
		out += " ClassName:" + self.className
		out += " Pos:" + str(self.pos[0]) + ", " + str(self.pos[1]) + ", " + str(self.pos[2])
		out += " Orient:" + str(self.orient[0]) + ", " + str(self.orient[1]) + ", " + str(self.orient[2]) + ", " + str(self.orient[3])
		out += " Active:" + str(self.active)
		out += " Hidden:" + str(self.hidden)
		out += " Invisible:" + str(self.invisible)
		out += " Flags:" + str(self.flags)
		out += "\n"
		out += " NumChildren:" + str(self.numChildren)
		for child in self.children:
			out += "\n"
			out += "  Child "
			out += child.output()
		return out

	def compare(self, rhs):
		result = ""
		if self.name != rhs.name:
			result += "name is different"
 			result += " LHS:"
			result += self.name
 			result += " RHS:"
			result += rhs.name
			result += "\n"
			return [False, result]
		if self.netID != rhs.netID:
			result += "netID is different"
 			result += " LHS:"
			result += self.netID
 			result += " RHS:"
			result += rhs.netID
			result += "\n"
			return [False, result]
		if self.className != rhs.className:
			result += "className is different"
 			result += " LHS:"
			result += self.className
 			result += " RHS:"
			result += rhs.className
			result += "\n"
			return [False, result]
		if self.active != rhs.active:
			result += "active is different"
 			result += " LHS:"
			result += self.active
 			result += " RHS:"
			result += rhs.active
			result += "\n"
			return [False, result]
		if self.hidden != rhs.hidden:
			result += "hidden is different"
 			result += " LHS:"
			result += self.hidden
 			result += " RHS:"
			result += rhs.hidden
			result += "\n"
			return [False, result]
		if self.invisible != rhs.invisible:
			result += "invisible is different"
 			result += " LHS:"
			result += self.invisible
 			result += " RHS:"
			result += rhs.invisible
			result += "\n"
			return [False, result]
		if self.flags != rhs.flags:
			result += "flags is different"
 			result += " LHS:"
			result += self.flags
 			result += " RHS:"
			result += rhs.flags
			result += "\n"
			return [False, result]
		valueTolerances = self.posTolerances
		valueNames = ["X pos", "Y pos", "Z pos"]
		for i in range(3):
			valueLHS = self.pos[i]
			valueRHS = rhs.pos[i]
			if abs(valueLHS - valueRHS) > valueTolerances[i]:
				result += valueNames[i]
				result += " is different"
				result += " LHS:"
				result += str(valueLHS)
				result += " RHS:"
				result += str(valueRHS)
				result += " Delta:" + str(abs(valueLHS - valueRHS))
				result += "\n"
				return [False, result]
		valueTolerances = self.orientTolerances
		valueNames = ["X orient", "Y orient", "Z orient", "W orient"]
		for i in range(4):
			valueLHS = self.orient[i]
			valueRHS = rhs.orient[i]
			if abs(valueLHS - valueRHS) > valueTolerances[i]:
				result += valueNames[i]
				result += " is different"
				result += " LHS:"
				result += str(valueLHS)
				result += " RHS:"
				result += str(valueRHS)
				result += " Delta:" + str(abs(valueLHS - valueRHS))
				result += "\n"
				return [False, result]
		if self.numChildren != rhs.numChildren:
			result += "numChildren is different"
 			result += " LHS:"
			result += self.numChildren
 			result += " RHS:"
			result += rhs.numChildren
			result += "\n"
			return [False, result]

		i = 0
		for childLHS in self.children:
			childRHS = rhs.children[i]
			res = childLHS.compare(childRHS)
			i += 1
			if res[0] == False:
				result += "\n"
				result += "Child[" + i + "] is different"
				result += "\n"
				result += "#### "
				result += res[1]
	 			result += "LHS:"
				result += "\n"
				result += childLHS.output()
				result += "\n"
	 			result += "RHS:"
				result += "\n"
				result += childRHS.output()
				result += "\n"
				return [False, result]

		return [True, result]

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

	def compare(self, rhs):
		result = ""
		if self.netID != rhs.netID:
			result += "netID is different"
 			result += " LHS:"
			result += self.netID
 			result += " RHS:"
			result += rhs.netID
			result += "\n"
			return [False, result]
		return [True, result]

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

	def compare(self, rhs):
		result = ""
		if self.name != rhs.name:
			result += "name is different"
 			result += " LHS:"
			result += self.name
 			result += " RHS:"
			result += rhs.name
			result += "\n"
			return [False, result]
		if self.count != rhs.count:
			result += "count is different"
 			result += " LHS:"
			result += self.count
 			result += " RHS:"
			result += rhs.count
			result += "\n"
			return [False, result]
		return [True, result]

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

	def compare(self, rhs):
		result = ""
		if self.name != rhs.name:
			result += "name is different"
 			result += " LHS:"
			result += self.name
 			result += " RHS:"
			result += rhs.name
			result += "\n"
			return [False, result]
		return [True, result]

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

	def compare(self, rhs):
		result = ""
		if self.name != rhs.name:
			result += "name is different"
 			result += " LHS:"
			result += self.name
 			result += " RHS:"
			result += rhs.name
			result += "\n"
			return [False, result]
		if self.netID != rhs.netID:
			result += "netID is different"
 			result += " LHS:"
			result += self.netID
 			result += " RHS:"
			result += rhs.netID
			result += "\n"
			return [False, result]
		if self.armour != rhs.armour:
			result += "armour is different"
 			result += " LHS:"
			result += self.armour
 			result += " RHS:"
			result += rhs.armour
			result += "\n"
			return [False, result]
		if self.maxArmour != rhs.maxArmour:
			result += "maxArmour is different"
 			result += " LHS:"
			result += self.maxArmour
 			result += " RHS:"
			result += rhs.maxArmour
			result += "\n"
			return [False, result]
		if self.health != rhs.health:
			result += "health is different"
 			result += " LHS:"
			result += self.health
 			result += " RHS:"
			result += rhs.health
			result += "\n"
			return [False, result]
		if self.maxHealth != rhs.maxHealth:
			result += "maxHealth is different"
 			result += " LHS:"
			result += self.maxHealth
 			result += " RHS:"
			result += rhs.maxHealth
			result += "\n"
			return [False, result]
		if self.currentItem != rhs.currentItem:
			result += "currentItem is different"
 			result += " LHS:"
			result += self.currentItem
 			result += " RHS:"
			result += rhs.currentItem
			result += "\n"
			return [False, result]
		if self.dead != rhs.dead:
			result += "dead is different"
 			result += " LHS:"
			result += self.dead
 			result += " RHS:"
			result += rhs.dead
			result += "\n"
			return [False, result]

		if self.dead != rhs.dead:
			result += "dead is different"
 			result += " LHS:"
			result += self.dead
 			result += " RHS:"
			result += rhs.dead
			result += "\n"
			return [False, result]

		if self.numItems != rhs.numItems:
			result += "numItems is different"
 			result += " LHS:"
			result += self.numItems
 			result += " RHS:"
			result += rhs.numItems
			result += "\n"
			return [False, result]
		i = 0
		for itemLHS in self.items:
			itemRHS = rhs.items[i]
			res = itemLHS.compare(itemRHS)
			i += 1
			if res[0] == False:
				result += "\n"
				result += "Item[" + i + "] is different"
				result += "\n"
				result += "#### "
				result += res[1]
	 			result += "LHS:"
				result += "\n"
				result += itemLHS.output()
				result += "\n"
	 			result += "RHS:"
				result += "\n"
				result += itemRHS.output()
				result += "\n"
				return [False, result]

		if self.numAmmos != rhs.numAmmos:
			result += "numAmmos is different"
 			result += " LHS:"
			result += self.numAmmos
 			result += " RHS:"
			result += rhs.numAmmos
			result += "\n"
			return [False, result]
		i = 0
		for ammoLHS in self.ammos:
			ammoRHS = rhs.ammos[i]
			res = ammoLHS.compare(ammoRHS)
			i += 1
			if res[0] == False:
				result += "\n"
				result += "Ammo[" + str(i) + "] is different"
				result += "\n"
				result += "#### "
				result += res[1]
	 			result += "LHS:"
				result += "\n"
				result += ammoLHS.output()
				result += "\n"
	 			result += "RHS:"
				result += "\n"
				result += ammoRHS.output()
				result += "\n"
				return [False, result]

		if self.numAccessories != rhs.numAccessories:
			result += "numAccessories is different"
 			result += " LHS:"
			result += self.numAccessories
 			result += " RHS:"
			result += rhs.numAccessories
			result += "\n"
			return [False, result]
		i = 0
		for accessoryLHS in self.accessories:
			accessoryRHS = rhs.accessories[i]
			res = accessoryLHS.compare(accessoryRHS)
			i += 1
			if res[0] == False:
				result += "\n"
				result += "Accessory[" + i + "] is different"
				result += "\n"
				result += "#### "
				result += res[1]
	 			result += "LHS:"
				result += "\n"
				result += accessoryLHS.output()
				result += "\n"
	 			result += "RHS:"
				result += "\n"
				result += accessoryRHS.output()
				result += "\n"
				return [False, result]

		return [True, result]

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
		out += "nickname:" + self.nickname + "\n"
		out += "numNetEntities:" + self.numNetEntities + "\n"
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

	def compare(self, rhs):
		result = "Comparing:" + self.nickname + " and " + rhs.nickname
		if self.numNetEntities != rhs.numNetEntities:
			result += "\n"
			result += "NumNetEntiies is different"
	 		result += " LHS:" + str(self.numNetEntities)
	 		result += " RHS:" + str(rhs.numNetEntities)
			result += "\n"
			return [False, result]
		if self.numNetActors != rhs.numNetActors:
			result += "\n"
			result += "NumNetActors is different"
	 		result += " LHS:" + str(self.numNetActors)
	 		result += " RHS:" + str(rhs.numNetActors)
			result += "\n"
			return [False, result]
		for netEntity in self.netEntities:
			netID = netEntity.netID
			netEntityRHS = None
			for netEntityOther in rhs.netEntities:
				if netEntityOther.netID == netID:
					netEntityRHS = netEntityOther
					break
			if netEntityRHS == None:
				result += "\n"
				result += "LHS NetEntity not found netID:" + netID
				result += "\n"
				result += netEntity.output()
				result += "\n"
				return [False, result]

			res = netEntity.compare(netEntityRHS)
			if res[0] == False:
				result += "\n"
				result += "NetEntity:" + netEntity.name + " and " + netEntityRHS.name + " are different"
				result += "\n"
				result += "#### "
				result += res[1]
	 			result += "LHS:"
				result += "\n"
				result += netEntity.output()
				result += "\n"
	 			result += "RHS:"
				result += "\n"
				result += netEntityRHS.output()
				result += "\n"
				return [False, result]

		for netActor in self.netActors:
			netID = netActor.netID
			netActorRHS = None
			for netActorOther in rhs.netActors:
				if netActorOther.netID == netID:
					netActorRHS = netActorOther
					break
			if netActorRHS == None:
				result += "\n"
				result += "LHS NetActor not found netID:" + netID
				result += "\n"
				result += netActor.output()
				result += "\n"
				return [False, result]

			res = netActor.compare(netActorRHS)
			if res[0] == False:
				result += "\n"
				result += "NetActor:" + netActor.name + " and " + netActorRHS.name + " are different"
				result += "\n"
				result += "#### "
				result += res[1]
	 			result += self.nickname + " LHS:"
				result += "\n"
				result += netActor.output()
				result += "\n"
	 			result += rhs.nickname + " RHS:"
				result += "\n"
				result += netActorRHS.output()
				result += "\n"
				return [False, result]
			
		result = self.nickname + " MATCHES " + rhs.nickname
		return [True, result]

