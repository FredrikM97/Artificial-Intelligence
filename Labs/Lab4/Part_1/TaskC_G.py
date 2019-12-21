import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from operator import itemgetter

'''
Task 1 “C”: Parameter tuning
• Use cross-validation and try different parameters for k-NN classifiers: change the number of
neighbors and change the distance measurement method.
'''
def main():
    k_list = list(range(1,15))
    metrics = [
        ('euclidean'),
        ('manhattan'),
        ('chebyshev'),
    ]
    
    data = np.loadtxt(open('Lab4Data.csv', "rb"), delimiter=";", skiprows=1)

    np.random.seed(420)
    Train_set, Test_set = train_test_split(data, test_size=0.2)
    
    #inputLabels, targetLabels,classifiers = classification()
    inputLabels, targetLabels,classifiers = regression()

    Input_train = normalizeData(Train_set[:, inputLabels])
    Target_train = Train_set[:, targetLabels]
    Input_test = normalizeData(Test_set[:, inputLabels])
    Target_test =  Test_set[:, targetLabels]

    print('Training:', len(Train_set),'Testing:', len(Test_set))
    
    # Modified neighbors and different metrics
    for classifier in classifiers:
        statistics = []
        
        for k in k_list:
            for metric in metrics:
                classy = classifier(k, metric=metric)
                model = classy.fit(Input_train, Target_train)
                PredictedOutcome = model.predict(Input_test)
                Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])
                accuracy = (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100
                scores = cross_val_score(model, Input_train, Target_train, cv=5) # Cross validation
                
                statistics.append((k,metric, round(float(accuracy),2),scores))
                


        print("\nClassifier:",str(classifier.__name__))
        for (neighboor, name, accuracy, scores) in sorted(statistics, key = lambda x: x[2], reverse=True):
            print(name, ":", neighboor, ":",accuracy,"%", "Crossval:",scores)

def classification():
     # The target for classification is driver performance
    inputLabels = [0,1,2,3,4,5,6,7,8]
    targetLabels=9
    classifiers =[
        KNeighborsClassifier
    ]

    return inputLabels, targetLabels,classifiers
    


def regression():
    # The target for regression is FuelConsumption
    inputLabels = [0,1,2,3,4,5,6,8,9]
    targetLabels=7
    classifiers = [
        KNeighborsRegressor
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