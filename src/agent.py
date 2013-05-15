
class Agent:

    def __init__(self, pos, speed, goal = None):
        self.pos = pos
        self.speed = speed
        self.goal = goal
        
    def __repr__(self):
        return '%s, %s, %s' % (self.pos, self.speed, self.goal)
        
    def __str__(self):
        return self.__repr__()
        
class Player(Agent):

    def __init__(self, pos, speed, goal = None):
        Agent.__init__(self, pos, speed, goal)
        
        
