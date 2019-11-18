#! /usr/bin/python3
# -*- coding: utf-8 -*-
__author__    = "Pierre Etheve"
__email__  = "pierre.etheve.lfdv@gmail.com"

from subprocess import Popen, PIPE, STDOUT
import argparse
import os
import shutil

parser = argparse.ArgumentParser(description="Custom dataset builder for Pix2Pix")
parser.add_argument('-project', '-p', type=str, required=True, help='name of the project')
parser.add_argument('-n', type=int, required=False, default=20, help="number of iteration with maximum learning rate (specific to step 1 and 4)")

opt = parser.parse_args()

# cmd = "python test.py --dataroot datasets/%s/struct/ --name %s_struct_pix2pix_mix --model pix2pix --direction AtoB --load_size 384 --crop_size 384 --netG unet_128 --num_test %d --dataset_mode anim"%(opt.project, opt.project, opt.n_render)

def simple_exec(command) :
	p = Popen(command, stdout = PIPE, stderr = STDOUT, shell = True)
	p.wait()

def transfer_images() :
	cmd1 = 'rm datasets/%s/struct/vid/*'%(opt.project)
	cmd3 = 'rm results/%s_struct_pix2pix_mix/test_latest/images/*'%(opt.project)
	simple_exec(cmd1)
	copy_images()
	simple_exec(cmd3)

def copy_images() :
	path_from = "results/%s_struct_pix2pix_mix/test_latest/images/"%(opt.project)
	path_to = "datasets/%s/struct/vid/"%(opt.project)
	files = os.listdir(path_from)
	for file in files : 
		if "_fake_B.png" in file :
			new_name = file.split("_fake")[0]+".png"
			shutil.copyfile(path_from+file, path_to+new_name)
			print("Copied %s to %s"%(path_from+file, path_to+new_name))

def createdir(path) :
	try :
		os.mkdir(path)
	except :
		pass
		
def silene() :
	cmd = "python test.py --dataroot datasets/%s/struct/ --name %s_struct_pix2pix_mix --model pix2pix --direction AtoB --load_size 384 --crop_size 384 --netG unet_128 --num_test 5000 --dataset_mode anim"%(opt.project, opt.project)
	simple_exec(cmd)

def archive(step) :
	path = "datasets/%s/struct/vid/"%(opt.project)
	archive_path = "evolutions/%s/"%(opt.project)
	files = os.listdir(path)
	
	for file in files :
		number = file.split(".png")[0] 
		createdir(archive_path+number)
		shutil.copyfile(path+file, archive_path+number+"/%05d.png"%step)
		print("Archived : '%s' to '%s'"%(path+file, archive_path+number+"/%05d.png"%step))

	step += 1

# transfer_images()
# silene()

createdir("evolutions/%s/"%opt.project)

for step in range(0, opt.n) :
	print("STEP #%03d"%step)
	silene()
	transfer_images()
	archive(step)