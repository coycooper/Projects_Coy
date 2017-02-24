#!/usr/bin/python

## build the dictionaries for userid and movie IDs

import sys
import csv

if len(sys.argv) != 4:
	print('usage: buildDictionary.py ratingsFile userDictionary movieDictionary')
	sys.exit(99)

ratingsFileName    = sys.argv[1]
userDictFileName   = sys.argv[2]
movieDictFileName   = sys.argv[3]

ratingsFile   = open(ratingsFileName,'r')
ratingsLines  = ratingsFile.readlines()[1:]  ## skip HEADER line 
ratingsFile.close()

nextUserID  = 0
nextMovieID = 0

userIDDict   = {}
movieIDDict  = {}

def DumpDict(dictToDump,fileName):
	dumpFile = open(fileName,'w')
	w = csv.writer(dumpFile)
	for key,val in dictToDump.items():
		w.writerow([key,val])
	dumpFile.close()

for r in ratingsLines:
	rSplit  = r.split(',')
	userID  = int(rSplit[0])
	movieID = int(rSplit[1])
	if userID not in userIDDict.keys():
		userIDDict[userID] = nextUserID
		nextUserID += 1
	if movieID not in movieIDDict.keys():
		movieIDDict[movieID] = nextMovieID
		nextMovieID += 1

## now write out the dictionaries to their respective file:
DumpDict(userIDDict,userDictFileName)
DumpDict(movieIDDict,movieDictFileName)
