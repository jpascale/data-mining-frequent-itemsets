class ItemSet(object):

	def __init__(self, filename, s):

		#Do the initial count (Compulsory for every k, s)
		self.dict = dict()
		self.s = s

		with open(filename, 'r') as fd:
			while True:
				if fd.readline() == '':
					break

				line = fd.readline()
				self.initial_line_process(line)

			print len(self.dict)
			self.apply_threshold()
			print len(self.dict)


	def initial_line_process(self, line):
		transaction = line.strip().split()

		for item in transaction:
			if item in self.dict:
				self.dict[item] = self.dict[item] + 1
			else:
				self.dict[item] = 1

	def apply_threshold(self):
		#We kill every item that is lower than the threshold
		for item in self.dict.keys():
			if not self.dict[item] >= self.s:
				del(self.dict[item])

	def generate_k_dict(self, k)