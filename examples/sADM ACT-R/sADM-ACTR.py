import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../lib/python"))

from psychopy import visual, core, event, gui, data
from ADMView import ADMView
from ADMBins import ADMBins
from ADMQueue import ADMQueue
from psychopy.iohub import launchHubServer
from ADMPerformance import ADMPerformance
from ADMFeedback import ADMFeedback
from ADMHighScores import ADMHighScores
import random, time, datetime, os
from psychopy.tools.filetools import fromFile, toFile
from twisted.internet import reactor
from twisted.internet.task import LoopingCall, Cooperator
from actr6_jni import Dispatcher, JNI_Server, VisualChunk, Twisted_MPClock



actr_enabled = True
ADM_VERSION = '5.1'
TOTAL_OBJECTS = 100
INTERRUPT_DELAY = 2

    
class Environment(object):
	if actr_enabled:
		d = Dispatcher()
	STATE_WAIT_CONNECT = -3
    	STATE_WAIT_MODEL = -2
    	STATE_INTRO = -1
    	STATE_RESET = 0
    	STATE_FIXATION = 1
    	STATE_UPDATE = 2
    	STATE_TASK = 3
    	STATE_DONE = 4
	
	def __init__(self, actr=False, subjectID="0", session="0"):
		
		#psychopy
		self.io = launchHubServer()
		self.keyboard = self.io.devices.keyboard
		self.win = visual.Window(size = (1280,1024), units='pix', color='white', colorSpace='rgb', allowGUI=False, screen=0, monitor='testMonitor')
		
		#ADM slide objects
		self.instext = visual.TextStim(self.win, text = "", font = 'Courier Regular', alignHoriz = "center", height = 24, color = 'black', bold = True)
		self.instext.wrapWidth=(922)
		self.nextslidetext = visual.TextStim(self.win, text = "", pos = (0,-307), font = 'Courier Regular', height = 24, color = 'black', bold = True) 
		self.nextslidetext.wrapWidth=(922)
		self.bintext = visual.TextStim(self.win, text = "", pos = (0,125), font = 'Courier Regular', height = 24, color = 'black', bold = True)
		self.attrib1 = visual.TextStim(self.win, text = "", pos = (0,75), font = 'Courier Regular', height = 24, color = 'black', bold = True)
		self.attrib2 = visual.TextStim(self.win, text = "", pos = (0,25), font = 'Courier Regular', height = 24, color = 'black', bold = True)
		self.attrib3 = visual.TextStim(self.win, text = "", pos = (0,-25), font = 'Courier Regular', height = 24, color = 'black', bold = True)
		self.attrib4 = visual.TextStim(self.win, text = "", pos = (0,-75), font = 'Courier Regular', height = 24, color = 'black', bold = True)
		self.keyboard_events = []
		self.coach = False #True runs the coaching program
		
		#ADM variables
		self.subjectID = subjectID
		self.session = session
		if int(self.session) == 1:
			self.blocks = ['Practice',1,2,3,4,5]
			self.object_file_list = ['PracticeObjects.csv','Block1.csv','Block2.csv','Block3.csv','Block4.csv','Block5.csv']
		elif int(self.session) == 2:
			self.blocks = [6,7,8,9,10,11,12]
			self.object_file_list = ['Block6.csv','Block7.csv','Block8.csv','Block9.csv','Block10.csv','Block11.csv','Block12.csv']
		elif int(self.session) == 3:
			self.blocks = [13,14,15,16,17,18,19]
			self.object_file_list = ['Block13.csv','Block14.csv','Block15.csv','Block16.csv','Block17.csv','Block18.csv','Block19.csv']
		self.highscores = ADMHighScores()
		self.sessionscore = 0
		
		#json
		self.state = self.STATE_INTRO
		self.actr = actr
		self.actr_time_lock = False
		if self.actr:
			self.state = self.STATE_WAIT_CONNECT
			self.actr = JNI_Server(self, clock=Twisted_MPClock())
			self.actr.addDispatcher(self.d)
			reactor.listenTCP(5555, self.actr)

		self.lc1 = LoopingCall(self.update_env)
		self.lc1.start(1.0 / 30)

		self.coop = Cooperator()
		self.coop.coiterate(self.process_event())
		
	def reset(self):
        	pass

	def draw_actr_wait_connect(self):
		self.instext.text = "Waiting for ACT-R to connect..."
		self.instext.draw()
		self.win.flip()

	def draw_actr_wait_model(self):
		self.instext.text = "Waiting for ACT-R model"
		self.instext.draw()
		self.win.flip()

	def draw_breakslide(self, block_num):
		if int(self.session) <> 1:
			highscores.readHighScores(self.subjectID)
		
			if self.object_file_list[block_num] == 'PracticeObjects.csv':
				self.instext.setText("You will now practice sorting objects.")
			elif self.object_file_list[block_num] == 'Block1.csv':
				self.instext.setText("You will now begin the sorting task.\n\nFinally, you can earn up to a $20 performance bonus in Session 3 based on how well you do. This bonus is on top of the $$ payment you will receive for attending the third session and for completing all sessions. By trying your best in this session and the next, you can learn how to maximize your score, which will help maximize your bonus in the final session. Please try your best now, so that you can improve your odds of scoring the highest points possible in Session 3.")
			elif self.object_file_list[block_num] == 'Block6.csv':
				self.instext.setText("You will now begin the sorting task.\n\nRemember, you can earn a performance bonus in Session 3 up to $20. By trying your best in the current session, you will gain practice that will help you to do well in Session 3. Please try your best so that you can improve your odds of scoring the highest points possible in Session 3.")
			elif self.object_file_list[block_num] == 'Block13.csv':
				self.instext.setText("You will now begin the sorting task.\n\nYou can earn up to $20 in this session based on your performance, beyond the $$ you will receive for attending this session and completing all sessions. Your bonus is based on how well you do across all blocks. Once you begin sorting, all points gained or lost througout the entire session will factor into how big your performance bonus will be. Please try your best so that you can improve your odds of scoring the highest points possible in Session 3.")
			else:
				self.instext.setText("Please take a short break.")
			self.instext.pos = (0,0)
			self.instext.draw()
			self.nextslidetext.setText("Press the spacebar when you are ready to continue the task.")
			self.nextslidetext.draw()
			self.win.flip()
			key = event.getKeys()
			while True:
				while len(key) == 0:
					key = event.getKeys()
					reactor.iterate()
				if key[0] in {'space'}:
					break
	
		
	def update_env(self): #based on state, update display
		if self.state == self.STATE_WAIT_CONNECT:
			self.draw_actr_wait_connect()
		if self.state == self.STATE_WAIT_MODEL:
			self.draw_actr_wait_model()
		if self.state == self.STATE_INTRO:
			while len(event.getKeys()) == 0:
		        	reactor.iterate()
			self.state = self.STATE_TASK
		if self.state == self.STATE_RESET:
			self.reset()
			self.state = self.STATE_TASK
		if self.state == self.STATE_TASK:
			for block_num, object_file_name in enumerate(self.object_file_list):
				#self.draw_breakslide(block_num)
				self.draw_ADM(block_num, object_file_name)
			self.draw_session_end


	def handle_key_press(self, code, key):
		event._onPygletKey(code, 0)

	def process_event(self):
		yield

	def setDefaultClock(self):
		self.lc1.stop()
		self.lc1.clock = reactor
		self.lc1.start(1.0 / 30)

	if actr_enabled:

		@d.listen('connectionMade')
		def ACTR6_JNI_Event(self, model, params):
			self.state = self.STATE_WAIT_MODEL
			self.actr.setup(self.win.size[0], self.win.size[1])

		@d.listen('connectionLost')
		def ACTR6_JNI_Event(self, model, params):
			self.setDefaultClock()
			self.state = self.STATE_WAIT_CONNECT

		@d.listen('reset')
		def ACTR6_JNI_Event(self, model, params):
			self.actr_time_lock = params['time-lock']
			self.setDefaultClock()
			self.state = self.STATE_WAIT_MODEL

		@d.listen('model-run')
		def ACTR6_JNI_Event(self, model, params):
			if not params['resume']:
				self.state = self.STATE_INTRO
				self.draw_intro()
				self.actr_running = True
		    	if self.actr_time_lock:
				self.lc1.stop()
				self.lc1.clock = self.actr.clock
				self.lc1.start(1.0 / 30)

		@d.listen('model-stop')
		def ACTR6_JNI_Event(self, model, params):
			pass

		@d.listen('keydown')
		def ACTR6_JNI_Event(self, model, params):
			self.handle_key_press(params['keycode'], chr(params['keycode']))

		@d.listen('mousemotion')
		def ACTR6_JNI_Event(self, model, params):
			pass

		@d.listen('mousedown')
		def ACTR6_JNI_Event(self, model, params):
			pass



###############main########################

	def draw_ADM_main(self, block_num, object_file_name):

		currenttime = 0
		self.win.color = 'black'
		self.win.flip()
		view = ADMView(self.win, blocks[block_num])
		bins = ADMBins('Bins.csv')
		starttime = core.getTime()
		performance = ADMPerformance('{}_ADM_Block{}.txt'.format(self.subjectID, blocks[block_num]), view.score_box, starttime)
		queue = ADMQueue(object_file_name, performance)
		feedback = ADMFeedback(view.feedback)
		current_menu = "action menu"
		selected_object = None
		prioritize_object = None
		currentlevel = 1
		view.activateActionMenu(selected_object, currentlevel)
		view.queue.queue = queue
		view.draw()
		win.flip()
		currentgoal = ""
		prioritizations = 0
		interruptTimer = 0
		blockduration = 600 #seconds
		interruptionselection = False 
		keyboard.getPresses(clear = True) # clears previous keyboard presses for later keyboard.getpresses function calls
	
		if self.object_file_list[block_num] == 'PracticeObjects.csv':
			blockduration = 1200
		while core.getTime() < starttime + blockduration: 
			feedback.checkExpiration()
			if queue.empty() and selected_object == None:
				arriving_object = queue.addObject()
				current_menu = 'prioritization menu'
				prioritizations = random.randint(1,3)
				view.activatePrioritizationMenu(arriving_object, str(prioritizations))
				performance.logMessage('Screen\tPriorityMenu')
				prioritize_object = arriving_object
				arriving_object = None
				currentgoal = "PRIORITIZE_OBJECT"
			if self.object_file_list[block_num] == 'PracticeObjects.csv' and len(queue.completed_objects) == 3:
				break
			if self.object_file_list[block_num] == 'PracticeObjects.csv' and core.getTime() > starttime + 240: #if haven't sorted 3 objects in 4 minutes, experimenter intervention
				view.activateHelp()
			if len(queue.completed_objects) >= TOTAL_OBJECTS:
				# this test is to make sure that queued key presses do not take us beyond the end of the ADM task
				break


			if selected_object <> None: #check for interruption
				if selected_object.interrupt_level == currentlevel and current_menu <> 'prioritization menu' and current_menu <> 'interruption menu': #needed so interrupt timer for interruptions starts after interruption has been dealt with
					selected_object.updateinterruptLvlStart()
				if selected_object.interrupt_level == currentlevel and (core.getTime() > (selected_object.interruptLvlStart + selected_object.interrupt_timer)) and selected_object.interrupted == False:
					current_menu = 'delay'
					interruptTimer = core.getTime() + INTERRUPT_DELAY
					selected_object.interrupted = True
			if current_menu == 'delay':
				view.activateDelay()
				performance.logMessage('Screen\tInterruptDelay')
				for i in range(INTERRUPT_DELAY, 0, -1):
					feedback.addFeedbackItem('Object arriving in: 00{}'.format(i), '3')
					view.draw()
					self.win.flip()
					core.wait(1)
				keyboard.getPresses(clear = True)
				keyboard_events = []
				current_menu = 'interruption menu'
				performance.logMessage('Screen\tInterruptMenu')
				arriving_object = queue.addObject()
				feedback.addFeedbackItem('Arrival object is: {}'.format(arriving_object.obj_name), '3')
				arriving_object.updateAsInterruption()
				view.activateInterruptionMenu(arriving_object)
				
			keyboard_events.append(keyboard.getPresses(chars=['1', u'1', '2',u'2', '3',u'3', '4',u'4', '0'],clear = True))
			reactor.iterate()
			for keypress in keyboard_events[0]:
				# escape key sequence for debugging
				if keypress == '0': #add back in '0' if escape key allowed
					print 'quitting because of escape'
					performance.flushLog()
					core.quit()
					break
				# menu interactions
				if current_menu == 'prioritization menu':
					if keypress == '1' or keypress == u'1':#high
						prioritize_object.setPriority(3) 
						performance.logMessage('PriorityMenu.AssignPriority\t{}\t{}\t{}'.format(prioritize_object.obj_number, prioritize_object.obj_name, prioritize_object.priority), keypress.time)
						prioritizations -= 1
						prioritize_object = None
						if prioritizations == 0:
							if selected_object == None:
								view.activateActionMenu(None,currentlevel)
							else: #interruption prioritization
								view.activateActionMenu(selected_object,currentlevel)
								queue.highlighted_object = queue.selected_object
								if interruptionselection == True: #interrupting object selected after interrupted object prioritized
									interruptionselection = False
									performance.logMessage('InterruptMenu.SelectObject\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name), keypress.time)
							current_menu = 'action menu'
						else: 
							arriving_object = queue.addObject()
							view.activatePrioritizationMenu(arriving_object, str(prioritizations))
							current_menu = 'prioritization menu'
							prioritize_object = arriving_object
							arriving_object = None
					elif keypress == '2' or keypress == u'2':#medium
						prioritize_object.setPriority(2)
						performance.logMessage('PriorityMenu.AssignPriority\t{}\t{}\t{}'.format(prioritize_object.obj_number, prioritize_object.obj_name, prioritize_object.priority), keypress.time)
						prioritizations -= 1
						prioritize_object = None
						if prioritizations == 0:
							if selected_object == None:
								view.activateActionMenu(None,currentlevel)
							else:
								view.activateActionMenu(selected_object,currentlevel)
								queue.highlighted_object = queue.selected_object
								if interruptionselection == True:
									interruptionselection = False
									performance.logMessage('InterruptMenu.SelectObject\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name), keypress.time)
							current_menu = 'action menu'
						else:
							arriving_object = queue.addObject()
							view.activatePrioritizationMenu(arriving_object, str(prioritizations))
							current_menu = 'prioritization menu'
							prioritize_object = arriving_object
							arriving_object = None
					elif keypress == '3' or keypress == u'3':#low
						prioritize_object.setPriority(1)
						performance.logMessage('PriorityMenu.AssignPriority\t{}\t{}\t{}'.format(prioritize_object.obj_number, prioritize_object.obj_name, prioritize_object.priority), keypress.time)
						prioritizations -= 1
						prioritize_object = None
						if prioritizations == 0:
							if selected_object == None:
								view.activateActionMenu(None,currentlevel)
							else:
								view.activateActionMenu(selected_object,currentlevel)
								queue.highlighted_object = queue.selected_object
								if interruptionselection == True:
									interruptionselection = False
									performance.logMessage('InterruptMenu.SelectObject\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name), keypress.time)
							current_menu = 'action menu'
						else:
							arriving_object = queue.addObject()
							view.activatePrioritizationMenu(arriving_object, str(prioritizations))
							current_menu = 'prioritization menu'
							prioritize_object = arriving_object
							arriving_object = None
					queue.sortQueue() #need to sort after setting priority
				elif current_menu == 'interruption menu':
					if keypress == '1' or keypress == u'1':
						current_menu = 'prioritization menu'
						performance.logMessage('InterruptMenu.PrioritizeInterruption', keypress.time)
						prioritizations = 1
						view.activatePrioritizationMenu(arriving_object, str(prioritizations))
						prioritize_object = arriving_object
						arriving_object = None
					elif keypress == '2' or keypress == u'2':
						selected_object.setPriority(-1)
						queue.addSelectedObject()
						current_menu = 'prioritization menu'
						performance.logMessage('InterruptMenu.SwitchObject', keypress.time)
						prioritizations = 1
						view.activatePrioritizationMenu(selected_object, str(prioritizations))
						prioritize_object = selected_object
						queue.highlighted_object = arriving_object ### need to set highlighted object 
						selected_object = queue.selectObject()
						arriving_object = None
						currentlevel = 1
						interruptionselection = True
				elif current_menu == 'action menu':
					if keypress == '1' or keypress == u'1': # select object
						if queue.selected_object <> None: 
							selected_object.setPriority(-1)
							queue.addSelectedObject()
							current_menu = 'prioritization menu'
							prioritizations = 1
							view.activatePrioritizationMenu(selected_object, str(prioritizations))
							prioritize_object = selected_object
							queue.clearHighlight()
							selected_object = None
						else:
							view.activateSelectMenu()
							queue.makeActive(None)
							performance.logMessage('ActionMenu.SelectObjectMenu', keypress.time)
							currentlevel = 1
							current_menu = 'select menu'
					elif keypress == '2' or keypress == u'2': # query object
						if selected_object != None:
							view.activateQueryMenu()
							performance.logMessage('ActionMenu.QueryObjectMenu\t{}\t{}'.format(selected_object.obj_number,selected_object.obj_name), keypress.time)
							current_menu = 'query menu'
					elif keypress == '3' or keypress == u'3': #sort object
						if selected_object != None:
							if selected_object.interrupt_level == currentlevel and selected_object.interrupted == False: #forces interruption if trying to sort before interruption occurs
								selected_object.interrupt_timer = 0
								continue
							view.activateSortMenu()
							performance.logMessage('ActionMenu.SortObjectMenu', keypress.time)
							current_menu = 'sort menu'
				elif current_menu == 'select menu':
					if keypress == '1' or keypress == u'1': # move up
						queue.moveSelectionUp()
						performance.logMessage('SelectObjectMenu.MoveUp', keypress.time)
					elif keypress == '2' or keypress == u'2': # move down
						queue.moveSelectionDown()
						performance.logMessage('SelectObjectMenu.MoveDown', keypress.time)
					elif keypress == '3' or keypress == u'3': # select object from queue
						selected_object = queue.selectObject()
						view.activateActionMenu(selected_object,currentlevel)
						performance.logMessage('SelectObjectMenu.SelectObject\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name), keypress.time)
						current_menu = 'action menu'
					elif keypress == '4' or keypress == u'4': # return to action menu
						performance.logMessage('SelectObjectMenu.ReturnToActionMenu', keypress.time)
						queue.clearHighlight()
						current_menu = 'action menu'
						view.activateActionMenu(None,currentlevel)
				elif current_menu == 'query menu':
					if keypress == '1' or keypress == u'1': 
						if currentlevel == 1:# query color
							performance.logMessage('QueryObjectMenu.QueryColor\t{}\t{}\t{}'.format(selected_object.color, selected_object.obj_number, selected_object.obj_name), keypress.time)
							if selected_object.queried_color:
								performance.logMessage('RepeatedQueryPenalty.Color\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name))
								for i in range(5, 0, -1):
									feedback.addFeedbackItem('Repeated Query Penalty: 00{}'.format(i), '1')
									view.draw()
									self.win.flip()
									core.wait(1)
							feedback.addFeedbackItem('Color is: ' + selected_object.color, '1')
							selected_object.queried_color = True
						elif currentlevel == 2:# query pitch
							performance.logMessage('QueryObjectMenu.QueryPitch\t{}\t{}\t{}'.format(selected_object.pitch, selected_object.obj_number, selected_object.obj_name), keypress.time)
							if selected_object.queried_pitch:
								performance.logMessage('RepeatedQueryPenalty.Pitch\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name))
								for i in range(5, 0, -1):
									feedback.addFeedbackItem('Repeated Query Penalty: 00{}'.format(i), '1')
									view.draw()
									self.win.flip()
									core.wait(1)
							feedback.addFeedbackItem('Pitch is: ' + selected_object.pitch, '1')
							selected_object.queried_pitch = True	
						elif currentlevel == 3:# query texture
							performance.logMessage('QueryObjectMenu.QueryTexture\t{}\t{}\t{}'.format(selected_object.texture, selected_object.obj_number, selected_object.obj_name), keypress.time)
							if selected_object.queried_texture:
								performance.logMessage('RepeatedQueryPenalty.Texture\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name))
								for i in range(5, 0, -1):
									feedback.addFeedbackItem('Repeated Query Penalty: 00{}'.format(i), '1')
									view.draw()
									self.win.flip()
									core.wait(1)
							feedback.addFeedbackItem('Texture is: ' + selected_object.texture, '1')
							selected_object.queried_texture = True	
					elif keypress == '2' or keypress == u'2': 
						if currentlevel == 1:# query shape
							performance.logMessage('QueryObjectMenu.QueryShape\t{}\t{}\t{}'.format(selected_object.shape, selected_object.obj_number, selected_object.obj_name), keypress.time)
							if selected_object.queried_shape:
								performance.logMessage('RepeatedQueryPenalty.Shape\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name))
								for i in range(5, 0, -1):
									feedback.addFeedbackItem('Repeated Query Penalty: 00{}'.format(i), '1')
									view.draw()
									self.win.flip()
									core.wait(1)
							feedback.addFeedbackItem('Shape is: ' + selected_object.shape, '1')
							selected_object.queried_shape = True
						elif currentlevel == 2:# query instrument
							performance.logMessage('QueryObjectMenu.QueryInstrument\t{}\t{}\t{}'.format(selected_object.instrument, selected_object.obj_number, selected_object.obj_name), keypress.time)
							if selected_object.queried_instrument:
								performance.logMessage('RepeatedQueryPenalty.Instrument\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name))
								for i in range(5, 0, -1):
									feedback.addFeedbackItem('Repeated Query Penalty: 00{}'.format(i), '1')
									view.draw()
									self.win.flip()
									core.wait(1)
							feedback.addFeedbackItem('Instrument is: ' + selected_object.instrument, '1')
							selected_object.queried_instrument = True
						elif currentlevel == 3:# query material
							performance.logMessage('QueryObjectMenu.QueryMaterial\t{}\t{}\t{}'.format(selected_object.material, selected_object.obj_number, selected_object.obj_name), keypress.time)
							if selected_object.queried_material:
								performance.logMessage('RepeatedQueryPenalty.Material\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name))
								for i in range(5, 0, -1):
									feedback.addFeedbackItem('Repeated Query Penalty: 00{}'.format(i), '1')
									view.draw()
									self.win.flip()
									core.wait(1)
							feedback.addFeedbackItem('Material is: ' + selected_object.material, '1')
							selected_object.queried_material = True
					elif keypress == '3' or keypress == u'3': 
						if currentlevel == 1:# query size
							performance.logMessage('QueryObjectMenu.QuerySize\t{}\t{}\t{}'.format(selected_object.size, selected_object.obj_number, selected_object.obj_name), keypress.time)
							if selected_object.queried_size:
								performance.logMessage('RepeatedQueryPenalty.Size\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name))
								for i in range(5, 0, -1):
									feedback.addFeedbackItem('Repeated Query Penalty: 00{}'.format(i), '1')
									view.draw()
									self.win.flip()
									core.wait(1)
							feedback.addFeedbackItem('Size is: ' + selected_object.size, '1')
							selected_object.queried_size = True
						elif currentlevel == 2:# query tempo
							performance.logMessage('QueryObjectMenu.QueryTempo\t{}\t{}\t{}'.format(selected_object.tempo, selected_object.obj_number, selected_object.obj_name), keypress.time)
							if selected_object.queried_tempo:
								performance.logMessage('RepeatedQueryPenalty.Tempo\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name))
								for i in range(5, 0, -1):
									feedback.addFeedbackItem('Repeated Query Penalty: 00{}'.format(i), '1')
									view.draw()
									self.win.flip()
									core.wait(1)
							feedback.addFeedbackItem('Tempo is: ' + selected_object.tempo, '1')
							selected_object.queried_tempo = True
						elif currentlevel == 3:# query consistency
							performance.logMessage('QueryObjectMenu.QueryConsistency\t{}\t{}\t{}'.format(selected_object.consistency, selected_object.obj_number, selected_object.obj_name), keypress.time)
							if selected_object.queried_consistency:
								performance.logMessage('RepeatedQueryPenalty.Consistency\t{}\t{}'.format(selected_object.obj_number, selected_object.obj_name))
								for i in range(5, 0, -1):
									feedback.addFeedbackItem('Repeated Query Penalty: 00{}'.format(i), '1')
									view.draw()
									self.win.flip()
									core.wait(1)
							feedback.addFeedbackItem('Consistency is: ' + selected_object.consistency, '1')
							selected_object.queried_consistency = True
					elif keypress == '4' or keypress == u'4':
						performance.logMessage('QueryObjectMenu.ReturnToActionMenu', keypress.time)
					current_menu = 'action menu'
					view.activateActionMenu(selected_object,currentlevel)
				elif current_menu == 'sort menu':
					# number corresponds to bin number
					bin_correctness = bins.sortObjectIntoBin(selected_object, int(keypress.char), currentlevel)
					if bin_correctness == 1: #correct
						if queue.checkFinalLevel(selected_object, currentlevel):
							sort_score = queue.calculateSortPenalty(selected_object)
							performance.changeScore(sort_score)
							performance.logMessage('SortObjectMenu.ChooseBin\t{}\t1\t{}\t{}\t{}\t1'.format(keypress.char, sort_score, bin_correctness, currentlevel), keypress.time)
							feedback.addFeedbackItem('Sort is: Correct! ' + str(sort_score) + ' points.', '2')
							queue.sortedObject(selected_object)
							selected_object = None
							currentlevel = 1
							view.queue.queueViewClear()
							view.activateActionMenu(selected_object,currentlevel)
							performance.logMessage('Screen\tActionMenu')
							if queue.checkAddObject():
								arriving_object = queue.addObject()
								current_menu = 'prioritization menu'
								performance.logMessage('Screen\tPriorityMenu')
								prioritizations = random.randint(1,3)
								view.activatePrioritizationMenu(arriving_object, str(prioritizations))
								prioritize_object = arriving_object
								feedback.addFeedbackItem('Arrival object is: {}'.format(arriving_object.obj_name), '3')
								arriving_object = None
							else:
								feedback.addFeedbackItem('No new objects', '3')
								current_menu = 'action menu'
						else:
							sort_score = queue.calculateSortPenalty(selected_object)
							performance.logMessage('SortObjectMenu.ChooseBin\t{}\t1\t{}\t{}\t{}\t0'.format(keypress.char, sort_score, bin_correctness, currentlevel), keypress.time)
							currentlevel += 1
							if currentlevel == 2:
								feedback.addFeedbackItem('Correct! Continue sorting on the auditory level.','2')
							else:
								feedback.addFeedbackItem('Correct! Continue sorting on the tactile level.','2')
							performance.logMessage('Screen\tActionMenu')
							current_menu = 'action menu'
							performance.logMessage('Screen\tActionMenu\t{}'.format(selected_object.obj_number))
							view.activateActionMenu(selected_object,currentlevel)
					else:
						feedback.addFeedbackItem('Sort is: Incorrect! -' + str(queue.getPoints(selected_object)) + ' penalty points.', '2')
						performance.changeScore(queue.getPoints(selected_object)*-1)
						performance.logMessage('SortObjectMenu.ChooseBin\t{}\t0\t-{}\t{}\t{}'.format(keypress.char, queue.getPoints(selected_object), bin_correctness, currentlevel), keypress.time)
						performance.logMessage('Screen\tActionMenu\t{}'.format(selected_object.obj_number))
						current_menu = 'action menu'
						view.activateActionMenu(selected_object,currentlevel)
				else:
					raise Exception('unknown menu for current_menu')
			keyboard_events = []
			view.draw()
			self.win.flip()
			#act-r actions occur after admview updated
				#locations for objects to attend (top left of box)
				#Feedback box: (100,226)
				#Selected object: (-382,130)
				#Queue object1: (-382, 84), y- (23*
				#Prioritization/Interruption box: (-68,-188)
				#select menu: (-126, 67)
				#query menu: (100, 67)
				#sort menu: (326, 67)
			if self.actr:
				if currentgoal == "PRIORITIZE_OBJECT":
					stim = VisualChunk("stim1", "vis-stim", -68, -188, value="1")
					self.actr.display_new([stim])
		performance.flushLog()
		queue.writeQueue(expInfo['participant number'], blocks[block_num])
		self.win.color = 'white'
		self.win.flip() #for some reason you have to flip it before you change the text
	####feedback page#####
		totalscore = performance.score+queue.calculatePenaltyPoints()
		self.highscores.updateHighScores(totalscore)
		performance.updateSessionScore(totalscore)
		self.instext.setText("Your score for sorted objects was: "+str(performance.score)+"\nYour penalty for unsorted objects was: "+str(queue.calculatePenaltyPoints())+"\nYour score for this block was: "+str(totalscore)+"\n\nYour highest scores so far are:\n"+self.highscores.getHighScores())
		self.instext.pos = (0,0)
		self.instext.draw()
		self.nextslidetext.setText("Press the spacebar when you are ready to continue.")
		self.nextslidetext.draw()
		self.win.flip() 
		self.sessionscore = performance.sessionscore
		key = event.getKeys()
		while True:
			while len(key) == 0:
				key = event.getKeys()
				reactor.iterate()
			if key[0] in {'space'}:
				break

	def draw_session_end(self):
		if int(self.session) == 3:
			if self.sessionscore < 18137.78:
				self.instext.setText("End of Study Performance Bonus: $5\n\nJob well done! Your total points fell within the range of what most people scored. For your effort, you will be awarded $5.")
			elif self.sessionscore < 48142.835: 
				self.instext.setText("End of Study Performance Bonus: $10\n\nCongratulations! Your score was above average. For your effort, you will be awarded $10.")
			elif self.sessionscore < 63145.3625: 
				self.instext.setText("End of Study Performance Bonus: $15\n\nCongratulations! You performed exceptionally well. Your total points were almost within the highest range possible. For your effort, you will be awarded $15.")
			else: 
				self.instext.setText("End of Study Performance Bonus: $20\n\nCongratulations! Very few sorters were able to perform at your level. Your total points were within the highest range possible. For your effort, you will be awarded $20.")
			self.instext.pos = (0,0)
			self.instext.draw()
		self.highscores.writeHighScores(expInfo['participant number'])
		self.nextslidetext.setText("This concludes the experiment. Thank you for your time! Please notify the experimenter")
		self.nextslidetext.draw()
		self.win.flip()
		key = event.getKeys()
		while True:
			while len(key) == 0:
				key = event.getKeys()
				reactor.iterate()
			if key[0] in {'space'}:
				break

if __name__ == '__main__':

	dateStr = time.strftime("%m_%d_%Y_%H%M", time.localtime())#add the current time
	try:#try to get a previous parameters file
		expInfo = fromFile('lastADMParams.pickle')
	except:#if not there then use a default set
		expInfo = {'participant number':'1', 'session number':3, 'date': dateStr, 'ADMVersion': ADM_VERSION}

	#present a dialogue to change params
	while expInfo['participant number'] == '0' or (int(expInfo['session number']) < 1 or int(expInfo['session number']) > 3):
		dlg = gui.DlgFromDict(expInfo, title='ADM Experiment', fixed=['date', 'ADMVersion'])
		if dlg.OK:
			toFile('lastParams.pickle', expInfo)#save params to file for next time
		else:
			core.quit()#the user hit cancel so exit

	#make a text file to save data
	filename = expInfo['participant number'] + '_ADM_' + dateStr
	exp = data.ExperimentHandler(name = 'sADM', version = '5.0', extraInfo = expInfo, dataFileName = filename)
    
	env = Environment(actr=actr_enabled, subjectID="1", session="1")
	print 'starting reactor'
	reactor.run()

