import csv

class ADMBins:
	def __init__(self, filename):
	# bins is an array of dictionaries where each bin is a dictionary
		self.bins = []
		with open(filename, 'rU') as csvfile:
			reader = csv.reader(csvfile)
			reader.next()
			for row in reader:
				self.bins.append({'color': row[0], 'shape': row[1], 'size': row[2], 'pitch': row[3], 'instrument': row[4], 'tempo': row[5], 'texture': row[6], 'material': row[7], 'consistency': row[8]})

	def sortObjectIntoBin(self,object,bin_number, sort_level): 
		score = 0
		bin_number -= 1
		if sort_level == 1:
			if self.bins[bin_number]['color'] == object.color and self.bins[bin_number]['shape'] == object.shape and self.bins[bin_number]['size'] == object.size:
				score = 1
		elif  sort_level == 2:
			if self.bins[bin_number]['pitch'] == object.pitch and self.bins[bin_number]['instrument'] == object.instrument and self.bins[bin_number]['tempo'] == object.tempo:
				score = 1
		elif  sort_level == 3:
			if self.bins[bin_number]['texture'] == object.texture and self.bins[bin_number]['material'] == object.material and self.bins[bin_number]['consistency'] == object.consistency:
				score = 1
		return score

