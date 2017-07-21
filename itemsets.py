import itertools
import time

def difference(a, b):
	return tuple(x for x in a if x not in b)

def sort_tuple(tup):
	if len(tup) == 1:
		return tup[0]

	asd = [int(x) for x in tup]
	asd.sort()
	return tuple([str(x) for x in asd])

class Rule(object):
	def __init__(self, I, j):
		self.I = I
		self.j = j

	def __repr__(self):
		return str(self.I) + " -> " + str(self.j)

	def set_params(self, interest):
		self.interest = interest


class ItemSet(object):

	def __init__(self, filename, s, k):

		#Do the initial count (Compulsory for every k, s)
		self.dict = dict()
		self.s = s
		self.k = k
		self.filename = filename

		#Every i element corresponsds to K = I + 1
		self.bkp_k_dict = []

		with open(filename, 'r') as fd:
			while True:
				if fd.readline() == '':
					break

				line = fd.readline()
				self.__initial_line_process__(line)

			self.__apply_initial_threshold__()
			self.k_dict = self.dict

			#Save dict for K = 1
			self.bkp_k_dict.append(self.dict.copy())


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
			
			print "DEBUG> Generating bkp_k_dict (k = " + str(i) + ")"
			self.bkp_k_dict.append(self.k_dict.copy())

			print "Done\n"

		return self.k_dict

	def print_rules(self):

		keys = self.k_dict.copy().keys()
		rules = []

		bkp_k_merged_dict = dict()
		for a in range(len(self.bkp_k_dict)):
			bkp_k_merged_dict.update(self.bkp_k_dict[a])

		#For every subset generate I -> j rule
		for k in range(self.k)[1:]:
			for key in keys:
				combinations = set(itertools.combinations(key, k))
				for combination in combinations:
					rules.append(Rule(difference(key, combination), combination))

		print "DEBUG> Rules generated"
		print rules

		print "DEBUG> Calculating confidence and interest for each rule"
		#import ipdb; ipdb.set_trace()

		#CONVERT TO SORT - THIS IS HORRIBLE


		#Iterate over rules to check confidence and interest
		for rule in rules:
			print str(rule.I) + " -> " + str(rule.j)
			#import ipdb; ipdb.set_trace()
			interest = bkp_k_merged_dict[sort_tuple(tuple(rule.I) + tuple(rule.j))] / float(bkp_k_merged_dict[sort_tuple(tuple(rule.I))])
			rule.set_params(interest)
			print str(rule.I) + " -> " + str(rule.j) + " - [" + str(rule.interest * 100) + "%]"

		#import ipdb; ipdb.set_trace()

		


if __name__ == '__main__':
	
	print "Test1: threshold s = 600 and k = 3"
	t = time.time()
	a = ItemSet("data.dat", 600, 3)
	a_dict = a.get_k_dict()
	print("Time to perform operation: %s seconds" %  (time.time() - t))
	
	for k, v in a_dict.iteritems():
		print str(k) + ": with support " + str(v)
	
	a.print_rules()
 	print "________________________________"

	print "Test2: threshold s = 1000 and k = 2"
	t = time.time()
	a = ItemSet("data.dat", 1000, 2)
	a_dict = a.get_k_dict()
	print("Time to perform operation: %s seconds" %  (time.time() - t))
	
	for k, v in a_dict.iteritems():
		print str(k) + ": with support " + str(v)
	
	a.print_rules()	
	print "________________________________"

	print "Test3: threshold s = 3000 and k = 1"
	t = time.time()
	a = ItemSet("data.dat", 3000, 1)
	a_dict = a.get_k_dict()
	print("Time to perform operation: %s seconds" %  (time.time() - t))
	
	for k, v in a_dict.iteritems():
		print str(k) + ": with support " + str(v)
	a.print_rules()





