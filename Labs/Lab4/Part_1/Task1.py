import numpy as np
from scipy import linalg as nla
import csv

def main():
    
    game = algorithm(openFile('Lab4Data.csv'))
    game.kNN()
    pass
    '''
    TODO:
    * Loop the 
    '''

def openFile(file):
    data = []
    with open(file) as csv_file:
        next(csv_file)
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            data.append(row)
        return data

class algorithm:
    def __init__(self, points=[]):
        self.points = points
        
    def kNN(self):
        A = self.points # Dataset
        B = np.random.rand(1,9)
        B_Old = []
        cnt_clusters = []
        print(B)
        for x in range(1,30): # x amount of clusters
            iterations = 0
            while B != B_Old: # Run as long as the centroids changeiterations
                B_Old = B # Write the new centroids to old one
                iterations += 1
                print("MY B",B)
                np.add(B, np.random.rand(1,9)) #Add new point to program
                print("Do dis now", B)
                A = A / np.max(A)
                B = np.array([[4, 5, 6],\
                            [6, 6, 6]]) # Random points
                B = B / np.max(B)

                numPoints = A.shape[0]
                numCentroids = B.shape[0]
                pointNorms = np.reshape(nla.norm(A, axis=1)**2.0, [numPoints, 1])
                centroidNorms = np.reshape(nla.norm(B, axis=1)**2.0, (1, numCentroids))
                
                self.centroids = pointNorms + centroidNorms - 2.0 * np.dot(A, np.transpose(B))
            cnt_clusters.append(x)
            print("Clusters:",x, ", Iterations:", iterations)

    def findOptimal(self):
        pass
    
if __name__ == "__main__":
    main()