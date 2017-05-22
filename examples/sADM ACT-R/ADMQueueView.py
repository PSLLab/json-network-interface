from textInRect import TextInRect
import datetime
from psychopy import core

class ADMQueueView:
	NUMBER_OF_OBJECT_SLOTS = 20
	def __init__(self, win, pos = (0,0), block_num = 0):
		self.win = win
		self.objectViews = []
		self.queue = None
		self.block_num = block_num
		self.selected_objectView = TextInRect(win, font = 'Courier', fillColor = 'black', width = 230, height = 24, pos = (pos[0], pos[1]), lineColor = 'gray', text = '', textColor = 'white')
		self.selected_object = None
		for i in range(0, self.NUMBER_OF_OBJECT_SLOTS):
			self.objectViews.append(TextInRect(win, font = 'Courier', fillColor = 'black', width = 230, height = 24, pos = (pos[0], pos[1] - (23 * (i+2))), lineColor = 'gray', text = '', textColor = 'white'))


	def draw(self):
		if self.queue == None:
			raise Exception('queue not initialized for ADMQueueView')
		update_time = core.getTime()
		#create boxes
		self.queueViewClear()
		for object_view in self.objectViews:
			object_view.draw()
		#check if more objects than boxes
		if len(self.queue.queue_objects) > self.NUMBER_OF_OBJECT_SLOTS:
			raise Exception('more objects than slots to display them in queue')
		#create text for the selected object
		self.selected_objectView.lineColor = 'gray'
		self.selected_objectView.text_stim.text = ''
		if self.queue.selected_object <> None: #creates and highlights selected object display
			self.selected_objectView.lineColor = 'white'
			time_delta = update_time - self.queue.selected_object.arrival_time
			timer = ''
			if time_delta < 10:
				timer += '00' + str(int(time_delta))
			elif time_delta < 100:
				timer += '0' + str(int(time_delta))
			else:
				timer += str(int(time_delta))
			if self.queue.selected_object.deadline < 100:
				deadline = '0' + str(self.queue.selected_object.deadline)
			else:
				deadline = str(self.queue.selected_object.deadline)
			self.selected_objectView.text_stim.text = self.queue.selected_object.obj_name + ' ' + timer + "/"+deadline+' '+str(self.queue.selected_object.points)
			if self.queue.selected_object.priority != 'None':
				if self.queue.selected_object.priority == 1:
					self.selected_objectView.text_stim.color = 'green'
				elif self.queue.selected_object.priority == 2:
					self.selected_objectView.text_stim.color = 'yellow'
				elif self.queue.selected_object.priority == 3:
					self.selected_objectView.text_stim.color = 'red'
				elif self.queue.selected_object.priority == -1:
					self.selected_objectView.text_stim.color = 'white'
		self.selected_objectView.draw()
	
                #reset all objectviews to gray boxes
                for i, object in enumerate(self.objectViews):
                        self.objectViews[i].lineColor = 'gray'
                        self.objectViews[i].text_stim.text = ''
                #create text for each object in the queue
                for i, object in enumerate(self.queue.queue_objects):
                        # for each object view update arrival time count and priority and draw
                        time_delta = update_time - self.queue.queue_objects[i].arrival_time
                        timer = ''
                        if time_delta < 10:
                                timer += '00' + str(int(time_delta))
                        elif time_delta < 100:
                                timer += '0' + str(int(time_delta))
                        else:
                                timer += str(int(time_delta))
                        if self.queue.queue_objects[i].deadline < 100:
                                deadline = '0' + str(self.queue.queue_objects[i].deadline)
                        else:
                                deadline = str(self.queue.queue_objects[i].deadline)
                        self.objectViews[i].text_stim.text = self.queue.queue_objects[i].obj_name + ' ' + timer + "/"+deadline+' '+str(self.queue.queue_objects[i].points)
                        if self.queue.queue_objects[i].priority != 'None':
                                if self.queue.queue_objects[i].priority == 1:
                                        self.objectViews[i].text_stim.color = 'green'
                                elif self.queue.queue_objects[i].priority == 2:
                                        self.objectViews[i].text_stim.color = 'yellow'
                                elif self.queue.queue_objects[i].priority == 3:
                                        self.objectViews[i].text_stim.color = 'red'
                                elif self.queue.queue_objects[i].priority == -1:
                                        self.objectViews[i].text_stim.color = 'white'
                        self.objectViews[i].draw()

                # draw highlighted object last so that white border shows up on all sides
                if self.queue.highlighted_object != None and self.queue.selected_object == None: #highlighted object is in main queue
                        self.objectViews[self.queue.queue_objects.index(self.queue.highlighted_object)].lineColor = 'white'
                        self.objectViews[self.queue.queue_objects.index(self.queue.highlighted_object)].draw()

	def queueViewClear(self):
		for i in range(0, self.NUMBER_OF_OBJECT_SLOTS):
			self.objectViews[i].text_stim.text = ""
			self.objectViews[i].text_stim.color = "white"
		self.selected_objectView.text_stim.text = ""
		self.objectViews[i].text_stim.color = "white"

