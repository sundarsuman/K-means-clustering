import numpy as np
import random
from collections import Counter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


# 3-dimensional plot showing clusters
def plot(file_input,file_output):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection = '3d')
	X,Y,Z = [],[],[]
	for line in file_input:
		[x,y,z] = map(float,line.strip().split())
		X.append(x)
		Y.append(y)
		Z.append(z)

	A,B,C = [],[],[]
	for line in file_output:
		[a,b,c] = map(float,line.strip().split())
		A.append(a)
		B.append(b)
		C.append(c)

	ax.scatter(X,Y,Z, c='b', marker ='o')
	ax.scatter(A,B,C, c='r', marker ='x')

	plt.show()

# Inputs from points.txt
points = {}
with open('points.txt','r') as f:
	obj = list(enumerate(f))
	for point in obj:
		points[point[0]] = map(float,point[1].strip().split())

centroids = {}
def initialize_centroid(K):
	for i in range(K):
		arr = []
		for k in range(3):
			arr.append(round(random.uniform(1,10),1))
		centroids[i] = arr

C = {}
def assign_centroids():
	for p1,p2 in points.items():
		min_dist = float('inf')
		for c1,c2 in centroids.items():
			vector = [a_i - b_i for a_i,b_i in zip(p2,c2)]
			# print (p1,p2,c1,c2,(np.linalg.norm(vector)))
			if(min_dist != min(np.linalg.norm(vector),min_dist)):
				min_dist = np.linalg.norm(vector)
				C[p1]=c1



def update_centroids():
	for key in centroids.keys():
		arr = [0,0,0]
		for p,c in C.items():
			if(c == key):
				arr = [a+b for a,b in zip(arr,points[p])]
		try:
			centroids[key] = [x/count[key] for x in arr]
		except:
			print("Zero division error: Reinitializing")
			initialize_centroid(K)

# Input for number of cluster points
print("Input number of clusters K")
K = input()

# Initializing and iterating through cluster assignment and update
initialize_centroid(K)
centroids_prev = {}
while cmp(centroids_prev,centroids)!=0:
	assign_centroids()
	count = Counter(values for values in C.values())
	centroids_prev = dict(centroids)
	update_centroids()


# Output to clusters.txt	
f = open('clusters.txt','w')
for key,value in centroids.items():
	centroids[key] = [ round(elem, 2) for elem in value ]
	f.write(' '.join(str(v) for v in centroids[key])+"\n")
f.close()

# Plotting the results
f_out = open('clusters.txt','r')
f_in = open('points.txt','r')
plot(f_in,f_out)
f_out.close()
f_in.close()
 
