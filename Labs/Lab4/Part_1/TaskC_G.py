import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from operator import itemgetter

'''
Task 1 “C”: Parameter tuning
• Use cross-validation and try different parameters for k-NN classifiers: change the number of
neighbors and change the distance measurement method.
'''
def main():
    neighbors = [1,2,3,4,5,6,7,8]
    metrics = [
        ('euclidean'),
        ('manhattan'),
        ('chebyshev'),
    ]
    classifiers = [KNeighborsClassifier,KNeighborsRegressor]
    data = np.loadtxt(open('Part_1/Lab4Data.csv', "rb"), delimiter=";", skiprows=1)


    Train_set, Test_set = train_test_split(data, test_size=0.2)

    Input_train = Train_set[:, :8]
    Target_train = Train_set[:, 9]
    Input_test = Test_set[:, :8]
    Target_test =  Test_set[:, 9]

    print('Training:', len(Train_set),'Testing:', len(Test_set))
    
    # Modified neighbors and different metrics
    for classifier in classifiers:
        statistics = []
        
        for neighbor in neighbors:
            for metric in metrics:
                classy = classifier(neighbor, metric=metric)
                model = classy.fit(Input_train, Target_train)
                PredictedOutcome = model.predict(Input_test)
                Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])
                accuracy = (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100
                statistics.append((neighbor,metric, round(float(accuracy),2)))

        print("\nClassifier:",str(classifier.__name__))
        for (neighboor, name, accuracy) in sorted(statistics, key = lambda x: x[2], reverse=True):
            print(name, ":", neighboor, ":",accuracy,"%")
            
if __name__ == "__main__":
    main()