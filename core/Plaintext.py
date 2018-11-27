import abc
import random

class Plaintext(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self):
		super().__init__()

	def __call__(self):
		plaintext = self.generate()
		return plaintext.strip()

	@abc.abstractmethod
	def generate(self):
		pass

class VarLengthPlaintext(Plaintext):
	def __init__(self, 
				 word_list=None, 
				 word_list_file=None, 
				 min_length=1, 
				 max_length=6, 
				 space_rate=0.0):
	
		if word_list is None and word_list_file is None:
			print('%s: word_list and word_list_file can not be None both.' % self.__class__.__name__)
			exit()

		self.word_list = word_list if word_list is not None else self.parse_word_list_file(word_list_file)
		self.min_length = min_length
		self.max_length = max_length
		self.space_rate = space_rate

		super().__init__()

	def parse_word_list_file(self, word_list_file):
		with open(word_list_file, 'r') as f:
			return [line.strip() for line in f.readlines()]

	def generate(self):
		length = random.randint(self.min_length, self.max_length)

		plaintext = list()
		for i in range(length):
			word = random.choice(self.word_list)
			word = word() if callable(word) else word
			plaintext.append(word)
			if random.random() < self.space_rate:
				plaintext.append(' ')

		plaintext = ''.join(plaintext)

		return plaintext






