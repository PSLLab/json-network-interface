from psychopy import visual
from psychopy.visual.rect import Rect

class TextInRect(Rect):
	def __init__(self, win, height = 100, width = 100, pos = (0, 0), textHeight = None, lineColor = 'black', text = "Test", textColor = 'black', alignHoriz = 'center', font = None, **kwargs):
		self.text_stim = visual.TextStim(win, pos = pos)
		#self.autoDraw = True
		self.text_stim.text = text
		self.text_stim.color = textColor
		self.text_stim.alignHoriz = alignHoriz
		self.text_stim.font = font
		if alignHoriz == 'left':
			self.text_stim.pos = (pos[0] - width/2, pos[1])
	
		self.text_stim.height = textHeight
		self.win = win
		super(TextInRect, self).__init__(win, height=height, width=width, pos=pos, lineColor = lineColor, **kwargs)

	def setText(self, text):
		self.text_stim.text = text
	
	def setTextColor(self, color):
		self.text_stim.color = color
		self.text_stim.draw()
	
	def draw(self):
		Rect.draw(self)
		self.text_stim.draw() 
