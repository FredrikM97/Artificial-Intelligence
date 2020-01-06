import numpy as np
from sklearn.model_selection import train_test_split,cross_val_score

from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import warnings
import copy
from itertools import repeat,

'''
TODO:
    ACTION: 
        Fold: 0, 
        Call: 1, 
        Raise: 2, 
        Allin: 3
        Open: 4
        Check: 5
        Unknown: -1

[-1, 50, 0, 50, 50, 'Forced_Bet', 'Player_Fold', 'Forced_Bet', 'Player_Fold', 'Forced_Bet', None]

[-1, 40, 0, 40, 70, 'Forced_Bet', 'Player_Fold', 'Forced_Bet', 'Player_Fold', 'Forced_Bet', 'Player_Check']
'''

def main():
    
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
    print(*data[:5],sep='\n')
    
    # split data
    np.random.seed(420) # set random seed for reproducibility
    Train_set, Test_set = train_test_split(data, test_size=0.2)

    # preprocess
    print('Before prepro:', *Train_set[:1], sep='\n')
    Train_set = preprocess_columns([preprocess_row(row) for row in Train_set])
    Test_set = preprocess_columns([preprocess_row(row) for row in Test_set])
    print('After prepro:', *Train_set[:1], sep='\n')  

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
    [6983, 10, 0, 100, 40, 0, 0, 0, 0, 0, 0, 1, 0,
                           0, 0, 0, 0, 0, 0, 0, 1,
                           1, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 1,
                           0, 0, 0, 0, 0, 0, 1, 0,
                           0, 0, 0, 0, 0, 0, 0, 1]
    '''
    targetHandStrength, *_ = row
    if targetHandStrength == -1: return []

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
    for item in row:
        if isinstance(item, int): 
            preprocess_row.append(item)
        else:
            val = action2int[item]
            length = len(action2int)
            preprocess_row.extend(one_hot_encode(val, length))

    return processed_row

def preprocess_columns(data:List[list]) -> List[list]:
    """ Preprocesses columns for a simple poker dataset. What is applied
to each column is decided by the process list"""
    norm_quantile = lambda x:normalize(quantile(x))
    echo = lambda x:x
    process = [ # functions to apply to the corresponding columns
        norm_quantile,
        normalize,
        norm_quantile,
        normalize,
        normalize,
        normalize,
        normalize,
        normalize,
        normalize,
        normalize,
        normalize,
        echo]
    assert len(process) == len(data[0])
    norm = [func(col) for col, func in zip(zip(*data),process)]
    return list(zip(*norm))

def normalize(vector: list) -> list:
    """ Normalizes a vector """
    high = max(vector)
    low = min(vector)
    if high-low == 0: return [zerp for zerp in repeat(0,len(vector))]
    return [(item-low)/(high-low) for item in vector]

def one_hot_encode(value:int, length:int):
    zeros = [0 for _ in repeat(None,length)]
    zeros[value] = 1
    return zeros

def saveModel(PATH):
    ''' Save mined data into path file '''
    try:
        with open(PATH+"/"+name, mode='a') as file:
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
