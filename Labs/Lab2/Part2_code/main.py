from game.simulation import Simulation
if __name__ == "__main__":
    algs = ['BFS','DFS','RANDOM', 'GREEDY_MANY', 'GREEDY_POT','A*_MANY', 'A*_POT']
    
    print(f'Processing data...')

    for type in algs:

        game = Simulation(4,100, 100, False, 20,type)
        game.run()
        
        print(f'\n---Statistics---- \
        \nType: {type} \
        \nAvg path length: {game.pathLength_avg/game.rounds} \
        \nAvg Expanded:  {game.step_avg/game.rounds} \
        \nWins: {game.winStreak}/{game.rounds}')