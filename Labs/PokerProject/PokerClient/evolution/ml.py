'''
Builds a poker classifier from mined poker data.

The encoding used for the poker actions is:
ACTION: 
    Forced_Bet: 0,
    Player_Open: 1,
    Player_Check: 2,
    Player_Fold: 3,
    Player_Call: 4, 
    Player_Raise: 5, 
    Player_All-in: 6,
    None: 7

Example input data:
[-1, 40, 0, 40, 70, 'Forced_Bet', 'Player_Fold', 'Forced_Bet', 'Player_Fold', 'Forced_Bet', 'Player_Check']
[-1, 50, 0, 50, 50, 'Forced_Bet', 'Player_Fold', 'Forced_Bet', 'Player_Fold', 'Forced_Bet', None]

Meaning of input data:
[targetHandStrength, targetChips, targetWin, p1Chips,p2Chips, targetAction1,targetAction2, p1Action1,p1Action2, p2Action1, p2Action2]

TODO:
-Figure out what our label is. Suggest starting in the other end a.k.a the client.
    If we predict ALL actions that result in win:
        Pro:
            +More true to reality
            +Only three outputs
            +Output make sense in all contexts
        Con:
            -Needs to be parsed into an action
            -Has to iterate all possible actions

    If we predict WHAT action that result in win:
        Pro:
            +Output directly translate into action
            +We know the output has the highest likelihood
        Con:
            -Can only train on winning cases
            -Might output invalid actions
    
-Decide classifier (and document why for the report). Suggested ones (assuming we'll use scikit):
    real name               scikit name                                                             
    k-nn                    KNeighborsClassifier(3),
    RBF SVM                 SVC(gamma=2, C=1),
    Random forest           RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    Neural net              MLPClassifier(alpha=1, max_iter=1000),

IF TIME is TRUE:
# FIXME: Do we know the opponents action on current turn? Most likely no. Yet it's in the training data. 
'''

import numpy as np
import pandas as pd
import warnings
import copy
from itertools import repeat, product
from typing import List

from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
#from sklearn.utils.testing import ignore_warnings
#from sklearn.exceptions import ConvergenceWarning
import warnings

#warnings.filterwarnings("ignore") #TODO: Remove this
# Setup 
actions_per_player  = 2
encoding_size       = 7
number_of_players   = 5
number_of_actions   = actions_per_player * encoding_size * number_of_players

def main():
    Input_train, Target_train, Input_test, Target_test, *_ = init()
    #test_classifiers(Input_train, Target_train, Input_test, Target_test)
    parameter_tuning(Input_train, Target_train, Input_test, Target_test)

def create_model(ABS_PATH):
    Input_train, Target_train, Input_test, Target_test, process, args = init(ABS_PATH)
    classifier = SVC(C=2.5, kernel='linear',gamma='scale',probability=True)
    return classifier.fit(Input_train+Input_test, Target_train+Target_test), process, args

def test_classifiers(Input_train, Target_train, Input_test, Target_test):
    classifiers = [
        SVC(C=2.5, kernel='linear'),
        RandomForestClassifier(max_depth=None, criterion='gini', n_estimators=115, max_features='auto'),
        MLPClassifier(hidden_layer_sizes=(100,50), alpha=2, solver='lbfgs',batch_size=50,max_iter=1000),
    ]
    # run all classifiers
    for classifi in classifiers:
        predictions = classifi.fit(Input_train, Target_train).predict(Input_test)
        name = classifi.__doc__.split('.')[0]
        print(f'Accuracy: {accuracy(Target_test, predictions)}\tClassifier: {name}')

def parameter_tuning(Input_train, Target_train, Input_test, Target_test):
    # prepare some classifiers from scikit library
    classifiers = [
        SVC,
        RandomForestClassifier,
        MLPClassifier,
    ]
    params = [  
        {'C':[0.5,1.0,2.0,3.0,4.0],'kernel':['rbf', 'linear','poly'],'gamma':['scale']},
        {'max_depth':[None,10],'criterion':['gini','entropy'],'n_estimators':[50,100,150],'max_features':['auto','log2']},
        {'hidden_layer_sizes':[(100,),(50,50,50)],'solver':['lbfgs', 'adam'],'batch_size':[40,50],'alpha':[1],'max_iter':[1000]}
    ]
    # run all classifiers
    for classifi, params in zip(classifiers,params):
        cross_valid_example(classifi,params)

def cross_valid_example(classifier,params):
    Input_train, Target_train, Input_test, Target_test, *_ = init()
    
    # do cross validation
    name = classifier.__doc__.split('.')[0]
    score = cross_valid_testing(classifier, Input_train, Target_train, params,5)
    
    # present parameters and result
    score.sort(key=lambda x:x[0], reverse=True)
    
    best = max(score, key=lambda x:x[0])
    acc, kwargs = best
    classi = classifier(**kwargs)
    classi.fit(Input_train, Target_train)
    predictions = classi.predict(Input_test)

    print(f'\n{name}\nBest parameters: {kwargs}',
        f'Cross valid accuracy: {acc} vs test accuracy: {accuracy(Target_test, predictions)}',
        'top 5:',*score[:10],sep='\n')

def init(ABS_PATH='evolution/minedData.txt',seed=420):
    # load data
    file = open(ABS_PATH)
    data = []
    for row in file:
        info = row[1:-2].split(', ')
        casted_info = []
        for item in info:
            try: # Int
                casted_info.append(int(item))
            except: # String
                casted_info.append(item if item == 'None' else item[1:-1])
        data.append(casted_info)

    # drop poor data
    data = [d for d in data if d[0] != -1] # drop if missing hand data
    
    # split data
    np.random.seed(seed) # set random seed for reproducibility
    Train_set, Test_set = train_test_split(data, test_size=0.3)

    # Extract target label
    Input_train = [s[:2] + s[3:] for s in Train_set]
    Target_train = [s[2] for s in Train_set]
    Input_test = [s[:2] + s[3:] for s in Test_set]
    Target_test = [s[2] for s in Test_set]

    # preprocess
    #print('Before prepro:', *Train_set[:1], sep='\n')
    Input_train, process, args = preprocess_columns([preprocess_row(row) for row in Input_train])
    Input_test, _, _ = preprocess_columns([preprocess_row(row) for row in Input_test])
    #print('After prepro:', *Train_set[:1], sep='\n')

    return Input_train, Target_train, Input_test, Target_test, process, args
    
def preprocess_row(row:list, process:list=None, args:List[dict]=None) -> list:
    ''' Preprocess row for poker data 

    If targetHandStrength is -1 the row is dropped by returning an empty list.
    Turn classifiers into one hot encoding. 
        Forced_Bet: 0,
        Player_Open: 1,
        Player_Check: 2,
        Player_Fold: 3,
        Player_Call: 4, 
        Player_Raise: 5, 
        Player_All-in: 6,
        None: 7

    ---------------------
    Example: 
    [-1, 50, 0, 50, 50, 'Forced_Bet', 'Player_Fold', 'Forced_Bet', 'Player_Fold', 'Forced_Bet', None]
    -->
    []
    ---------------------
    [6983, 10, 0, 100, 40, 'Player_All-in', None, 'Forced_Bet', None, 'Player_All-in', None]
    -->
    [6983, 10, 0, 100, 40, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, # Target
                                 0, 0, 0, 0, 0, 0, 0, 1, # Target
                                 1, 0, 0, 0, 0, 0, 0, 0, # P1
                                 0, 0, 0, 0, 0, 0, 0, 1, # P1
                                 0, 0, 0, 0, 0, 0, 1, 0, # P2
                                 0, 0, 0, 0, 0, 0, 0, 1, # P2
                                 0, 0, 0, 0, 0, 0, 0, 1, # P3
                                 0, 0, 0, 0, 0, 0, 0, 1, # P3
                                 0, 0, 0, 0, 0, 0, 0, 1, # P4
                                 0, 0, 0, 0, 0, 0, 0, 1] # P4
    '''
    # Discard data if handstrength -1
    targetHandStrength, *_ = row
    if targetHandStrength == -1: return []

    # Padding row 
    player_in_row = (len(row)-1)/(1+actions_per_player)
    index_to_insert_chip = int(player_in_row) + 1
    players_to_add = int(number_of_players-player_in_row)

    padded_row = row[:index_to_insert_chip]  + \
                 [*repeat(0,players_to_add)] + \
                 row[index_to_insert_chip:]  + \
                 [*repeat('None',players_to_add*actions_per_player)]

    # Cast string to int
    action2int = {
        #'Forced_Bet': 0,
        'Player_Open': 1,
        'Player_Check': 2,
        'Player_Fold': 3,
        'Player_Call': 4, 
        'Player_Raise': 5, 
        'Player_All-in': 6,
        'None': 0
    }
    processed_row = []
    for item in padded_row:
        if isinstance(item, int): 
            processed_row.append(item)
        else:
            val = action2int[item]
            length = len(action2int)
            processed_row.extend(one_hot_encode(val, length))

    # If additional processing is requsted
    if process != None and args != None:
        args2 =  []
        for d in args:
            if 'ret' in d: del d['ret']
            args2.append(d)
        args = args2
        processed_row = [func([row], **kwargs)[0][0] for row, func, kwargs in zip(processed_row, process, args)]
    return processed_row

def preprocess_columns(data:List[list]) -> List[list]:
    """ Preprocesses columns for a simple poker dataset. 

    What is applied to each column is decided by the process list
    
    Example:
    [6983, 10, 0, 100, 40, 0, 0, 0, 0, 0, 0, 1, 0,
                           0, 0, 0, 0, 0, 0, 0, 1,
                           ...
                           0, 0, 0, 0, 0, 0, 0, 1]
    -->
    [0.93, 0.12, 0, 0.88, 0.5, 0, 0, 0, 0, 0, 0, 1, 0,
                               0, 0, 0, 0, 0, 0, 0, 1,
                               ...
                               0, 0, 0, 0, 0, 0, 0, 1]

    """
    # Drop Empty rows
    processed = [row for row in data if len(row) != 0]

    # Setup list of processes 
    norm_quantile = lambda x,**kw:normalize(*quantile(x, ret=True, **kw))
    echo = lambda x,**kw:(x,kw)
    process = [ # functions to apply to the corresponding columns
        norm_quantile,  # targetHandStrength
    ]
    
    process.extend([*repeat(norm_quantile, number_of_players)]) # Process for player chips
    process.extend([*repeat(echo, number_of_actions)]) # Process for player actions
    
    # Run processes
    assert len(process) == len(processed[0])
    processed = [func(col) for col, func in zip(zip(*processed),process)]
    args = [kw for _,kw in processed]
    processed = [p for p,_ in processed]
    return list(zip(*processed)), process, args

def normalize(vector:list,ret:bool=False, low:int=None, high:int=None, **kwargs) -> list:
    "Normalizes a vector"
    h = max(vector) if high == None else high
    l = min(vector) if low == None else low
    out = [*repeat(0,len(vector))] if h == l \
    else [(item-l)/(h-l) for item in vector]

    if ret: 
        kwargs.update({'low':l,'high':h})
        return out, kwargs
    return out
    
def one_hot_encode(value:int, length:int):
    zeros = [*repeat(0,length)]
    zeros[value] = 1
    return zeros

def quantile(vector:list, q:list=None, ret:bool=False, **kwargs) -> list:
    "Discretize variable into sqrt(len(vector)) semi-equal-sized buckets"
    if q == None: q = int(len(vector)**.5)
    out, *bins = pd.qcut(vector, q, labels=False,retbins=ret, duplicates='drop')
    if len(bins) > 0: 
        kwargs.update({'q':bins[0]})
        return out, kwargs
    return out

def cross_valid_testing(algorithm, Input_train:List[list], Target_train:list, parameters:dict, k_folds:int=5) -> List[tuple]:
    # build a bunch of dicts from this one dict
    # This is unreadable but it turns {key1:[val1_1,val1_2],key2:[val2_1,val2_2]}
    # into -> [{key1:val1_1,key2:val2_1},{key1:val1_1,key2:val2_2},{key1:val1_2,key2:val2_1},{{key1:val1_2,key2:val2_2}}]
    list_of_dicts = [[{key:val} for val in values] for key, values in parameters.items()]
    list_of_dicts = [{key:val for dic in tup for key,val in dic.items()} for tup in product(*list_of_dicts)]

    # run the stuff
    results = []
    for kwargs in list_of_dicts:
        alg = algorithm(**kwargs)
        score = cross_val_score(alg, Input_train, Target_train, cv=k_folds)
        accuracy = sum(score)/len(score)
        results.append((accuracy, kwargs))
    return results

def accuracy(Target_test:list, predictions:list) -> int:
    "Computes prediction accuracy metric"
    assert len(Target_test) == len(predictions)
    true_positives = len([real for real, prediction in zip(Target_test, predictions) if real==prediction])
    return true_positives/len(Target_test)

def saveModel(PATH):
    ''' Save mined data into path file '''
    try:
        with open(PATH, mode='a') as file:
            print(*data,sep='\n',file=file)

    except:
        raise Exception('Shit no work')

def loadModel(PATH):
    ''' Try to load Path file'''
    try:
        return open(PATH)
    except:
        raise Exception(f'Me no find: {PATH}')

if __name__ == "__main__":
    main()
