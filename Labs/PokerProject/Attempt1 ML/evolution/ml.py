import numpy as np
from sklearn.model_selection import train_test_split,cross_val_score

from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import warnings
import copy

'''
TODO:
Parameters:
INFO:
    RANKS: No point in checking since we dont know until after? What happens if they play risky with bad hand
        0: highcard, 
        1: onepair, 
        2: twopair, 
        3: 3ofakind, 
        4: straight,
        5: flush, 
        6: fullhouse,
        7: 4ofakind, 
        8: straightflush    
        Unknown: -1

    ACTION: 
        Fold: 0, 
        Call: 1, 
        Raise: 2, 
        Allin: 3
        Open: 4
        Check: 5
        Unknown: -1

All data for training:
    Sample	p1HandCategory	p1HandRank	p1Coin	p1AvgRaise	p1RaiseRatio	p2HandCategory	p2HandRank	p2Coin	p2AvgRaise	p2RaiseRatio	p1Action1	p1RaiseCoin1	p2Action1	p2RaiseCoin1	p1Action2	p1RaiseCoin2	p2Action2	p2RaiseCoin2	p1Action3	p1RaiseCoin3	p2Action3	p2RaiseCoin3	p1Action4	p1RaiseCoin4	p2Action4	p2RaiseCoin4	p1CntRaises	p2CntRaises

Known at the beginning: 
    Sample	p1HandCategory	p1HandRank	p1Coin	p1AvgRaise	p1RaiseRatio, p2Coin, p2AvgRaise	p2RaiseRatio

Actions: Only check between two users at a time, take best action after checking everyone
    p1Action1		p2Action1		
    p1Action2		p2Action2		
    p1Action3		p2Action3		
    p1Action4		p2Action4		

Interesting actions:
    Open & Betting

Statistics: 
    p1CntRaises	p2CntRaises

Unknown until after one round: 
    p2HandCategory	p2HandRank

What player1 knows before doing action:
    [Player2] = [Sample, p1HandCategory,p1HandRank,p1Coin,p1AvgRaise,p1RaiseRatio, p2Coin,p2AvgRaise,p2RaiseRatio, p1CntRaises, p2CntRaises, Actionsx3]]

Interesting data and what to expect:
    Input: [Round, p1HandCategory,p1HandRank, p1Coin, p2Coin, Actionsx3]]
    Target: [p2HandRank] # The higher value the better - Not gonna work on server since we are never told what opponents have, Which is stupid

Notes:
Raise removed to minimize model, sample=Rounds
'''



def generateModel():
    warnings.filterwarnings("ignore")

    # Define training stuff
    classifiers =[('Nearest Neighbors Classification',KNeighborsClassifier(5))]
    metrics = [('manhattan')]
    # Agents to check towards, Currently only opponent
    agents = ['p2']

    train_set, test_set,kwarg = preprocessing()
    print(f'Training: {len(train_set)} Testing: {len(test_set)}\n')

    statistics = []
    for agent in agents: # Create model for each agent
        models = train(agent,classifiers,**kwarg)
        predictions = analyseModel(models, **kwarg)
        statistics.append(predictions)

    for classType, agent, validation_avg,accuracy in sorted(statistics[0], key = lambda x: x[2], reverse=True):
        print(f'{classType}, {agent}, Validation_avg: {round(validation_avg,2)}%')

def determineAction():
    '''
    Determine which action to take based on results from the Model on all players
    '''

def preprocessing():
    '''
    Use same data as Lab4, this will decide what we do next
    '''
    data = np.loadtxt(open("pokerStatistic.csv", "rb"), delimiter=",", skiprows=1) 

    # Training label of p1 is included since we only try to predict p2
    inputLabels = list(range(0,13)) 
    # Target labels
    targetLabel=list(range(14,15)) 

    Train_set, Test_set = train_test_split(data, test_size=0.2)

    # Working for two agents only
    Input_train = Train_set[:, inputLabels]    
    Target_train = Train_set[:, targetLabel] 

    Input_test = Test_set[:, inputLabels] # Should be Test_set
    Target_test = Test_set[:, targetLabel]

    kwarg = {
        'Input_train':Input_train,
        'Target_train':Target_train,
        'Input_test':Input_test, 
        'Target_test':Target_test,
    }
    
    return Train_set, Test_set, kwarg

def structureInputSet():
    '''
    * Import data
    * Create dataset for each player
    * Categorise data to what each player sees
    '''
    '''
    (playerName,{
        round, 
        Action,
        Chips,
        
    } )
    '''


def train(agent,
            classifiers, 
            Input_train=None, 
            Input_test=None,
            Target_train=None, 
            **kwarg
        ):
    '''
    * Generate a fit model for each classifier
    * Returns the models as a list
    '''
    models = []
    
    for name, classifier in classifiers:
        models.append((name,agent,classifier.fit(Input_train,Target_train)))

    return models

def analyseModel(
            models,
            Input_test=None, 
            Input_train=None,
            Target_test=None, 
            **kwarg):
    '''
    * Predict the fit model
    * Returns Classification type, agent, validation_avg, accuracy 
    '''
    
    model_accuracy = []
    
    for Classtype, agent, dataModel in models:
        predict = predictData(dataModel,Input_test)

        correct_predict = len([i for i, j in zip(predict, Target_test) if i == j])
        validation = cross_val_score(dataModel, Input_test, Target_test, cv=5)
        accuracy = (correct_predict/float(len(predict)))*100
        validation_avg = sum(validation)/float(len(validation))*100 # Calculate average validation

        model_accuracy.append((Classtype, agent, validation_avg,accuracy))
    return model_accuracy

def save():
    pass
def load():
    pass
def predictData(dataModel,inputData):
    return dataModel.predict(inputData)

if __name__ == "__main__":
    generateModel()
