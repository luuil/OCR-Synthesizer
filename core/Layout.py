import abc
import random
from PIL import Image, ImageDraw

class Layout(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self):
		super().__init__()

	@abc.abstractmethod
	def place(self, background, texts):
		pass


class HorizontalLayout(Layout):

	def __init__(self):
		super().__init__()

	def place(self, background, texts):
		fonts = [text[1] for text in texts]

		# check if the text size is too large and exceeds the background 
		text_sizes = [font.getsize(text) for text, font, _, _ in texts]
		text_widths = [size[0] for size in text_sizes]
		text_heights = [size[1] for size in text_sizes]
		bg_size = background.size		
		if sum(text_widths) > bg_size[0] or max(text_heights) > bg_size[1]:
			return None

		left = max(bg_size[0] // 2 - sum(text_widths) // 2, 0)		
		left += int(random.random() * left) - left // 2
		upper = None
		for i, (text, font, color, opacity) in enumerate(texts):
			upper = max(bg_size[1] // 2 - text_heights[i] // 2, 0)
			upper += int(random.random() * upper) - upper // 2

			text_palette = background.copy()
			draw_handler = ImageDraw.Draw(text_palette)
			draw_handler.text((left, upper), text, font=font, fill=color)	
			background = Image.blend(background, text_palette, opacity)

			left += text_widths[i]				

		return background

