import random
from PIL import ImageDraw, Image

class Synthesizer(object):

	def __init__(self, 
				 background,
				 texts,
				 layout, 
				 min_num_segs=1,
				 max_num_segs=1,
				 processors=None,
				 max_failure=30):

		self.background = background
		self.texts = texts
		self.layout = layout
		self.min_num_segs = min_num_segs
		self.max_num_segs = max_num_segs
		self.processors = processors
		self.max_failure = max_failure

		super().__init__()


	def __call__(self):
		failure_count = 0
		sample = None
		while True:
			sample = self.synthesize()
			
			if sample is None:
				failure_count += 1
			else:
				break

			if failure_count > self.max_failure:
				print('Synthesizer fails to generate a sample after %d times failures.' % (self.max_failure))
				exit()

		# extra processings: like adding noise.
		if self.processors is not None:
			for p in self.processors:
				sample = p.process(sample)

		if failure_count > 0:
			print('After %s failures...' % failure_count)

		return sample


	def synthesize(self):

		self.cur_background = self.background()

		num_segs = random.randint(self.min_num_segs, self.max_num_segs)

		self.cur_texts = list()
		for i in range(num_segs):	
			ind = random.randint(0, len(self.texts) - 1)
			self.cur_texts.append(self.texts[ind]())

		result = self.layout.place(self.cur_background, self.cur_texts)

		return result
