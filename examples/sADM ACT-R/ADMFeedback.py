from psychopy import core

class ADMFeedback:
	FEEDBACK_DURATION = 3

	def __init__(self, view):
		# use -1 as a marker that there is no expiration time
		# feedback items are a tuple of text, expiration time, type
		# types are QueryArrivalOther, Sort, Task - matching ADM 3.3.1
		self.feedback_strings = [('', -1, None), ('', -1, None), ('', -1, None)]
		self.view = view

	def checkExpiration(self):
		current_time = core.getTime()
		for  item_num, item in enumerate(self.feedback_strings):
			if item[1] != -1 and item[1] <= current_time:
				self.feedback_strings[item_num] = ('', -1, None)
		self.sortFeedback()
		self.displayFeedbackText()

	def sortFeedback(self):
		self.feedback_strings.sort(key = lambda item: item[1])
		
		#feedback types
                #1 = queries
                #2 = sort result
                #3 = arrival or interrupting object delay	
		

	def displayFeedbackText(self):
		text = ''
		for item in self.feedback_strings:
			text += item[0] + '\n'
		self.view.setText(text)

	def addFeedbackItem(self, text, stype):
		for item_num, item in enumerate(self.feedback_strings):
			
			if item[2] == stype:
				self.feedback_strings[item_num] = (text, core.getTime() + self.FEEDBACK_DURATION, stype)
				break
		else:
			# put it in the 0 slot because that should be the oldest message
			self.feedback_strings[0] = (text, core.getTime() + self.FEEDBACK_DURATION, stype)

		self.sortFeedback()
		self.displayFeedbackText()

