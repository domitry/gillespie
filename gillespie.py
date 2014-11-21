import random, math
from copy import deepcopy as copy
from matplotlib.pyplot import *

"""
Simple Implementation of Gillespie Algorithm

exapmle:
from gillespie import *
A = Species('A')
B = Species('B')
sim = Simulator.new(A, B)
sim.reaction(lambda a, b: alpha1/(1+b**beta), lambda sim: sim.decrement(A, 1))
sim.reaction(lambda a, b: a, lambda sim: sim.increment(A, 1))
sim.reaction(lambda a, b: alpha2/(1+a**gamma), lambda sim: sim.decrement(B, 1))
sim.reaction(lambda a, b: b, lambda sim: sim.increment(B, 1))
sim.increment(A, 100)
sim.increment(B, 50)
sim.run(100)
sim.plot()
"""

class Species:
    def __init__(self, name):
        self.name = name

class Reaction:
    def __init__(self, *args):
        args = list(args)
        self.propersity_func = args.pop()
        self.action_func = args.pop()
        self.species = args

    def propersity(self, *args):
        return self.propersity_func(*args)

    def action(self, *args):
        return self.action_func(*args)

class Simulator:
    def __init__(self, *species):
        self.t = 0.0
        self.num = {s.name: 0 for s in species}
        self.reactions = []
        self.species = list(species)
        self.hist = []

    def run(self, step_num):
        if self.t == 0.0:
            self.hist.append({'t': 0, 'num': copy(self.num)})

        for step in range(0, step_num):
            arr = map(lambda r: r.propersity(*[self.num[s.name] for s in self.species]), self.reactions)
            v_total = sum(arr)
            rnd1 = random.random()
            rnd1 = random.random() if rnd1 == 0.0 else rnd1
            dt = (1.0/v_total)*math.log(1.0/rnd1)
            rnd2 = random.random()*v_total
            rnd2 = random.random() if rnd2 == 0.0 else rnd2
            tmp = 0
            for i, p in enumerate(arr):
                tmp += p
                if tmp > rnd2:
                    self.reactions[i].action(self)
                    break
            self.t += dt
            self.hist.append({'t': self.t , 'num': copy(self.num)})

    def reaction(self, propersity, action):
        arr = self.species + [action, propersity]
        rec = Reaction(*arr)
        self.reactions.append(rec)

    def decrement(self, species, num):
        self.num[species.name] -= num

    def increment(self, species, num):
        self.num[species.name] += num

    def plot(self):
        data = []
        for h in self.hist:
            row = []
            for species in self.species:
                row.append(h['num'][species.name])
            data.append(row)

        plot(data,xdata=map(lambda h: h['t'], self.hist))
        xlabel("Time(s)")
        ylabel("Number of Moleculars")
        legend(map(lambda s: s.name, self.species))
        ylim(0)
        show()
