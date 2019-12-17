import numpy as np
from scipy import linalg as nla
import csv
'''
Task 1 “A”: Implement k-NN classifier
• Implement k-Nearest Neighbor (k-NN) algorithm to classify driver performance in
Lab5Data.csv. For this task, you are not allowed to use the k-NN function in scikitlearn library (you need to implement this classification algorithm by your own using
python).
'''
def main():
    
    game = algorithm(openFile('Part_1/Lab4Data.csv'))
    game.kNN()
    pass


def openFile(file):
    data = []
    with open(file) as csv_file:
        next(csv_file)
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            data.append(row[9])
        return data

class algorithm:
    def __init__(self, points=[]):
        self.points = points
        
    def kNN(self):
        A = np.array(self.points).astype(np.float) # Dataset
        B = np.random.rand(1,1)
        centroids = 1
        centroids_Old = []
        for x in range(1,30): # x amount of clusters
            B = np.vstack([B,np.random.rand(1,10)]) #Add new point to program
            iterations = 0
            while not np.array_equal(centroids,centroids_Old) or iterations != 0: # Run as long as the centroids changeiterations
                centroids_Old = centroids
                iterations += 1
                
                
                A = A / np.max(A) # Normalise
                B = B / np.max(B) # Normalise

                numPoints = A.shape[0]
                numCentroids = B.shape[0]
                pointNorms = np.reshape(nla.norm(A, axis=1)**2.0, [numPoints, 1])
                centroidNorms = np.reshape(nla.norm(B, axis=1)**2.0, (1, numCentroids))

                centroids = pointNorms + centroidNorms - 2.0 * np.dot(A, np.transpose(B))
                print("Centroids:",centroids)
            print("Clusters:",x, ", Iterations:", iterations)

    def findOptimal(self):
        pass
    
if __name__ == "__main__":
    main()