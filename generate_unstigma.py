#! /usr/bin/python3
# -*- coding: utf-8 -*-
__author__    = "Pierre Etheve"
__email__  = "pierre.etheve.lfdv@gmail.com"

import os
import argparse
import shutil

parser = argparse.ArgumentParser(description="Custom dataset builder for Pix2Pix")
parser.add_argument('-source', type=str, required=True, help='folder where raw files are located')
parser.add_argument('-results', type=str, required=True, help='folder where raw files are located')
parser.add_argument('-variant', type=str, required=False, default="", help='variant of the struct folder')
opt = parser.parse_args()

variant = ""
if opt.variant != "" :
	variant = "_"+opt.variant

struct_draw = os.path.join(opt.source, "struct%s/draw"%variant)
struct_vid = os.path.join(opt.source, "struct%s/vid"%variant)

try :
	shutil.rmtree(os.path.join(opt.source, "unstigma"))
except :
	pass

os.mkdir(os.path.join(opt.source, "unstigma"))

unstigma_draw = os.path.join(opt.source, "unstigma/draw")
unstigma_vid = os.path.join(opt.source, "unstigma/vid")
os.mkdir(unstigma_vid)
os.mkdir(unstigma_draw)

print(struct_draw, struct_vid)

draw_list = os.listdir(struct_draw)
draw_list.sort();
print(draw_list)

for file in draw_list :
	from_file = os.path.join(struct_draw, file)
	to_file = os.path.join(unstigma_draw, file)
	print(from_file, to_file)
	shutil.copyfile(from_file, to_file)

vid_path = os.path.join(opt.results, "test_latest/images")
vid_list = os.listdir(vid_path)
vid_list.sort();
print(vid_list)

for file in vid_list :
	# print(file, "_fake_B" in file)
	if "_fake_B" in file :
		new_name = file.split("_fake_B")[0]+".png"
		from_file = os.path.join(vid_path, file)
		to_file = os.path.join(unstigma_vid, new_name)
		print(from_file, to_file)
		shutil.copyfile(from_file, to_file)