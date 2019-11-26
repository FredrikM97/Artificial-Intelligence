import math
# AStar_euc_cost_function
def cost_function(self,node, current):
    goal = self.goal
    pos = node

    return math.sqrt((pos[0]-goal[0])*(pos[0]-goal[0]) + (pos[1]-goal[1])*(pos[1]-goal[1])) + self.getNode(current)['cost'] +1