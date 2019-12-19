import numpy as np
from sklearn.model_selection import train_test_split
from collections import Counter

'''
Task 1 “A”: Implement k-NN classifier
 Implement k-Nearest Neighbor (k-NN) algorithm to classify driver performance in
Lab5Data.csv. For this task, you are not allowed to use the k-NN function in scikit-learn
library (you need to implement this classification algorithm by your own using python).
In your report, you need to: a) explain the algorithm and b) write the evaluation results of the
classification algorithm.

Task 1 “E”: Implement k-NN regression
• Modify your K-Nearest Neighbor (k-NN) algorithm in task 1A to find a model to fit the
“FuelConsumption” data in Lab4Data.csv. For this task you are not allowed to use the kNN function in scikit-learn library (you need to implement this regression model by
your own using python).
In your report, you need to explain the algorithm and write the evaluation results of the
regression model in your report.
'''

def main():
    # Load data
    data = np.loadtxt(open('Part_1/Lab4Data.csv', "rb"), delimiter=";", skiprows=1)    
    
    # Create training and test set
    Train_set, Test_set = train_test_split(data, test_size=0.2)
    
    # Training set, testset with amount of rows, K, change between 9 and 7
    classifier = prediction(Train_set, Test_set,k=3, excel_pos=7,model_type=1)
    target = [i for *_,i in Test_set]
    #Prediction/Correct Answer: {list(zip(classifier,target))}
    print(f"\nAccuracy: {accuracy(list(zip(classifier,target)))}%")

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

def prediction(train, test_set, k,excel_pos, model_type):
    classes = []
    for test_row in test_set:
        neighbors = knn(train, test_row, k)
        derp = [i[excel_pos] for i in neighbors] # Change to extract different columns
        classes.append(model(derp,model_type))
    return classes

def accuracy(data):
    accuracy = 0 
    for guess,correct in data:
        if guess == correct:
            accuracy += 1
    return accuracy/len(data)


def model(classes, model_type):
    if model_type == 0: # Classification
        return Counter(classes).most_common(1)[0][0]
    elif model_type == 1: # Regression
        return sum(classes) / len(classes)

def euclidean(pos1, pos2):
    sum = 0
    for x,y in zip(pos1,pos2):
        diff = (x - y)
        sum += diff*diff
    return (sum)**.5
    
if __name__ == "__main__":
    main()
