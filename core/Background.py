import os
import abc
import random
from PIL import Image

class Background(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self):
			super().__init__()

	def __call__(self):
		# add pre/post processing in this function
		return self.generate()

	@abc.abstractmethod
	def generate(self):
		pass

class RandomSelectionBackground(Background):
	def __init__(self, image_dir, rois=None):

		self.image_dir = image_dir
		self.rois = rois

		if not os.path.exists(image_dir):
			print('%s: Directory %s does not exist' % (self.__class__.__name__, image_dir))
			exit()
		
		self.bg_dict = dict()		
		for img_name in os.listdir(self.image_dir):
			img_path = os.path.join(self.image_dir, img_name)
			img = Image.open(img_path)
			img_prefix = img_name.split('.')[0]

			if rois is None:
				self.bg_dict[img_prefix] = img.copy()
			else:
				for i, roi in enumerate(rois):
					self.bg_dict[img_prefix + '_' + str(i + 1)] = img.crop((roi[0], roi[1], roi[0] + roi[2], roi[1] + roi[3]))
		
		self.cur_bg_name = None		

		super().__init__()

	def generate(self):
		self.cur_bg_name, self.cur_bg = random.choice(list(self.bg_dict.items()))
		
		return self.cur_bg


class ConcatenateRandomSelectionBackground(Background):
	def __init__(self, image_dir, rois=None):

		self.image_dir = image_dir
		self.rois = rois

		if not os.path.exists(image_dir):
			print('%s: Directory %s does not exist' % (self.__class__.__name__, image_dir))
			exit()
		
		self.bg_dict = dict()		
		for img_name in os.listdir(self.image_dir):
			img_path = os.path.join(self.image_dir, img_name)
			img = Image.open(img_path)
			img_prefix = img_name.split('.')[0]

			if rois is None:
				self.bg_dict[img_prefix] = img.copy()
			else:
				for i, roi in enumerate(rois):
					bg_src = img.crop((roi[0], roi[1], roi[0] + roi[2], roi[1] + roi[3]))
					self.bg_dict[img_prefix + '_' + str(i + 1)] = self.concatenate([bg_src, bg_src])
		
		self.cur_bg_name = None

		super().__init__()

	@staticmethod
	def concatenate(images):
		"""Horizontally concatenate list of images.
		images: list of images.
		"""
		widths, heights = zip(*(i.size for i in images))

		total_width = sum(widths)
		max_height = max(heights)

		new_im = Image.new('RGB', (total_width, max_height))

		x_offset = 0
		for im in images:
		  new_im.paste(im, (x_offset,0))
		  x_offset += im.size[0]
		return new_im

	def generate(self):
		self.cur_bg_name, self.cur_bg = random.choice(list(self.bg_dict.items()))
		
		return self.cur_bg

