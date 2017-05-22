from psychopy import core
import os.path

class ADMHighScores:

	def __init__(self):
		self.scores = []

	def updateHighScores(self, score):
		self.scores.append(score)
		self.scores.sort(reverse = True)
		if len(self.scores) > 3:
			self.scores = self.scores[0:3]

	def writeHighScores(self, subjectID):
		outfile = open(subjectID + " ADM highestscores.txt",'w')
		for i in self.scores:
			outfile.write(str(i)+"\n")
		outfile.close()

	def readHighScores(self, subjectID):
		if os.path.exists(subjectID + " ADM highestscores.txt"):
			infile = open(subjectID + " ADM highestscores.txt",'rU')
			lines = infile.readlines()
			infile.close()
			for line in lines:
				self.scores.append(int(line.rstrip('\n')))
		else:
			raise Exception('high score file missing')

	def getHighScores(self):
		scorestring = ""
		for i in self.scores:
			scorestring += str(i)+"\n"
		return scorestring
			
