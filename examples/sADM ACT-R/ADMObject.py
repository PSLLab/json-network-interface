import random
from psychopy import core

class ADMObject:
	def __init__(self, color, shape, size, final_level, obj_number, obj_name, interrupt_level):
		self.color = color
		self.shape = shape
		self.size = size
		self.obj_number = obj_number
		self.obj_name = obj_name
		self.interrupt_level = int(interrupt_level)
		self.final_level = final_level

		temp = random.randint(0,3)
		if temp == 0:
			self.pitch = "High"
			self.instrument = "Horn"
			self.tempo = "Slow"
		elif temp == 1:
			self.pitch = "Low"
			self.instrument = "Horn"
			self.tempo = "Fast"
		elif temp == 2:
			self.pitch = "Low"
			self.instrument = "Flute"
			self.tempo = "Slow"
		elif temp == 3:
			self.pitch = "High"
			self.instrument = "Flute"
			self.tempo = "Fast"

		temp = random.randint(0,3)
		if temp == 0:
			self.texture = "Rough"
			self.material = "Rock"
			self.consistency = "Solid"
		elif temp == 1:
			self.texture = "Slimy"
			self.material = "Plastic"
			self.consistency = "Solid"
		elif temp == 2:
			self.texture = "Rough"
			self.material = "Plastic"
			self.consistency = "Gooey"
		elif temp == 3:
			self.texture = "Slimy"
			self.material = "Rock"
			self.consistency = "Gooey"

		temp = random.randint(0,1)
		if temp == 0:
			self.points = 100
		elif temp == 1:
			self.points = 200

		temp = random.randint(0,2)
		if temp == 0:
			self.deadline = 60
		elif temp == 1: 
			self.deadline = 120
		elif temp == 2:
			self.deadline = 180

		self.priority = -1
		self.arrival_time = -1
		self.addedinqueue = -1
		self.sorted = 0
		self.currentpointworth = 0
		self.queried_color = False
		self.queried_shape = False
		self.queried_size = False
		self.queried_pitch = False
		self.queried_instrument = False
		self.queried_tempo = False
		self.queried_texture = False
		self.queried_material = False
		self.queried_consistency = False
		self.interrupted = False
		temp = random.uniform(5,20)
		self.interrupt_timer = temp
		self.interruptLvlStart = 0

	def queriesMade(self):
		queries_made = 0
		if self.queried_color:
			queries_made += 1
		if self.queried_shape:
			queries_made += 1
		if self.queried_size:
			queries_made += 1
		if self.queried_pitch:
			queries_made += 1
		if self.queried_instrument:
			queries_made += 1
		if self.queried_tempo:
			queries_made += 1
		if self.queried_texture:
			queries_made += 1
		if self.queried_material:
			queries_made += 1
		if self.queried_consistency:
			queries_made += 1
		return queries_made

	def updateAsInterruption(self):
		temp = random.randint(0,2)
		if temp == 0:
			self.deadline = 20
		elif temp == 1: 
			self.deadline = 40
		elif temp == 2:
			self.deadline = 60
		self.points = 300

	def setPriority(self, priority):
		self.priority = priority

	def updateinterruptLvlStart(self):
		if self.interruptLvlStart == 0:
			self.interruptLvlStart = core.getTime()

