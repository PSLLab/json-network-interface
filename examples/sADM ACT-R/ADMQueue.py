from ADMObject import ADMObject
import csv, random
from psychopy import core

class ADMQueue:
	def __init__(self, filename, performance):
		self.waiting_objects = []
		self.queue_objects = []
		self.completed_objects = []
		self.selected_object = None
		self.highlighted_object = None
		self.performance = performance
		self.paused = False
		self.pause_start = None
		# read file and init objects
		with open(filename, 'rU') as csvfile:
			reader = csv.reader(csvfile)
			reader.next()
			for row in reader:
				self.waiting_objects.append(ADMObject(color = row[0], shape = row[1], size = row[2], final_level = row [9], obj_number = row[10], obj_name = row[11], interrupt_level = row[14]))

	def empty(self):
		if len(self.queue_objects) == 0:
			return True
		else:
			return False

	def clearHighlight(self):
		self.highlighted_object = None

	def addObject(self):
		new_object = self.waiting_objects.pop(0)
		new_object.arrival_time = core.getTime()
		new_object.addedinqueue = core.getTime()
		self.queue_objects.append(new_object)
		self.sortQueue()
		self.highlighted_object = None
		self.performance.logMessage('Arrival\t{}\t{}\t{}\t{}' .format(new_object.obj_name, new_object.obj_number, new_object.points, new_object.deadline))
		return new_object

	def addSelectedObject(self): #puts back selected object into queue
		self.selected_object.addedinqueue = core.getTime()
		self.queue_objects.append(self.selected_object)
		self.selected_object = None
		self.sortQueue()

	def sortedObject(self, object):
		self.completed_objects.append(object)
		self.highlighted_object = None
		self.selected_object = None

	def checkFinalLevel(self,object, currentlevel):
		if object.final_level == str(currentlevel):
			return True
		else:
			return False
		
	def selectObject(self):
		if self.highlighted_object == None:
			raise Exception('can not select an object when no object is highlighted')
		self.selected_object = self.highlighted_object
		self.queue_objects.pop(self.queue_objects.index(self.selected_object))
		return self.selected_object

	def makeActive(self, selected_object):
		if selected_object == None:
			if len(self.queue_objects) >  0:
				self.highlighted_object = self.queue_objects[0]
			else:
				raise Exception('there are no objects in the queue to highlight')

	def moveSelectionUp(self):
		if self.highlighted_object == None:
			raise Exception('should not be able to move up in queue without having an object highlighted')
		current_position = self.queue_objects.index(self.highlighted_object)
		if current_position > 0:
			self.highlighted_object = self.queue_objects[current_position - 1]

	def moveSelectionDown(self):
		if self.highlighted_object == None:
			raise Exception('should not be able to move up in queue without having an object highlighted')
		current_position = self.queue_objects.index(self.highlighted_object)
		if current_position < (len(self.queue_objects) - 1):
			self.highlighted_object = self.queue_objects[current_position + 1]

	def sortQueue(self):
		if len(self.queue_objects) > 1:
			self.queue_objects.sort(key = lambda object: object.addedinqueue, reverse = True)
			self.queue_objects.sort(key = lambda object: object.priority, reverse = True)

	def calculateSortPenalty(self, obj):
		score = obj.points - (obj.points * int((core.getTime()-obj.arrival_time)/obj.deadline))
		return score

	def calculatePenaltyPoints(self):
		penaltyscore = 0
		for object in self.queue_objects:
			if self.calculateSortPenalty(object) < 0:
				penaltyscore += self.calculateSortPenalty(object)
		if self.selected_object <> None:
			if self.calculateSortPenalty(self.selected_object) < 0:
				penaltyscore += self.calculateSortPenalty(self.selected_object)
		return penaltyscore*-1
		

	def getPoints(self, obj):
		return obj.points

	def getLength(self):
		return len(self.queue_objects)

	def checkAddObject(self):
		temp = random.randint(1,100)
		if self.getLength()<5:
			return True
		elif self.getLength()<10 and temp > 85:
			return True
		elif self.getLength()<16 and temp > 75:
			return True
		else:
			return False
			
	def writeQueue(self, subject, block):
		tempqueue = []
		for object in self.waiting_objects:
			tempqueue.append(object)
		for object in self.queue_objects:
			tempqueue.append(object)
		for object in self.completed_objects:
			tempqueue.append(object)
		if self.selected_object <> None:
			tempqueue.append(self.selected_object)
		tempqueue.sort(key = lambda object: int(object.obj_number))
		outfile2=open(str(subject)+"-ADM-Block"+str(block)+" ObjectList.txt", 'w')
		outfile2.write("Subject\tObjectNumber\tObjectName\tColor\tShape\tSize\tPitch\tInstrument\tTempo\tTexture\tMaterial\tConsistency\tFinalLevel\tInterruptRequired\tInterruptLevel\tPoints\tDeadline\n")
		for object in tempqueue:
			outfile2.write(str(subject)+"\t"+object.obj_number+"\t"+object.obj_name+"\t"+object.color+"\t"+object.shape+"\t"+object.size+"\t"+object.pitch+"\t"+object.instrument+"\t"+object.tempo+"\t"+object.texture+"\t"+object.material+"\t"+object.consistency+"\t"+object.final_level+"\t")
			if object.interrupt_level <> 0:
				outfile2.write("1")
			else:
				outfile2.write("0")
			outfile2.write("\t"+str(object.interrupt_level)+"\t"+str(object.points)+"\t"+str(object.deadline)+"\n")
		outfile2.close()
		

