from core.SynthesizerGroup import *
from core.Synthesizer import *
from core.Background import *
from core.Text import *
from core.Plaintext import *
from core.Processor import *
from core.Layout import *

import argparse
import yaml
import os
import random
import time

parser = argparse.ArgumentParser()

parser.add_argument(
	'--config_path',
	default='./configs/demo.yaml',
	type=str,
	help='The path to the config file.')

FLAGS, _ = parser.parse_known_args()


def parse_simple_config(config):
	class_name = config.pop('type')

	args = config
	return globals()[class_name](**args)

def parse_text_config(config):
	args = config
	args['plaintext'] = parse_simple_config(args['plaintext'])
	return Text(**args)

def parse_synthesizer_config(config):
	background = parse_simple_config(config.pop('background'))

	processors = None 
	if 'processors' in config:
		processor_configs = config.pop('processors')
		processors =  [parse_simple_config(c) for c in processor_configs]

	layout = parse_simple_config(config.pop('layout'))
	
	text_configs = config.pop('text')
	if 'text_style' in config:
		style_config = config.pop('text_style')
		for c in text_configs:
			c.update(style_config)

	texts = [parse_text_config(c) for c in text_configs]

	args = {
			'background': background,
			'texts': texts,
			'layout': layout,
			'processors': processors
		   }
	args.update(config)

	return Synthesizer(**args)

def main():
	with open(FLAGS.config_path, 'r') as f: 
		config = yaml.load(f)

	print('Load config from %s\n' % FLAGS.config_path)
	print(config)

	# load basic config
	# TODO label format & output filename format
	num_outputs = config['num_outputs']
	output_dir = config['output_dir']
	label_dir = config['label_dir']
	seed = config['seed']

	# set global random seed
	random.seed(seed)	

	# load synthesizers
	sg = SynthesizerGroup()
	for synthesizer_config in config['synthesizers']:
		name = synthesizer_config.pop('name')
		weight = synthesizer_config.pop('weight')
		synthesizer = parse_synthesizer_config(synthesizer_config)
		sg.add(name, synthesizer, weight)

	# prepare output directories
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	if not os.path.exists(label_dir):
		os.makedirs(label_dir)

	start = time.time()
	
	label_path = os.path.join(label_dir, 'label.txt')
	label_f = open(label_path, 'w')
	for i in range(num_outputs):
		output_img = sg.generate_sample()

		texts = sg.cur_synthesizer.cur_texts
		label_text = ''.join([t[0] for t in texts])

		output_name = '%s_%08d.jpg' % \
			(label_text, 
			 random.randint(0, 99999999))
		output_name = output_name.replace('/', '-')
		output_path = os.path.join(output_dir, output_name)

		print('#%08d  %s' % (i + 1, output_name))				
	
		# write output image and labels
		output_img.save(output_path, 'JPEG')
		label_f.write('%s\t%s\n' % (output_name, label_text))

	end = time.time()
	
	print('time cost: %.2fs' % (end - start))
		
if __name__ == '__main__':
	main()
