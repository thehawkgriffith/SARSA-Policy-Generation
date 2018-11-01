from game import standardMap
from game import move
from game import gameOver
from time import sleep
import numpy as np

map1 = standardMap()


def max_dict(d):
        max_key = None
        max_value = float('-inf')
        for k, v in d.items():
               if v > max_value:
                     max_value = v
                     max_key = k
        return max_key, max_value

def random_action(a, eps=0.1):
	ALL_POSSIBLE_ACTIONS = ('U', 'D', 'L', 'R')
	p = np.random.random()
	if p < (1 - eps):
		return a
	else:
		return np.random.choice(ALL_POSSIBLE_ACTIONS)

class Agent():

    def __init__(self):
    	self.policy = {}
    	self.Q = {}

    def generateOptimalPolicy(self, map1):
        alpha = 0.1
        gamma = 0.9
        ALL_POSSIBLE_ACTIONS = ('U', 'D', 'L', 'R')
        states = []
        for state in map1.all_states:
            states.append(state)
        Q = {}
        for s in states:
            Q[s] = {}
            for a in ALL_POSSIBLE_ACTIONS:
                Q[s][a] = 0
        counts = {}
        for s in states:
            counts[s] = {}
            for a in ALL_POSSIBLE_ACTIONS:
                counts[s][a] = 1.0
        t = 1
        for it in range(10000):
            if it % 100 == 0:
                t += 1e-2
            if it % 2000 == 0:
                print("it:", it)
            s = map1.all_states[0]
            map1.setState(s)
            #map1.displayMap()
            #sleep(0.3)   <-----------UNCOMMENT THESE AND THESE IF
            a, _ = max_dict(Q[s])   # YOU WANT TO WATCH IT LEARN
            a = random_action(a)        # 
            epsilon = 0.1               # 
            while not gameOver(map1):   #
                r = move(map1, a)       #
                #map1.displayMap()<-------------------------------
                #sleep(0.3)
                s2 = map1.currentState()
                a2, _ = max_dict(Q[s2])
                a2 = random_action(a2, 0.5/t)
                Q[s][a] = Q[s][a] + alpha/counts[s][a] * (r + (gamma * Q[s2][a2]) - Q[s][a])
                counts[s][a] += 0.005
                s = s2
                a = a2
        self.policy = {}
        self.V = {}
        for s in states:
            if s.terminal == False:
                a, max_q = max_dict(Q[s])
                self.policy[s] = a
                self.V[s] = max_q

agent = Agent()
agent.generateOptimalPolicy(map1)
map1.setState(map1.all_states[0])
map1.displayMap()
while True:
    mv = agent.policy[map1.currentState()]
    move(map1, mv)
    map1.displayMap()
    sleep(0.3)
    if gameOver(map1):
        break
map1.displayMap()
