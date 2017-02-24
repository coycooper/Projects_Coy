Short description of files:

MakeDictionaries.py 
  Short python program that reads in the FULL writing file (ratings_unix.csv) 
  and builds two CSV files, one for userids and the other for movieids.
  These csv files list the original file first followed by the converted
  value. These converted values REINDEX the data such that the ids now
  go from 0 to n-1 with no gaps.  Thus, these new values can be used
  as INDEXES to your matrices.

ConvertRatingsFile.py
  This short python program reads the dictionaries created by 
  MakeDictionaries.py and recodes the supplied ratings file such
  that the indices for userIDs and movieIDs are converted into
  their cooresponding 0 to n-1 assignment. 

ConvertFiles.sh (Has already been run, I just included it for your info)
  Runs MakeDictionaries.sh and then ConvertRatingsFile.py on all
  files (the original ratings_unix.csv file followed by the training
  and test sets).  All converted files are named with _v3.


