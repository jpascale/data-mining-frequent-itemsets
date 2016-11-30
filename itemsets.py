import itertools
import time

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
	'''
	#try to optimize
	def __OLD_read_k_dict__(self):
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

				transaction = set(line.strip().split())
				
				for key_tuple in self.k_dict.keys():
					if transaction.issuperset(key_tuple):
						self.k_dict[key_tuple] = self.k_dict[key_tuple] + 1

				index += 1
			print "__read_k_dict__ finished"
			print self.k_dict.values()
			print("--- %s seconds ---" % (time.time() - start_time))
	'''

	##new version
	def __read_k_dict__(self, curr_k):
		with open(self.filename, 'r') as fd:
			while True:
				line = fd.readline()
				if line == '':
						break

				transaction = set(itertools.combinations(line.strip().split(), curr_k))
				for elem in transaction:
					if elem in self.k_dict:
						self.k_dict[elem] = self.k_dict[elem] + 1

	def __apply_k_threshold__(self):
		#We kill every item that is lower than the threshold
		for item in self.k_dict.keys():
			if not self.k_dict[item] >= self.s:
				del(self.k_dict[item])

	def __update_original_dict__(self):
		allowed_keys = set([x for a in self.k_dict.keys() for x in a])

		for key in self.dict.keys():
			if not key in allowed_keys:
				del(self.dict[key])


	def get_k_dict(self):
		k = self.k

		if k < 1:
			return None
		if k == 1:
			return self.dict

		for i in range(k + 1)[2:]: #Only possible to make it from 2 and on
			print "DEBUG> Processing (k = " + str(i) + ")"
			print "DEBUG> Generating empty dictionary (k = " + str(i) + ")"
			self.__generate_k_empty_dict__(i)
			
			print "DEBUG> Filling the dict (k = " + str(i) + ")"
			self.__read_k_dict__(i)
			
			print "DEBUG> Applying threshold (k = " + str(i) + ")"
			self.__apply_k_threshold__()
			
			print "DEBUG> Updating original dict (k = " + str(i) + ")"
			self.__update_original_dict__()
			
			print "Done\n"

		return self.k_dict


if __name__ == '__main__':
	
	print "Test1: threshold s = 600 and k = 3"
	t = time.time()
	a = ItemSet("data.dat", 600, 3)
	a_dict = a.get_k_dict()
	print("Time to perform operation: %s seconds" %  (time.time() - t))

	for k, v in a_dict.iteritems():
		print str(k) + ": with support " + str(v)
	
 	print "________________________________"

	print "Test2: threshold s = 1000 and k = 2"
	t = time.time()
	a = ItemSet("data.dat", 1000, 2)
	a_dict = a.get_k_dict()
	print("Time to perform operation: %s seconds" %  (time.time() - t))
	
	for k, v in a_dict.iteritems():
		print str(k) + ": with support " + str(v)
		
	print "________________________________"

	print "Test3: threshold s = 3000 and k = 1"
	t = time.time()
	a = ItemSet("data.dat", 3000, 1)
	a_dict = a.get_k_dict()
	print("Time to perform operation: %s seconds" %  (time.time() - t))

	for k, v in a_dict.iteritems():
		print str(k) + ": with support " + str(v)





