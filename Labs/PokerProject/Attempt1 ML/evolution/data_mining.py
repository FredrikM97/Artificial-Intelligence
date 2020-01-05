from deuces import Card, Evaluator# https://github.com/FredrikM97/deuces python3

PATH = 'evolution/data/d4.txt'

def main():
    print(miner(PATH))

class miner:
    def __init__(self, PATH):
        f = self.loadFile()
        self.players = {}
        self.id2player = self.git_players(f)
        self.round = 0
        self.runForest(f)
      
        f.close()
    
    def loadFile(self):
        try:
            return open(PATH)
        except:
            raise Exception(f'Me no find: {PATH}')
    
    def runForest(self, f):
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
                'Player_Draw',          # 'Player_Draw RandomA 1'
            }
        }
     
        split_handlers = {
            'hand':self.splitHand,
            'chips':self.splitChips,
            'roundWin':self.splitRoundWin,
            'Action':self.splitAction
        }

        for number, line in enumerate(f):
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
        return Evaluator().evaluate([], [Card.new(x) for x in data[0:5]]) # Lower the better
    
    def getPerspectronum(self):
        pass
    def splitChips(self,data:str):
        _,name,info = data.split(' ')
        return name, info
        
    def splitHand(self,data:str):
        _, name, *info = data.split(' ')
        return name, self.evaluateHand(info)

    def splitRoundWin(self,data:str):
        
        name2int = {'Round_Win_Undisputed':1, 'Round_result':2}
        info, name, _ = data.split(' ')
        
        return name, name2int[info]

    def splitAction(self,data):
        info, name, *_ = data.split(' ')
        return name, info
    
    def newPlayer(self, player:str, key, info):
        '''
        * Create a new player
        '''
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
                name = message[2]
                id2player[player_id] = name
        return id2player
    
    def __str__(self):
        return '\n'.join([f'{key}:{value}' for key,value in self.players.items()])

if __name__ == "__main__":
    main()