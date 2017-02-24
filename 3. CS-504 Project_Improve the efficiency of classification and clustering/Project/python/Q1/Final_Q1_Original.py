# 0. import modula
import numpy as np
import pandas as pd
import math
import pdb
import csv

# 2. Load the data
header = ['user_id', 'movie_id', 'rating', 'timestamp']
df = pd.read_csv('ratings.csv', sep=',', names=header)
n_users = df.user_id.unique().shape[0]
n_movies = df.movie_id.unique().shape[0]
print 'Number of users = ' , n_users , ' | Number of movies = ' , n_movies

train_data = df
#test_data = pd.read_csv('testing-input.csv', sep=',', names=header)
test_data = pd.read_csv('ratings_test_10_v2.csv', sep=',', names=header)

# 3.1. Create the hash table
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

# 3.2. Create the matrix for this project
train_data_matrix = np.zeros((n_users, n_movies))
for line in train_data.itertuples():
    matrix_user = userid_dict[str(line[1])]
    matrix_movie = movieid_dict[str(line[2])]
    train_data_matrix[matrix_user][matrix_movie] = line[3]

# 3.3. build the distance function
def distance(user1, user2, length):
    d = 0
    for x in range(length):
        d += pow((user1[x] - user2[x]), 2)
    return math.sqrt(d)

# 3.4. get the K nearest neighbors
def GetNeighbors(DD, k):
    Order = sorted(enumerate(DD), key=lambda x:x[1])
    
    neighbors = []
    x=0
    y=0
    l=len(Order)
    while (y<k) and (x<l):
        if (Order[x][1]!=0) and (train_data_matrix[Order[x][0]][movie]!=0):
            	neighbors.append(Order[x])
            	y+=1
        x+=1
        
    return neighbors

D_matrix = np.zeros((n_users, n_users))

#pdb.set_trace()    

#csvfile = file('testing-output.csv', 'wb')
csvfile = file('final_Q1.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['UserID', 'MovieID', 'k','Real Rating','Predicting','Nearest Neighbors'])
for line in test_data.itertuples():
    answer = []
    user = userid_dict[str(line[1])]
    movie = movieid_dict[str(line[2])]
    answer.append(str(line[1]))
    answer.append(str(line[2]))

    for x in range(n_users):
        if train_data_matrix[x][movie]!=0 :
            if (x!=user) and (D_matrix[user][x]==0) :
                D_matrix[user][x]=distance(train_data_matrix[user],train_data_matrix[x],n_movies)
                D_matrix[x][user]=D_matrix[user][x]
    dist = D_matrix[user]
                
    k=3
    answer.append(str(k))
    answer.append(str(line[3]))
    KNN = GetNeighbors(dist,k)
##    print KNN
    s=0.0
    an=""
    l=len(KNN)
    for i in range(l):
        s+=train_data_matrix[KNN[i][0]][movie]
        an+=str(KNN[i][0]+1)+"("+str(KNN[i][1])+") "
    answer.append("%.1lf"%(s/k))
    answer.append(an)
    writer.writerow(answer)
    del answer[5]
    answer[0]=''
    answer[1]=''
    answer[3]=''

    k=5
    answer[2]=str(k)
    KNN = GetNeighbors(dist,k)
    s=0.0
    l=len(KNN)
    for i in range(l):
        s+=train_data_matrix[KNN[i][0]][movie]

    answer[4]=str(s/k)
    writer.writerow(answer)

    k=10
    answer[2]=str(k)
    KNN = GetNeighbors(dist,k)
    s=0.0
    l=len(KNN)
    for i in range(l):
        s+=train_data_matrix[KNN[i][0]][movie]
    answer[4]=str(s/k)
    writer.writerow(answer)

csvfile.close()
