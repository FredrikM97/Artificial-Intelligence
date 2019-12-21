import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression


'''
Task 1 “B”: Investigate different classification algorithms
• Try 3 different classification algorithms from scikit-learn library. For this task, you are
allowed to use the available functions in scikit-learn library.
'''

'''
Classification and regression is included
'''
def main():
    
   
    data = np.loadtxt(open('Lab4Data.csv', "rb"), delimiter=";", skiprows=1)
    Train_set, Test_set = train_test_split(data, test_size=0.2,)
   
    #inputLabels, targetLabels,classifiers = classification()
    inputLabels, targetLabels,classifiers = regression()
   
    Input_train = normalizeData(Train_set[:, inputLabels])
    Target_train = Train_set[:, targetLabels]
    Input_test = normalizeData(Test_set[:, inputLabels])
    Target_test =  Test_set[:, targetLabels]

    print('Training:', len(Train_set),'Testing:', len(Test_set))

    for name, classy in classifiers:
        model = classy.fit(Input_train, Target_train)
        PredictedOutcome = model.predict(Input_test)
        Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])
        print('Type:',name,'Accuracy:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100,"%")

def classification():
     # The target for classification is driver performance
    inputLabels = [0,1,2,3,4,5,6,7,8]
    targetLabels=9
    classifiers =[
        ('Nearest Neighbors Classification',KNeighborsClassifier(5)),
        ('SVC Classification',svm.SVC(kernel='linear', C=1.0)),
        ('Decision Tree Classification',DecisionTreeClassifier(max_depth=5)),
        ('Random Forest Classification',RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)),
    ]

    return inputLabels, targetLabels,classifiers
    


def regression():
    # The target for regression is FuelConsumption
    inputLabels = [0,1,2,3,4,5,6,8,9]
    targetLabels=7

    classifiers = [
        ('Nearest Neighbors Regression',KNeighborsRegressor(5)),
        ('Linear Regression',LinearRegression()),
        ('Random Forest Regression',RandomForestRegressor(max_depth=5, n_estimators=10, max_features=1))
    ]

    return inputLabels, targetLabels,classifiers

# Just for fun
def normalizeData(data):
    normData = []
    for col in zip(*data):
        high = max(col)
        low = min(col)
        col = [item-low/high for item in col]
        normData.append(col)
    return [row for row in zip(*normData)]

if __name__ == "__main__":
    main()