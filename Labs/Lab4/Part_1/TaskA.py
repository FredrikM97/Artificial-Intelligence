import numpy as np
from sklearn.model_selection import train_test_split
from collections import Counter

def main():
    # Load data
    data = np.loadtxt(open('Part_1/Lab4Data.csv', "rb"), delimiter=";", skiprows=1)    
    
    # Create training and test set
    Train_set, Test_set = train_test_split(data, test_size=0.2)
    
    # Training set, testset with amount of rows, and K
    classifier = prediction(Train_set, Test_set[:5],3)
    target = [i for *_,i in Test_set[:5]]
    print("Prediction/Correct Answer:",list(zip(classifier,target)))
    '''
    TODO:
    * Calculate accuracy
    * Try to plot (Maybe not)
    * 
    '''

def knn(train, test_row, k):
    distance = [(euclidean(test_row, train_row),train_row) for train_row in train]
    distance.sort()
    return [row for distance,row in distance[:k]]

def prediction(train, test_set, k):
    classes = []
    for test_row in test_set:
        neighbors = knn(train, test_row, k)
        derp = [i for *_,i in neighbors] # Change to extract different columns
        classes.append(model(derp,0))
    return classes

def model(classes, type):
    if type == 0: # Classification
        return Counter(classes).most_common(1)[0][0]
    elif type == 1: # Regression
        return sum(classes) / len(classes)

def euclidean(pos1, pos2):
    sum = 0
    for x,y in zip(pos1,pos2):
        diff = (x - y)
        sum += diff*diff
    return (sum)**.5
    
if __name__ == "__main__":
    main()
