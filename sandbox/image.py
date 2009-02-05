from PIL import Image, ImageDraw
import glob, os

#this file is a short test for PIL programming 
#@TODO remove that from the projects

size = 1024, 1024
im = Image.new('RGBA', size)
mask = Image.new('RGBA', size,(0,0,0,0))
for i in range(45):
	comp = Image.new('RGBA', size,(0,0,0,0))
	draw = ImageDraw.Draw(comp)
	draw.line((0, 0) + im.size, fill=(128,128,0,255-i*4))
	comp = comp.rotate(i*2, Image.BICUBIC)
	#alpha = 0.5
	#im.paste(comp, (0,0))
	im = Image.composite(comp, im, comp)

	#im = em

#im = im.resize((512,512), Image.BICUBIC)
im.save('test.png')