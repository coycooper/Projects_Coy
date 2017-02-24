# 0. import modula
import numpy as np
import pandas as pd
import math
import pdb
import csv
import sys


# 1. Load the data
header = ['user_id', 'movie_id', 'rating', 'timestamp']
train_data = pd.read_csv('ratings_train_95.csv', sep=',', names=header)
test_data = pd.read_csv('ratings_test_05_v2.csv', sep=',', names=header)

n_users = train_data.user_id.unique().shape[0]
n_movies = train_data.movie_id.unique().shape[0]
print 'Number of users = ' , n_users , ' | Number of movies = ' , n_movies

# 2. Predict
# 2.1. Create the hash table
userid_dict = {}
matrix_idx = 0
movieid_dict = {}
matrix_idy = 0

for line in train_data.itertuples():
    if str(line[1]) not in userid_dict.keys():
        userid_dict[str(line[1])] = matrix_idx
        matrix_idx += 1
    if str(line[2]) not in movieid_dict.keys():
        movieid_dict[str(line[2])] = matrix_idy
        matrix_idy += 1

print "n_users = " + str(n_users) + ' , ' + "matrix_idx = " + str(matrix_idx)
print "n_movies = " + str(n_movies) + ' , ' + "matrix_idy = " + str(matrix_idy)

# 2.2. Create the matrix for this project and calculate the average
train_data_matrix = np.zeros((n_users, n_movies))
n_user_rate = np.zeros(n_users)
s_user_rate = np.zeros(n_users)
bar_user = np.zeros(n_users)

for line in train_data.itertuples():
    matrix_user = userid_dict[str(line[1])]
    matrix_movie = movieid_dict[str(line[2])]
    train_data_matrix[matrix_user][matrix_movie] = line[3]
    n_user_rate[matrix_user] += 1
    s_user_rate[matrix_user] += line[3]
    
for i in range(n_users):
    bar_user[i]=s_user_rate[i]/n_user_rate[i]
    
# 2.3. Build the similarity function
def sim(movie1, movie2, user_set):
    s1 = 0.0
    s2 = 0.0
    s3 = 0.0
    for i in range(len(user_set)):
        diff1=train_data_matrix[user_set[i]][movie1]-bar_user[user_set[i]]
        diff2=train_data_matrix[user_set[i]][movie2]-bar_user[user_set[i]]
        s1 += diff1 * diff2
        s2 += diff1 * diff1
        s3 += diff2 * diff2
    if (s2==0) or (s3==0):
        return 1
        print 'movie1:',movie1
        print 'movie2:',movie2
        print user_set
        
    return (s1/ ( math.sqrt(s2) * math.sqrt(s3) ) )

# 2.4. Get the user set
csvfile = file('final_Q2_Output.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['userID', 'movieID', 'realRating','predictedRating'])

SSE = 0
S_matrix = np.zeros((n_movies, n_movies))
for line in test_data.itertuples():
    answer = []
    user = userid_dict[str(line[1])]
    movie = movieid_dict[str(line[2])]
    answer.append(str(line[1]))
    answer.append(str(line[2]))
    answer.append(str(line[3]))

    for m in range(n_movies):
        if (m!=movie) and (S_matrix[movie][m] ==0)and (train_data_matrix[user][m] != 0):
            US=[]
            for u in range(n_users):
                if (train_data_matrix[u][movie]!=0) and (train_data_matrix[u][m]!=0):
                    US.append(u)
            if (len(US)!=0):
                S_matrix[movie][m] = sim(m, movie, US)
                S_matrix[m][movie] = S_matrix[movie][m]
            
    s1 = 0.0
    s2 = 0.0
    for m in range(n_movies):
        if (m!=movie) and (train_data_matrix[user][m] != 0) and (S_matrix[m][movie]>0):
            s1 += S_matrix[movie][m]*train_data_matrix[user][m]
            s2 += S_matrix[movie][m]
#    print user, movie
    if s2!=0:
        pred = s1/s2
    else:
        print "s2=0, user:", user, ",movie:", movie
        pred = bar_user[user]
        
    answer.append("%.1lf"%(pred))
    SSE += pow((pred - line[3]), 2)
    writer.writerow(answer)

print 'SSE: ',SSE

n = len(test_data)
RMSE = math.sqrt(SSE)/n
print 'RMSE: ', RMSE
csvfile.close()
