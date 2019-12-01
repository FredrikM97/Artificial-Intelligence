from game.simulation import Simulation
if __name__ == "__main__":
    algs = ['BFS','DFS','RANDOM', 'GREEDY','A*']
    heuristics = ['MANY', 'BIG']

    print(f'Processing data...')

    for heur in heuristics:
        for type in algs:

            game = Simulation(4,100, 1, False, 20,type ,heur)
            game.run()
            
            print("\n---Statistics----")
            print(f'Type: {type} \
            \nHeuristic: {heur} \
            \nAvg path length: {game.pathLength_avg/game.rounds} \
            \nAvg Expanded:  {game.step_avg/game.rounds} \
            \nWins: {game.winStreak}/{game.rounds}')
            
