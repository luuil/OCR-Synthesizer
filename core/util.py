# coding: utf-8
# author: luuil@outlook.com
# created: 2018-11-23 15:45:42
# modified: 2018-11-27 15:43:39
# =============================================================
r""""""

from PIL import Image
import cv2
import os

def crop_image(image, roi):
  """
  image: object opened by PIL
  roi: x, y, w, h
  """
  return image.crop((roi[0], roi[1], roi[0] + roi[2], roi[1] + roi[3]))

def concatenate_images(images):
    """Horizontally concatenate list of images.
    images: list of images.
    """
    # images = map(Image.open, images)
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
      new_im.paste(im, (x_offset,0))
      x_offset += im.size[0]
    return new_im

def resize(raw_image, target_height):
  assert raw_image is not None
  return cv2.resize(raw_image,
    (int(raw_image.shape[1] * target_height / raw_image.shape[0]), target_height),
    interpolation=cv2.INTER_NEAREST)

def padding(input, pixels):
  width, height = input.size
  left, top, right, bottom = pixels
  if left == 0 and top == 0 and right == 0 and bottom == 0:
    return input
  new_size = width + left + right, height + top + bottom
  new_image = Image.new("RGB", new_size)
  new_image.paste(input, (left, top))
  return new_image


#####################################################

def main_crop():
  from PIL import Image
  import os

  rois = [[790, 1025, 200, 24], [790, 1045, 200, 24]]
  image_dir = "../backgrounds/demo"
  n = 1
  for name in os.listdir(image_dir):
    image_path = os.path.join(image_dir, name)
    image = Image.open(image_path)
    for roi in rois:
      image_crop = crop_image(image, roi)
      # image_crop = concatenate_images([image_crop, image_crop])
      image_crop.save("{}.jpg".format(str(n)))
      n += 1

def main_resize():
  image_dir_in = r"../backgrounds/demo"
  image_dir_out = r"../backgrounds/demo"
  h = 24
  for image_name in sorted(os.listdir(image_dir_in)):
    image_path = os.path.join(image_dir_in, image_name)
    image_path_out = os.path.join(image_dir_out, image_name)
    raw_image = cv2.imread(image_path)
    image = resize(raw_image, h)
    cv2.imwrite(image_path_out, image)


def main_padding():
  image_dir = "../backgrounds/demo"
  pixels = [[50, 0, 0, 0],  [0, 50, 0, 0],  [0, 0, 50, 0],  [0, 0, 0, 50],  [30, 100, 500, 50]]
  for name in os.listdir(image_dir):
    image_path = os.path.join(image_dir, name)
    image = Image.open(image_path)
    image = padding(image, pixels[4])
    image.show()
    image.close()

if __name__ == "__main__":
  # main_crop()
  # main_resize()
  main_padding()