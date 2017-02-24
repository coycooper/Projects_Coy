#!/bin/bash

## build Python dictionaries to modify userid and movieID
## data such that the indexes (IDs) run from 0 to n-1

## run conversion program on all data

./MakeDictionaries.py ratings_unix.csv UserIDDictionary.dat MovieIDDictionary.dat

 ./ConvertRatingsFiles.py ratings_unix.csv UserIDDictionary.dat MovieIDDictionary.dat ratings_unix_v3.csv Y

 ./ConvertRatingsFiles.py ratings_train_80.csv UserIDDictionary.dat MovieIDDictionary.dat ratings_train_80_v3.csv N
 ./ConvertRatingsFiles.py ratings_train_80.csv UserIDDictionary.dat MovieIDDictionary.dat ratings_train_85_v3.csv N
 ./ConvertRatingsFiles.py ratings_train_80.csv UserIDDictionary.dat MovieIDDictionary.dat ratings_train_90_v3.csv N
 ./ConvertRatingsFiles.py ratings_train_80.csv UserIDDictionary.dat MovieIDDictionary.dat ratings_train_95_v3.csv N


 ./ConvertRatingsFiles.py ratings_test_05_v2.csv UserIDDictionary.dat MovieIDDictionary.dat ratings_test_05_v3.csv N
 ./ConvertRatingsFiles.py ratings_test_10_v2.csv UserIDDictionary.dat MovieIDDictionary.dat ratings_test_10_v3.csv N
 ./ConvertRatingsFiles.py ratings_test_15_v2.csv UserIDDictionary.dat MovieIDDictionary.dat ratings_test_15_v3.csv N
 ./ConvertRatingsFiles.py ratings_test_20_v2.csv UserIDDictionary.dat MovieIDDictionary.dat ratings_test_20_v3.csv N
