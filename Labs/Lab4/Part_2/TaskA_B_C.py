import numpy as np
from sklearn.model_selection import train_test_split,cross_val_score

from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import warnings
import copy

'''
TODO:
Availible info: hand category, hand rank, amount of money
Problems: Expand to make list that handles all input (one hot encoding ish)

INFO:
*   RANKS: 
        0: highcard, 
        1: onepair, 
        2: twopair, 
        3: 3ofakind, 
        4: straight,
        5: flush, 
        6: fullhouse,
        7: 4ofakind, 
        8: straightflush
*   ACTION: 
        Fold: 0, 
        Call: 1, 
        Raise: 2, 
        Allin: 3
        NoData: -1 


Columns: 

Sample, p1HandCategory, p1HandRank, p1Coin, p1AvgRaise, p1RaiseRatio, p2HandCategory, p2HandRank, p2Coin, p2AvgRaise, p2RaiseRatio
p1Action1, p1RaiseCoin1...
'''
def main():
    warnings.filterwarnings("ignore")
    classifiers =[
        ('Nearest Neighbors Classification',KNeighborsClassifier(5)),
        ('SVC Classification',svm.SVC(kernel='linear', C=1.0)),
        ('Random Forest Classification',RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)),
    ]
    metrics = [
            ('euclidean'),
            ('manhattan'),
            ('chebyshev'),
    ]
    agents = ['p1','p2']

    train_set, test_set,kwarg = preprocessing()

    print(f'Training: {len(train_set)} Testing: {len(test_set)}\n')

    singleRun(agents,classifiers, metrics,**kwarg)
    crossValidation(agents,metrics,k_list=10,**kwarg)

    
def singleRun(agents,classifiers, metrics,**kwarg):
    '''
    Task 2-B
    * Start each process
    '''
    for agent in agents: # Create model for each agent
        models = generateModel(agents,classifiers,**kwarg)
        predictions = prediction(models, **kwarg)
    
        for classType, agent, validation_avg,_ in predictions:
            print(f'{classType}, {agent}, Validation_avg: {round(validation_avg,2)}%')

def preprocessing():
    '''
    * Load data into the program
    * Split up into training sets
    * Return name_space 
    '''

    data = np.loadtxt(open("pokerStatistic.csv", "rb"), delimiter=";", skiprows=1) 
    inputLabels = list(range(0,29)) # Training label of p1 is included since we only try to predict p2
    p1_targetLabel=29
    p2_targetLabel=30

    Train_set, Test_set = train_test_split(data, test_size=0.2)

    # Working for two agents only
    Input_train = Train_set[:, inputLabels]    
    Target_train_p1 = Train_set[:, p1_targetLabel] 
    Target_train_p2 = Train_set[:, p2_targetLabel]

    Input_test = Train_set[:, inputLabels] # Should be Test_set
    Target_test_p1 = Train_set[:, p1_targetLabel]
    Target_test_p2 = Train_set[:, p2_targetLabel]

    kwarg = {
        'Input_train':Input_train,
        'Target_train_p1':Target_train_p1,
        'Target_train_p2':Target_train_p2,
        'Input_test':Input_test, 
        'Target_test_p1':Target_test_p1,
        'Target_test_p2':Target_test_p2
    }
    
    return Train_set, Test_set, kwarg

def generateModel(agent,
            classifiers, 
            Input_train=None, 
            Input_test=None,
            Target_train_p1=None,
            Target_train_p2=None, 
            **kwarg
        ):
    '''
    * Generate a fit model for each classifier
    * Returns the models as a list
    '''
    models = []
    
    for name, classifier in classifiers:
        models.append((name,agent,classifier.fit(Input_train,Target_train_p1)))

    return models

def prediction(
            models,
            Input_test=None, 
            Input_train=None,
            Target_test_p1=None, 
            Target_test_p2=None,
            **kwarg):
    '''
    * Predict the fit model
    * Returns Classification type, agent, validation_avg, accuracy 
    '''
    Target_List = { # removes the need of if statement
        'p1':Target_test_p1,
        'p2':Target_test_p2
    }
    
    model_accuracy = []
    
    for Classtype, agent, dataModel in models:
        
        predict = dataModel.predict(Input_test)

        correct_predict = len([i for i, j in zip(predict, Target_List[agent]) if i == j])
        validation = cross_val_score(dataModel, Input_train, Target_List[agent], cv=10)
        accuracy = (correct_predict/float(len(predict)))*100
        validation_avg = sum(validation)/float(len(validation))*100 # Calculate average validation

        model_accuracy.append((Classtype, agent, validation_avg,accuracy))
    return model_accuracy

def crossValidation(
            agents,
            metrics, 
            k_list,
            **kwarg
    ):
    '''
    Task 2 C
    * Evaluates with multiple metrics and different amount of neighbors
    '''
    k_list = list(range(1,k_list))
    statistics = []
    best_score = {
        'validation':0,
        'k':0,
        'metric':0
    }

    for agent in agents: # Create model for each agent
        for k in k_list:
            for metric in metrics:
                classifiers =[('Nearest Neighbors',KNeighborsClassifier(k, metric=metric))]
                models = generateModel(agent,classifiers,**kwarg)
                predict = prediction(models,**kwarg)

                if best_score['validation'] < predict[0][2]:
                    best_score['validation'] = predict[0][2] # Validation_Avg
                    best_score['k'] = k
                    best_score['metric'] = metric
                
                statistics.append((metric,k,*predict[0]))

    ## Calculate the best one
    

    # Print data
    print(f'\n{classifiers[0][0]}')
    for metric, k,classifiers, agent, val_avg, accuracy in statistics:
        print(f'{agent}, {metric}, {k} Val: {round(val_avg,2)}%, Acc: {round(accuracy,2)}%')
  
    print("\nBest score:", round(best_score['validation'],2),"%, k:",best_score['k'], "Metric:",best_score['metric'])

if __name__ == "__main__":
    main()