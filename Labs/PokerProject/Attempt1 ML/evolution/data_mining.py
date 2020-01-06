from deuces import Card, Evaluator# https://github.com/FredrikM97/deuces python3
from itertools import tee, repeat, chain, zip_longest
from functools import reduce
import glob
from copy import deepcopy
PATH = 'evolution/data/'

def main():
    for i in glob.glob(f'{PATH}*.txt'):
        print(f'Opening folder: {i}')
        m = miner(f'{i}')
        for player in m.get_players():
            data = deepcopy(m).getPerspectronum(player)
            m.saveFile('evolution/','minedData.txt',data)
class miner:
    def __init__(self, PATH):
        f = self.loadFile(PATH)
        self.players = {}
        self.id2player = self.git_players(f)
        self.round = 0
        self.runForest(f)
      
        f.close()
    
    def loadFile(self, PATH):
        ''' Try to load Path file'''
        try:
            return open(PATH)
        except:
            raise Exception(f'Me no find: {PATH}')

    def saveFile(self, PATH:str, name:str, data:list):
        ''' Save mined data into path file '''
        try:
            with open(PATH+"/"+name, mode='a') as file:
                print(*data,sep='\n',file=file)

        except:
            raise Exception('Shit no work')

    def runForest(self, f):
        ''' Extract data from data in file '''
        mydicisbig = {
            'hand':{ # String, List
                'Player_Hand'           # 'Player_Hand Subject_1 4s 6c 8s Kd 5c'
            },
            'chips':{ # String, Int
                'Chips'                 # 'Chips Subject_1 10'
            },
            'roundWin':{ # Int
                'Round_Win_Undisputed', # 'Round_Win_Undisputed Subject_2 100'
                'Round_result'          # 'Round_result Subject_2 90'
            },
            'Action':{ # String, String
                'Forced_Bet',           # 'Forced_Bet Subject_2 40'
                'Player_Open',          # 'Player_Open ReflexB 11' 
                'Player_Check',         # 'Player_Check RandomA '
                'Player_Raise',         # 'Player_Raise RandomA 17'
                'Player_Call',          # 'Player_Call RandomA '
                'Player_Fold',          # 'Player_Fold Subject_1 '
                'Player_All-in',        # 'Player_All-in Subject_1 10'
                #'Player_Draw',          # 'Player_Draw RandomA 1'
            }
        }
     
        split_handlers = {
            'hand':self.splitHand,
            'chips':self.splitChips,
            'roundWin':self.splitRoundWin,
            'Action':self.splitAction
        }

        for line in f:
            #print(number,line)
            if 'all players' in line: # Check sent message :D
                if "Sent message 'Round " in line: self.round = line.split(' ')[3]
 
                for key,value in mydicisbig.items():
                    for keyword in value:
                        if keyword in line:
                            name, info = split_handlers[key](line.split("'")[1]) # call the handle function
                            
                            self.newPlayer(name, key, info) # add to dict
                            break


    def evaluateHand(self,data:list):
        ''' Return integer value of hand strength: Lower is better '''
        return Evaluator().evaluate([], [Card.new(x) for x in data[0:5]]) # Lower the better
    
    def get_players(self):
        return [*self.id2player.values()]
    
    def getPerspectronum(self, target_player:str):
        """ Compile data into one line
            Works with multiple users, example below there is 1 target and 2 opponents, total of 3 players
            Example:
            Data:
                [-1, 50, 0, 50, 50, 'Forced_Bet', 'Player_Fold', 'Forced_Bet', 'Player_Fold', 'Forced_Bet', None]
            Parameters:
                targetHandStrength, targetChips, targetWin, p1Chips,p2Chips, targetAction1,targetAction2, p1Action1,p1Action2, p2Action1, p2Action2,  

             
        """
        turn_player_data = {}
        for (turn, agent), data in self.players.items(): # Combine turn into one list
            if turn not in turn_player_data: 
                turn_player_data.update({turn:{agent:data}})
            else:
                turn_player_data[turn].update({agent:data})
        
        result = []
        for _, player_data in turn_player_data.items(): # Extract relevant data from players
            actions = {}
            the_rest = {}
            for player in self.id2player.values():
                actions.update({player:player_data[player]['Action']}) # Extract actions from player
                del player_data[player]['Action']
                if player is target_player:
                    the_rest.update({player:player_data[player]})
                else: # Extract blacklist data
                    del player_data[player]['hand']
                    del player_data[player]['roundWin']
                    the_rest.update({player:player_data[player]})
            # fix actions
            actions = {player:self.action_tuple(2, actions) for player, actions in actions.items()}
            # stitch fixed actions with the rest
            players = [player for player in self.id2player.values() if player is not target_player]
            orderd_players = [target_player]+players
            orderd_actions = [actions[player] for player in orderd_players]
            orderd_actions = [*zip(*orderd_actions)] # from turn,tuple -> tuple,turn
            orderd_data = [[*the_rest[player].values()] for player in orderd_players]
            orderd_data = [*self.flatten(orderd_data)]
            result.extend([orderd_data+[*self.flatten(actions)] for actions in orderd_actions])
            #print(*result,sep='\n')
        return result
        
        
        
    def flatten(self,list_of_lists):
        "Flatten one level of nesting"
        return chain.from_iterable(list_of_lists)

    def pairwise(self,iterable, n=2):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        A = tee(iterable,n)
        for i, a in enumerate(A):
            for _ in repeat(None,i): next(a, None)
        return zip_longest(*A, fillvalue=None)

    def action_tuple(self, n:int, action:list) -> list:
        """ Combine actions into n sized tuples """
        return list(self.pairwise(action, n=n))
    
    def splitChips(self,data:str):
        ''' Split name and chips '''
        _,name,info = data.split(' ')
        return name, int(info)
        
    def splitHand(self,data:str):
        ''' Split name and hand info '''
        _, name, *info = data.split(' ')
        return name, self.evaluateHand(info)

    def splitRoundWin(self,data:str):
        ''' Split name and win as int -> 0:Loss,1:Undisputed,2:Win '''
        name2int = {'Round_Win_Undisputed':1, 'Round_result':2}
        info, name, _ = data.split(' ')
        return name, name2int[info]

    def splitAction(self,data:str):
        ''' Split name and action '''
        info, name, *_ = data.split(' ')
        return name, info
    
    def newPlayer(self, player:str, key, info):
        '''Create a new player '''

        if (self.round, player) not in self.players:
            self.players[(self.round, player)] = {
                'hand':-1,
                'chips':-1,
                'roundWin':0,
                'Action':[]
            }
        #if key == 'roundWin': print(self.players[(self.round, player)][key])
        if key == 'Action':
            self.players[(self.round, player)][key].append(info)
        else:
            self.players[(self.round, player)][key] = info

    def git_players(self, file) -> dict:
        id2player = {}
        for line in file :
            if 'All players connected' in line: break
            if 'Connected player' in line: 
                # Looks like this: Received message 'Name Subject_3' from player #2
                message = line.split(' ')
                player_id = ' '.join(message[-2:])
                name = message[2][1:-1]
                id2player[player_id] = name
        return id2player
    
    def __str__(self):
        return '\n'.join([f'{key}:{value}' for key,value in self.players.items()])

if __name__ == "__main__":
    main()