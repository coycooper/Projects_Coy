#!/usr/bin/python

import sys
import csv

#
#
def ReadDict(fn):
        f=open(fn,"rb")
        dict_rap={}
        for key,val in csv.reader(f):
                keyn=int(key)
                dict_rap[keyn] = eval(val)
        f.close()
        return(dict_rap)

#
# Main
#

ratingsFileName    = sys.argv[1]
userDictFileName   = sys.argv[2]
movieDictFileName  = sys.argv[3]
newRatingsFileName = sys.argv[4]
headerFlag         = sys.argv[5]

ratingsFile = open(ratingsFileName,'r')
if headerFlag == 'Y':
	ratingsLines = ratingsFile.readlines()[1:]
else:
	ratingsLines = ratingsFile.readlines()
ratingsFile.close()

newRatingsFile = open(newRatingsFileName,'w')
userIDDict = ReadDict(userDictFileName)
movieIDDict = ReadDict(movieDictFileName)

for r in ratingsLines:
	rSplit = r.split(',')
	userID=int(rSplit[0])
	movieID = int(rSplit[1])
	rating  = float(rSplit[2])
	otherData = int(rSplit[3])
	userIDX =  userIDDict[userID]
	movieIDX = movieIDDict[movieID]
	newRatingsFile.write(str(userIDX) + ',' + str(movieIDX) + ',' + str(rating) + ',' + str(otherData) + '\n')

newRatingsFile.close()
