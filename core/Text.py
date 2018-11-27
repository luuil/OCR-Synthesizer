import os
import random
from PIL import ImageFont

class Text(object):

	def __init__(self,
				 plaintext,
				 font_dir,
				 text_size_range,
				 opacity_range,
				 r_range,
				 g_range,
				 b_range):
		
		self.plaintext = plaintext
		self.font_dir = font_dir
		self.text_size_range = text_size_range
		self.opacity_range = opacity_range
		self.r_range = r_range
		self.g_range = g_range
		self.b_range = b_range

		if not os.path.exists(self.font_dir):
			print('%s: Font directory %s does not exist' % (self.__class__.__name__, self.font_dir))
		
		self.font_dict = dict()
		for font_name in os.listdir(self.font_dir):
			font_path = os.path.join(self.font_dir, font_name)
			for font_size in range(self.text_size_range[0], self.text_size_range[1] + 1):
				self.font_dict[(font_name.split('.')[0], font_size)] = ImageFont.truetype(font_path, font_size)			

	def __call__(self):
		plaintext = self.plaintext()

		font = random.choice(list(self.font_dict.values()))

		color = (random.randint(*self.r_range), random.randint(*self.g_range), random.randint(*self.b_range))

		opacity = self.opacity_range[0] + random.random() * (self.opacity_range[1] - self.opacity_range[0])

		return plaintext, font, color, opacity




