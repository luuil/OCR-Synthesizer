import random

class SynthesizerGroup(object):
	
	def __init__(self):
		self.weights = list()
		self.synthesizers = list()
		self.names = list()
		self.cur_synthesizer = None
		super().__init__()


	def add(self, name, synthesizer, weight):
		print('Add Synthesizer %s with weight %f to SynthesizerGroup' % (name, weight))
		self.names.append(name)
		self.synthesizers.append(synthesizer)
		self.weights.append(weight)


	def generate_sample(self):
		synthesizer = None
		rand = random.random() * sum(self.weights)
		for j, weight in enumerate(self.weights):
			rand -= weight
			if rand <= 0:
				synthesizer = self.synthesizers[j]
				break
		self.cur_synthesizer = synthesizer
		
		return synthesizer()