from PIL import Image, ImageFilter
import os
import random
import abc
import numpy as np

class Processor(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self):
		super().__init__()

	def __call__(self, input):
		return self.process(input)

	@abc.abstractmethod
	def process(self, input):
		pass
		

class GaussianBlurProcessor(Processor):
	def __init__(self, 
				 min_radius, 
				 max_radius):
		self.min_radius = min_radius
		self.max_radius = max_radius
		self.cur_radius = None
		super().__init__()

	def process(self, input):
		self.cur_radius = random.randint(self.min_radius, self.max_radius)
		return input.filter(ImageFilter.GaussianBlur(radius=self.cur_radius))
		

class SaltPepperNoiseProcessor(Processor):
	def __init__(self,
				 noise_proportion,
				 salt_proportion):
		self.noise_proportion = noise_proportion
		self.salt_proportion = salt_proportion
		super().__init__()

	def process(self, input):
		process_or_not = np.random.randint(0, 5)
		if process_or_not != 0: # 1/5 probability will add noises
			return input
			
		nparray = np.array(input)
		h, w, c = nparray.shape

		# add salt
		salt_amount = int(h * w * self.noise_proportion * self.salt_proportion)
		salt_h_coords = np.random.randint(0, h - 1, salt_amount)
		salt_w_coords = np.random.randint(0, w - 1, salt_amount)
		nparray[(salt_h_coords, salt_w_coords)] = (255, 255, 255)

		# add pepper
		pepper_amount = int(h * w * self.noise_proportion * (1 - self.salt_proportion))
		pepper_h_coords = np.random.randint(0, h - 1, pepper_amount)
		pepper_w_coords = np.random.randint(0, w - 1, pepper_amount)
		nparray[(pepper_h_coords, pepper_w_coords)] = (0, 0, 0)

		return Image.fromarray(nparray)


class PaddingCropResizeProcessor(Processor):
	def __init__(self, 
				 crop_rois,
				 padding_pixels, 
				 target_size):
		self.crop_rois = crop_rois
		self.padding_pixels = padding_pixels
		self.target_size = target_size[0], target_size[1]
		super().__init__()

	def process(self, input):
		# crop
		rnd_idx = np.random.randint(0, len(self.crop_rois))
		crop_roi = tuple(self.crop_rois[rnd_idx])
		# input = input.crop((crop_roi[0], crop_roi[1], crop_roi[0] + crop_roi[2], crop_roi[1] + crop_roi[3]))
		input = input.crop(crop_roi)

		# padding
		rnd_idx = np.random.randint(0, len(self.padding_pixels))
		padding = self.padding_pixels[rnd_idx]
		input = self.padding(input, padding)

		return input.resize(self.target_size)

	@staticmethod
	def padding(input, pixels):
		width, height = input.size
		left, top, right, bottom = pixels
		if left == 0 and top == 0 and right == 0 and bottom == 0:
			return input
		new_size = width + left + right, height + top + bottom
		new_image = Image.new("RGB", new_size)
		new_image.paste(input, (left, top))
		return new_image
