import numpy as np
from sklearn.model_selection import train_test_split
from scipy import linalg as nla
import matplotlib.pyplot as plt
from pylab import rcParams
import seaborn as sns
import csv
'''
Task 1 “A”: Implement k-NN classifier
• Implement k-Nearest Neighbor (k-NN) algorithm to classify driver performance in
Lab5Data.csv. For this task, you are not allowed to use the k-NN function in scikitlearn library (you need to implement this classification algorithm by your own using
python).
'''
def main():
    data = np.loadtxt(open('Part_1/Lab4Data.csv', "rb"), delimiter=";", skiprows=1)
    features = ['Acceleration','Gender','Age','LateralAcceleration','VehicleSpeed','GearChanges','EngineSpeed','FuelConsum','Weight']
    labels = ['DriverPerformance']

    Train_set, Test_set = train_test_split(data, test_size=0.2)
    Input_train = Train_set[:, :8]
    Target_train = Train_set[:, 9]
    Input_test = Test_set[:, :8]
    Target_test =  Test_set[:, 9]
    points = createPoints(Target_train,Input_train)
    print(points)
    # Normalize training set

    #print(Input_train)
    kvarg = {
        'points':points,
        'features':features,
        'labels':labels
    }
    #print(points)
    #showScatter(points)
    print('Init algorithm')
    
    game = algorithm(**kvarg)    
    game.kNN()

def createPoints(x_list, y_2Dlist): # TODO: Optimize
    points = []
    for x, y_list in zip(x_list,y_2Dlist):
        for y in y_list:
            points.append((x,y))
    return points

class algorithm:
    def __init__(self, points=None, **kvarg):
        self.points = np.array(points).astype(np.float)
        
    def kNN(self):
        A = self.points # Dataset
        B = np.random.rand(1,1)

        print(A)
        for x in range(1,30): # x amount of clusters
            B = np.vstack([B,np.random.rand(1,1)]) #Add new point to program
            
            A = A / np.max(A) # Normalise
            B = B / np.max(B) # Normalise

            numPoints = A.shape[0]
            numCentroids = B.shape[0]
            pointNorms = np.reshape(nla.norm(A, axis=1)**2.0, [numPoints, 1])
            centroidNorms = np.reshape(nla.norm(B, axis=1)**2.0, (1, numCentroids))

            centroids = pointNorms + centroidNorms - 2.0 * np.dot(A, np.transpose(B))
            plt.show(A)
            print("Clusters:",x, ", Iterations:", iterations)

    def findOptimal(self):
        pass
    
if __name__ == "__main__":
    main()