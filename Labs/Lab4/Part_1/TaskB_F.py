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
    classifiers =[
        ('Nearest Neighbors Classification',KNeighborsClassifier(5)),
        ('SVC Classification',svm.SVC(kernel='linear', C=1.0)),
        ('Decision Tree Classification',DecisionTreeClassifier(max_depth=5)),
        ('Random Forest Classification',RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)),
        ('Nearest Neighbors Regression',KNeighborsRegressor(5)),
        ('Linear Regression',LinearRegression()),
        ('Random Forest Regression',RandomForestRegressor(max_depth=5, n_estimators=10, max_features=1))
    ]
   
    data = np.loadtxt(open('Part_1/Lab4Data.csv', "rb"), delimiter=";", skiprows=1)
    Train_set, Test_set = train_test_split(data, test_size=0.2)
    data_params = np.reshape(['Acceleration''Gender','Age'	'LateralAcceleration','VehicleSpeed','GearChanges','EngineSpeed','FuelConsu,','Weight','DriverPerformance'], (-1,1))

   

    Input_train = Train_set[:, :8]
    Target_train = Train_set[:, 9]

    Input_test = Test_set[:, :8]
    Target_test =  Test_set[:, 9]

    print('Training:', len(Train_set),'Testing:', len(Test_set))
    
    for name, classy in classifiers:
        model = classy.fit(Input_train, Target_train)
        PredictedOutcome = model.predict(Input_test)
        Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])
        print('Type:',name,'Accuracy:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100,"%")

if __name__ == "__main__":
    main()