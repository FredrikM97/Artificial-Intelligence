# greedy_man_cost_function
def cost_function(self,node, current):
    goal = self.goal
    pos = node

    return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1]) +1