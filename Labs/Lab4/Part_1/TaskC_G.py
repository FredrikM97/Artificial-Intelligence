import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from operator import itemgetter
from sklearn.preprocessing import normalize

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
    classifiers = [KNeighborsClassifier,KNeighborsRegressor]
    data = np.loadtxt(open('Part_1/Lab4Data.csv', "rb"), delimiter=";", skiprows=1)

    np.random.seed(420)
    Train_set, Test_set = train_test_split(data, test_size=0.2)
    
    '''
    TODO: FIX CROSSVALIDATION
    '''

    Input_train = normalizeData(Train_set[:, :8])
    Target_train = Train_set[:, 9]
    Input_test = normalizeData(Test_set[:, :8])
    Target_test =  Test_set[:, 9]

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