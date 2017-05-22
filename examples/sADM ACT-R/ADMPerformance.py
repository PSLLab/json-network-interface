from psychopy import core

# this class will keep track of score and log events
class ADMPerformance:
	def __init__(self, log_filename, score_box, starttime):
		self.score = 0
		self.log_filename = log_filename
		self.to_flush = ["ADM Version: 5.1\nStart: " + str(starttime) + "\n"]
		self.score_box = score_box
		self.score_box.setText(str(self.score))
		self.sessionscore = 0

	def logMessage(self, message, time = None):
		# allow timestamp from key press to be passed through but set time to getTime() if no timestamp is passed
		if time == None:
			time = core.getTime()
		self.to_flush.append(str(core.getTime()) + '\t' + message + '\n')

	def changeScore(self, score_delta):
		self.score += score_delta
		self.score_box.setText(str(self.score))

	def flushLog(self):
		with open(self.log_filename, 'a') as log:
			log.writelines(self.to_flush)
		self.to_flush = []

	def updateSessionScore(self, score):
		self.sessionscore += score
