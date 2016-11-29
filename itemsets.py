import itertools

class ItemSet(object):

	def __init__(self, filename, s, k):

		#Do the initial count (Compulsory for every k, s)
		self.dict = dict()
		self.s = s
		self.k = k
		self.filename = filename

		with open(filename, 'r') as fd:
			while True:
				if fd.readline() == '':
					break

				line = fd.readline()
				self.__initial_line_process__(line)

			self.__apply_initial_threshold__()
			self.k_dict = self.dict


	def __initial_line_process__(self, line):
		transaction = line.strip().split()

		for item in transaction:
			if item in self.dict:
				self.dict[item] = self.dict[item] + 1
			else:
				self.dict[item] = 1

	def __apply_initial_threshold__(self):
		#We kill every item that is lower than the threshold
		for item in self.dict.keys():
			if not self.dict[item] >= self.s:
				del(self.dict[item])

	def __generate_k_empty_dict__(self, k):
		self.k_dict = dict.fromkeys(set(itertools.combinations(self.dict, k)), 0)

	#try to optimize
	def __read_k_dict__(self):
		print "llegue hasta aca"
		import time
		start_time = time.time()
		with open(self.filename, 'r') as fd:
			index = 1
			while True:
				print "iteration " + str(index)
				line = fd.readline()
				if line == '':
						break

				transaction = line.strip().split()
				
				for key_tuple in self.k_dict.keys():
					
					key_in_transaction = True
					for individual_key in key_tuple:
						if not individual_key in transaction:
							key_in_transaction = False
							break

					if key_in_transaction:
						self.k_dict[key_tuple] = self.k_dict[key_tuple] + 1
				index += 1
			print "__read_k_dict__ finished"
			print self.k_dict.values()
			print("--- %s seconds ---" % (time.time() - start_time))
			while True:
				pass

	def __apply_k_threshold__(self):
		#We kill every item that is lower than the threshold
		for item in self.k_dict.keys():
			if not self.k_dict[item] >= self.s:
				del(self.k_dict[item])

	def __update_original_dict__(self):
		for key in self.dict:
			found = False
			for tuple_key in self.k_dict:
				for k_key in tuple_key:
					if key == k_key:
						found = True
						break
			if not found:
				del(self.dict[key])


	def get_k_dict(self):
		k = self.k

		if k < 1:
			return None
		if k == 1:
			return self.dict

		for i in range(k + 1)[2:]: #Only possible to make it from 2 and on
			self.__generate_k_empty_dict__(i)
			self.__read_k_dict__()
			self.__apply_k_threshold__()
			self.__update_original_dict__(self)

		return self.k_dict
