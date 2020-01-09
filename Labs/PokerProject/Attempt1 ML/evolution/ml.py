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
from itertools import repeat
from typing import List

from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

# Setup 
actions_per_player  = 2
encoding_size       = 8
number_of_players   = 5
number_of_actions   = actions_per_player * encoding_size * number_of_players

def main():
    Input_train, Target_train, Input_test, Target_test = init()
    
    # prepare some classifiers from scikit library
    classifiers = [
        KNeighborsClassifier(5),
        SVC(gamma=2, C=1),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        MLPClassifier(alpha=1, max_iter=1000),
    ]
    
    # run all classifiers
    for classifi in classifiers:
        predictions = classifi.fit(Input_train, Target_train).predict(Input_test)
        name = classifi.__doc__.split('.')[0]
        print(f'Accuracy: {accuracy(Target_test, predictions)}\tClassifier: {name}')

def init(seed=420):
    # load data
    ABS_PATH = 'evolution/minedData.txt'
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
    
    # split data
    np.random.seed(seed) # set random seed for reproducibility
    Train_set, Test_set = train_test_split(data, test_size=0.2)

    # preprocess
    print('Before prepro:', *Train_set[:1], sep='\n')
    Train_set = preprocess_columns([preprocess_row(row) for row in Train_set])
    Test_set = preprocess_columns([preprocess_row(row) for row in Test_set])
    print('After prepro:', *Train_set[:1], sep='\n')

    Input_train = Train_set[:2] + Train_set[3:]
    Target_train = Train_set[2]
    Input_test = Test_set[:2] + Test_set[3:]
    Target_test = Test_set[2]
    return Input_train, Target_train, Input_test, Target_test

def predict(model, data):
    model.predict(data)
    
def preprocess_row(row:list) -> list:
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
    player_in_row = (len(row)-2)/(1+actions_per_player)
    index_to_insert_chip = int(player_in_row) + 2
    players_to_add = int(number_of_players-player_in_row)

    padded_row = row[:index_to_insert_chip]  + \
                 [*repeat(0,players_to_add)] + \
                 row[index_to_insert_chip:]  + \
                 [*repeat('None',players_to_add*actions_per_player)]

    # Cast string to int
    action2int = {
        'Forced_Bet': 0,
        'Player_Open': 1,
        'Player_Check': 2,
        'Player_Fold': 3,
        'Player_Call': 4, 
        'Player_Raise': 5, 
        'Player_All-in': 6,
        'None': 7
    }

    processed_row = []
    for item in padded_row:
        if isinstance(item, int): 
            processed_row.append(item)
        else:
            val = action2int[item]
            length = len(action2int)
            processed_row.extend(one_hot_encode(val, length))

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
    norm_quantile = lambda x:normalize(quantile(x))
    echo = lambda x:x
    process = [ # functions to apply to the corresponding columns
        norm_quantile,  # targetHandStrength
        norm_quantile,  # targetChips
        echo,           # targetWin
    ]

    process.extend([*repeat(norm_quantile, number_of_players-1)]) # Process for player chips
    process.extend([*repeat(echo, number_of_actions)]) # Process for player actions
    
    # Run processes
    assert len(process) == len(processed[0])
    processed = [func(col) for col, func in zip(zip(*processed),process)]
    return list(zip(*processed))

def normalize(vector: list) -> list:
    "Normalizes a vector"
    high = max(vector)
    low = min(vector)
    if high-low == 0: return [*repeat(0,len(vector))]
    return [(item-low)/(high-low) for item in vector]

def one_hot_encode(value:int, length:int):
    zeros = [*repeat(0,length)]
    zeros[value] = 1
    return zeros

def quantile(vector: list) -> list:
    "Discretize variable into sqrt(len(vector)) semi-equal-sized buckets"
    return pd.qcut(vector, int(len(vector)**.5), labels=False, duplicates='drop')

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
