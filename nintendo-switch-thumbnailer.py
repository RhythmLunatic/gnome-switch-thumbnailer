#!/usr/bin/env python3
import re
import sys
import requests
import json
import cv2
import numpy
import os
import time

#Change to False if you want it to run faster, but titles.json will be 50MB instead of 11MB.
USE_COMPRESSION = True
TITLES = os.path.join(os.path.expanduser('~'),'.cache/','titles.json')
if USE_COMPRESSION:
	import gzip
	TITLES=TITLES+".gz"

assert len(sys.argv) == 4


def downloadNewDatabase():
	print("Have to download a new database... Please wait")
	r=requests.get('https://tinfoil.media/repo/db/titles.json')
	if USE_COMPRESSION:
		print("Compressing database, this might take a while")
		with gzip.open(TITLES,'wb') as t:
			t.write(r.content)
			print("Saved to "+TITLES)
	else:
		with open(TITLES,'wb') as t:
			t.write(r.content)
			print("got new database, saved to "+TITLES)

def writeImage(imgData):
	img = cv2.resize(imgData,(HEIGHT,HEIGHT))
	cv2.imwrite(sys.argv[3],img)
	print("Wrote image to "+sys.argv[3])

HEIGHT = int(sys.argv[2])
#print(sys.argv[1])
match = re.search(r"\[(\w{16}\b)\]",sys.argv[1])
if not match:
	print("no match")
	sys.exit(-1)
titleID = match.group(1)

iconsDir= os.path.join(os.path.expanduser('~'),'.cache','switchIcons')
if not os.path.isdir(iconsDir):
	os.mkdir(iconsDir)

thumbPath = os.path.join(iconsDir,titleID+".jpg")
if os.path.isfile(thumbPath):
	imgData = cv2.imread(thumbPath)
	writeImage(imgData)
else:
	if not os.path.isfile(TITLES) or time.time()-os.stat(TITLES).st_mtime > 604800:
		downloadNewDatabase()

	if USE_COMPRESSION:
		with gzip.open(TITLES,"r") as db:
			j = json.load(db)
	else:
		with open(TITLES,'r') as db:
			j = json.load(db)

	#print(j[titleID])
	if titleID not in j:
		print(titleID +" not present in database")
		sys.exit(-1)
	elif 'iconUrl' not in j[titleID] or j[titleID]['iconUrl'] is None:
		print(titleID+" has no icon.")
		sys.exit(-1)
	
	r = requests.get(j[titleID]['iconUrl'])
	if r.ok:
		with open(thumbPath,'wb') as t:
			t.write(r.content)
		npB = numpy.frombuffer(r.content,dtype=numpy.uint8)
		imgData = cv2.imdecode(npB,flags=1)
		writeImage(imgData)
		
	else:
		print("Failed to obtain image!")
		sys.exit(-1)




	#print(db[titleID])
#requests.get('https://tinfoil.media/repo/db/',
