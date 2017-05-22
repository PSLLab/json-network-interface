from psychopy import visual, core, event
from textInRect import TextInRect
from ADMQueueView import ADMQueueView

# assumes window is 1280 x 1024
class ADMView:
	def __init__(self, win, block_num):
		self.win = win
		self.score_box_title = TextInRect(win, fillColor='white', text='Score', textColor = 'teal', height=38, width=230, pos=(-382,309))
		self.score_box = TextInRect(win, fillColor='lightgray', textColor='black', text='0', height=78, width=230, pos=(-382,245))
		self.queue_title = TextInRect(win, fillColor='white', textColor='gray', text='Objects', height=38, width=230, pos=(-382,167))
		self.queue = ADMQueueView(win, pos=(-382, 130), block_num=block_num) # pos is top left of first object in queue



		self.feedback_title = TextInRect(win, fillColor='white', textColor='teal', text='System Messages', height=38, width=673, pos=(100,309))
		self.feedback = TextInRect(win, fillColor='lightgray', textColor='black', text='', textHeight = 18, height=116, width=673, pos=(100,226))

		self.action_menu_title = TextInRect(win, fillColor='white', lineColor = 'lightgray', textColor='gray', text='Select an Action', height=38, width=673, pos=(100,129))


		self.action_menu_select = TextInRect(win, fillColor='lightgray', lineColor = 'lightgray', textColor='gray', text='1 = Select Object', height=75, width=220, pos=(-126,67))
		self.action_menu_query = TextInRect(win, fillColor='lightgray', lineColor = 'lightgray', textColor='gray', text='2 = Query', height=75, width=220, pos=(100,67))
		self.action_menu_sort = TextInRect(win, fillColor='lightgray', lineColor = 'lightgray', textColor='gray', text='3 = Sort', height=75, width=220, pos=(326,67))
		38

		self.select_menu = TextInRect(win, fillColor='lightgray', lineColor = 'lightgray', textColor='gray', text='  1 = Move Up\n  2 = Move Down\n  3 = Select Object\n  4 = Return to Action Menu', textHeight = 16, alignHoriz='left', height=115, width=220, pos=(-126,-10))
		self.query_menu = TextInRect(win, fillColor='lightgray', lineColor = 'lightgray', textColor='gray', text='  1 = Object Color\n  2 = Object Shape\n  3 = Object Size\n  4 = Return to Action Menu', textHeight = 16, alignHoriz='left', height=115, width=220, pos=(100,-10))
		self.sort_menu = TextInRect(win, fillColor='lightgray', lineColor = 'lightgray', textColor='gray', text='  1 = Bin 1\n  2 = Bin 2\n  3 = Bin 3\n  4 = Bin 4', alignHoriz='left', textHeight = 16, height=115, width=220, pos=(326,-10))

		self.priority_title = TextInRect(win, fillColor='white', textColor='navy', text='Assign Priority. 1 object(s) left to prioritize.', height=38, width=673, pos=(100,-106))
		self.priority_object = TextInRect(win, fillColor='lightgray', lineColor = 'lightgray', textColor='black', text='Object:\nPoints:\nDeadline:', textHeight = 18, height=115, width=337, pos=(-68,-188))
		self.priority_menu = TextInRect(win, fillColor='lightgray', lineColor = 'lightgray', textColor='black', text='1. Red\n2. Yellow\n3. Green', textHeight = 18, height=115, width=337, pos=(268,-188))
		self.stim_list = [self.score_box_title, self.score_box, self.query_menu, self.queue_title, self.action_menu_query, self.action_menu_select, self.action_menu_sort, self.action_menu_title, self.priority_menu, self.priority_object, self.priority_title, self.feedback, self.feedback_title, self.select_menu, self.sort_menu] #self.queue,

	def activateActionMenu(self, selected_object, currentlevel):
		self.action_menu_title.setTextColor('black')
		self.action_menu_select.setTextColor('black')
		if selected_object != None:
			self.action_menu_sort.setTextColor('black')
			self.action_menu_query.setTextColor('black')
			self.action_menu_query.setText('2 = Query ' + selected_object.obj_name)
			self.action_menu_sort.setText('3 = Sort ' + selected_object.obj_name)
		else:
			self.action_menu_sort.setTextColor('gray')
			self.action_menu_query.setTextColor('gray')
			self.action_menu_query.setText('2 = Query')
			self.action_menu_sort.setText('3 = Sort')
		self.select_menu.setTextColor('gray')
		self.sort_menu.setTextColor('gray')
		self.query_menu.setTextColor('gray')
		if currentlevel == 1:
			self.query_menu.setText('  1 = Object Color\n  2 = Object Shape\n  3 = Object Size\n  4 = Return to Action Menu')
		elif currentlevel == 2:
			self.query_menu.setText('  1 = Object Pitch\n  2 = Object Instrument\n  3 = Object Tempo\n  4 = Return to Action Menu')
		elif currentlevel == 3:
			self.query_menu.setText('  1 = Object Texture\n  2 = Object Material\n  3 = Object Consistency\n  4 = Return to Action Menu')
		self.queue_title.setTextColor('gray')
		self.priority_title.setText('')
		self.priority_title.fillColor = 'white'
		self.priority_object.setText('')
		self.priority_menu.setText('')

	def activateSelectMenu(self):
		self.action_menu_title.setTextColor('gray')
		self.action_menu_select.setTextColor('gray')
		self.action_menu_sort.setTextColor('gray')
		self.action_menu_query.setTextColor('gray')
		self.select_menu.setTextColor('black')
		self.sort_menu.setTextColor('gray')
		self.query_menu.setTextColor('gray')
		self.queue_title.setTextColor('black')
		self.priority_title.setText('')
		self.priority_title.fillColor = 'white'
		self.priority_object.setText('')
		self.priority_menu.setText('')

	def activateQueryMenu(self):
		self.action_menu_title.setTextColor('gray')
		self.action_menu_select.setTextColor('gray')
		self.action_menu_sort.setTextColor('gray')
		self.action_menu_query.setTextColor('gray')
		self.select_menu.setTextColor('gray')
		self.sort_menu.setTextColor('gray')
		self.query_menu.setTextColor('black')
		self.queue_title.setTextColor('gray')
		self.priority_title.setText('')
		self.priority_title.fillColor = 'white'
		self.priority_object.setText('')
		self.priority_menu.setText('')

	def activateSortMenu(self):
		self.action_menu_title.setTextColor('gray')
		self.action_menu_select.setTextColor('gray')
		self.action_menu_sort.setTextColor('gray')
		self.action_menu_query.setTextColor('gray')
		self.select_menu.setTextColor('gray')
		self.sort_menu.setTextColor('black')
		self.query_menu.setTextColor('gray')
		self.queue_title.setTextColor('gray')
		self.priority_title.setText('')
		self.priority_title.fillColor = 'white'
		self.priority_object.setText('')
		self.priority_menu.setText('')

	def activatePrioritizationMenu(self, prioritize_object, prioritizations):
		self.action_menu_title.setTextColor('gray')
		self.action_menu_select.setTextColor('gray')
		self.action_menu_sort.setTextColor('gray')
		self.action_menu_query.setTextColor('gray')
		self.select_menu.setTextColor('gray')
		self.sort_menu.setTextColor('gray')
		self.query_menu.setTextColor('gray')
		self.queue_title.setTextColor('gray')
		self.priority_title.setText('Assign Priority. '+ prioritizations+' object(s) left to prioritize.')
		self.priority_title.fillColor = 'orangered'
		self.priority_title.setTextColor('black')
		self.priority_object.setText('Object: '+prioritize_object.obj_name+'\nPoints: '+str(prioritize_object.points)+'\nDeadline: '+str(prioritize_object.deadline))
		self.priority_menu.setText('1. Red\n2. Yellow\n3. Green')

	def activateInterruptionMenu(self, interrupt_object):
		self.action_menu_title.setTextColor('gray')
		self.action_menu_select.setTextColor('gray')
		self.action_menu_sort.setTextColor('gray')
		self.action_menu_query.setTextColor('gray')
		self.select_menu.setTextColor('gray')
		self.sort_menu.setTextColor('gray')
		self.query_menu.setTextColor('gray')
		self.queue_title.setTextColor('gray')
		self.priority_title.setText('Switch Object?')
		self.priority_title.fillColor = 'orangered'
		self.priority_title.setTextColor('black')
		self.priority_object.setText('Object: '+interrupt_object.obj_name+'\nPoints: '+str(interrupt_object.points)+'\nDeadline: '+str(interrupt_object.deadline))
		self.priority_menu.setText('1. Prioritize object ' +interrupt_object.obj_name+'\n2. Switch to object ' +interrupt_object.obj_name)

	def activateDelay(self):
		self.action_menu_title.setTextColor('gray')
		self.action_menu_select.setTextColor('gray')
		self.action_menu_sort.setTextColor('gray')
		self.action_menu_query.setTextColor('gray')
		self.select_menu.setTextColor('gray')
		self.sort_menu.setTextColor('gray')
		self.query_menu.setTextColor('gray')
		self.queue_title.setTextColor('gray')

	def activateHelp(self):
		self.score_box_title.setTextColor('gray')

	def draw(self):
		self.score_box.draw()
		self.score_box_title.draw()
		self.queue_title.draw()
		self.queue.draw()
		self.select_menu.draw()
		self.query_menu.draw()
		self.sort_menu.draw()
		self.action_menu_title.draw()
		self.action_menu_select.draw()
		self.action_menu_query.draw()
		self.action_menu_sort.draw()
		self.feedback_title.draw()
		self.feedback.draw()
		self.priority_title.draw()
		self.priority_menu.draw()
		self.priority_object.draw()
