#!/bin/env python
# Makes jio phone compatible landscape videos 
try:
	from ffmpy import FFmpeg
except:
	print("Install ffmpy python module")
import os

def convert():
	src="SOURCE"
	dst="OUTPUT"
	files=""
	try:
		files=os.listdir(src)
	except FileNotFoundError:
		print(src+" directory not found. Please create one.")
		exit(1)


	if(len(files)==0):
		print("No files found. Sorry, I cannot generate videos for you")
		exit(1)

	try: 
		os.makedirs(dst)
	except: #May occur if already exists. [Perm error would also cause this but that's a diff story
		pass

	print("Found: ")
	print("\n".join(files))
	for file in files:
		ff = FFmpeg(
				inputs={src+'/'+file:None},
				outputs={dst+'/'+file: '-vf transpose=clock,scale=240:320'}
				)
		ff.run()
	print("Done!")
