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
print(TITLES)
assert len(sys.argv) == 4

TYPE_UPD = 1
TYPE_DLC = 2


HEIGHT = int(sys.argv[2])
#print(sys.argv[1])
match = re.search(r"\[(\w{16}\b)\]",sys.argv[1])
if not match:
	print("no match")
	sys.exit(-1)
titleID = match.group(1).upper()
pkgType=0
if titleID[-3]=='8':
	s=list(titleID)
	s[-3]='0'
	titleID="".join(s)
	pkgType=TYPE_UPD
	print("This is an update")
s=list(titleID)
s[-1]='0'
s[-2]='0'
s[-3]='0'
s[-4]=hex(int(s[-4],16)-1)[2:].upper()
baseTitleID="".join(s)
#print(baseTitleID)

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

def writeImage(imgData,pkgType = 0):
	if pkgType != 0:
		if pkgType == TYPE_DLC:
			writeStr = "DLC"
			try:
				dlcNum = int(titleID[-3:],16)
				print(dlcNum)
				writeStr=writeStr+" "+str(dlcNum)
			except:
				
				pass
		elif pkgType == TYPE_UPD:
			writeStr = "UPD"
			match = re.search(r"\[v(\d+)\]",sys.argv[1])
			if match:
				try:
					updateNum = int(match.group(1))>>16
					print(updateNum)
					writeStr=writeStr+" "+str(updateNum)
				except:
					pass
			else:
				print("Update version string missing")
		img = cv2.putText(imgData,writeStr,(20,150),cv2.FONT_HERSHEY_SIMPLEX,6,(0,0,0,255),35,cv2.LINE_AA)
		img = cv2.putText(imgData,writeStr,(20,150),cv2.FONT_HERSHEY_SIMPLEX,6,(255,255,255,255),15,cv2.LINE_AA)
	img = cv2.resize(imgData,(HEIGHT,HEIGHT))
	cv2.imwrite(sys.argv[3],img)
	print("Wrote image to "+sys.argv[3])


iconsDir= os.path.join(os.path.expanduser('~'),'.cache','switchIcons')
if not os.path.isdir(iconsDir):
	os.mkdir(iconsDir)

thumbPath = os.path.join(iconsDir,titleID+".jpg")
baseThumbPath = os.path.join(iconsDir,baseTitleID+".jpg")
if os.path.isfile(thumbPath):
	imgData = cv2.imread(thumbPath)
	writeImage(imgData,pkgType)
elif os.path.isfile(baseThumbPath):
	print("DLC detected.")
	imgData = cv2.imread(baseThumbPath)
	writeImage(imgData,TYPE_DLC)
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
	elif baseTitleID in j and j[baseTitleID]['iconUrl'] is not None:
		r = requests.get(j[baseTitleID]['iconUrl'])
		if r.ok:
			with open(baseThumbPath,'wb') as t:
				t.write(r.content)
			npB = numpy.frombuffer(r.content,dtype=numpy.uint8)
			imgData = cv2.imdecode(npB,flags=1)
			writeImage(imgData,TYPE_DLC)
	elif 'iconUrl' not in j[titleID] or j[titleID]['iconUrl'] is None:
		print(titleID+" has no icon.")
		sys.exit(-1)
	else:
		r = requests.get(j[titleID]['iconUrl'])
		if r.ok:
			with open(thumbPath,'wb') as t:
				t.write(r.content)
			npB = numpy.frombuffer(r.content,dtype=numpy.uint8)
			imgData = cv2.imdecode(npB,flags=1)
			writeImage(imgData,pkgType)
		else:
			print("Failed to obtain image!")
			sys.exit(-1)
	#print(db[titleID])
#requests.get('https://tinfoil.media/repo/db/',
