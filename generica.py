import math
from random import getrandbits, randint, seed, choice
from os import urandom
try:
    import matplotlib.pyplot as plt
except Exception:
    pass
from itertools import tee
import copy
#from multiprocessing import Process
from bitarray import bitarray

class Genenetix(object):
    def __init__(popsize=10,size=3, func='rastrigin'):
        seed(urandom(1000))
        self.population = [Solution(fill=True, size=size, func=func) for _ in range(popsize)]

    def run(self):
        pass

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Solution(object):
    def __init__(self, fill=False, size = 3, func = None):
#       if func in 'six-hump':
#           size = 2
        self._bits = []
        self._values = list()
        self._change = True
        self._func = func
        self._b2f = self._func.bit2float
        self._size = size
        self._repr = 10 #number of bits
        if fill:
            self.generate()


    def eval(self):
        if(self._change):
            self._values = []
            for bits in self._bits:
                self._values.append(self._b2f(bits))
        self.change = False
        return self._func.eval(self._values)

    def fitness(self):
        return 1/self.eval()

    def mutate(self):
        self.change = True
        for bits in self._bits:
            if self.chance():
                ypos = randint(0, len(bits)- 1)
                bits[ypos] = not bits[ypos]


    def chance(self):
        r = bool(getrandbits(1))
        return r

    def crosover(self, solution):
        #TODO: crosover the 2 genes
        self.change = True
        new = list()
        for mother, father in zip(self._bits, solution._bits):
            if self.chance():
                bits = bitarray()
                for index in range(len(mother)):
                    b = choice((mother[index], father[index]))
                    bits.append(b)
            else:
                bits = copy.deepcopy(choice((mother, father)))
            new.append(bits)
        a = Solution()
        a._bits = new
        return a

    def generate(self):
        for _ in range(self._size):
            arraybit = bitarray()
            for _ in range(self._repr):
                arraybit.append(bool(getrandbits(1)))
            self._bits.append(arraybit)

    def printg(self):
        for line in self._bits:
            print (line.to01())
        print('\n')

class Function:
    def __init__(self, func='rastrigin'):
        funcs = {"rastrigin":
                 {
                    'func': self.rastrigin,
                    'slim': 5.12,
                    "ulim": -5.12,
                    "special": False
                 },
                 "griewangk":
                 {
                    "func": self.griewangk,
                    "slim": 600,
                    "ulim": -600,
                    "special": False
                 },
                 "rosenbrock":
                 {
                    "func": self.rosenbrock,
                    "slim": 2.048,
                    "ulim": -2.048,
                    "special": False
                 },
                 "six-hump":
                 {
                    "func": self.six_hump,
                    "slim": None,
                    "ulim": None,
                    "special": True

                 }
                }
        self.special = [3, 2]
        self.isspecial = funcs[func]["special"]
        self.pos = 0
        self.run = False

        self.slim = funcs[func]["slim"]
        self.ulim = funcs[func]["ulim"]
        self.func = funcs[func]['func']


    def rastrigin(self, numbers):
        ret = float(10 * len(numbers))
        for val in numbers:
            ret += (val ** 2) - 10 * math.cos(2 * math.pi * val)
        return ret

    def griewangk(self, numbers):
        ret = sum([x ** 2 / 4000 for x in numbers])
        n = [math.cos(x / math.sqrt(i)) for i, x in enumerate(numbers, 1)]
        prod = 1
        for nu in n:
            prod *= nu
        ret -= prod + 1
        return ret

    def rosenbrock(self, numbers):

        def algo(x, y):
            return 100 * (y - x ** 2) ** 2 + (1 - x) ** 2

        return sum([algo(x, y) for x, y in pairwise(numbers)])

    def six_hump(self, numbers):
        x1, x2 = numbers
        return (4 - 2.1 * x1**2 + x1**4 / 3) * x1**2 + x1 * x2 + \
                (-4 + 4 * x2**2) * x2**2

    def eval(self, numbers):
        return self.func(numbers)

    def bit2float(self, boolarray):
        number = 0
        offset = 1
        for val in boolarray:
            number += offset * int(val)
            offset *= 2
        max = 2 ** len(boolarray) - 1
        """This is needed because some functions are special and
        they don't play nice with others"""
        if self.isspecial:
            self.slim = self.special[self.pos]
            self.ulim = -self.special[self.pos]
            if not self.run:
                self.pos += 1
                self.pos %= 2
        number = (float(number) / max) * (self.slim - self.ulim) + self.ulim
        return number


class Population:
    def __init__(self, popsize=30, vec_size=3, func = None):
        self._popsize = popsize
        self._vec_size = vec_size
        self._func = func
        self._population = [Solution(fill=True, size=vec_size, func=func)
                            for _ in range(popsize)]
        self.elit = []

    def printp(self):
        for index, creature in enumerate(self._population):
            print("Creature %d:" % index)
            creature.printg()

    def printf(self):
        for index, creature in enumerate(self._population):
            print("Creature %d with fitness %f value %f:" % (index, creature.fitness(), creature.eval()))

    def select(self):
        self._population.sort(key=Solution.fitness)
        self.printf()


    def combine(self):
        pass

    def evolve(self):
        pass


if __name__ == '__main__':
    func = Function()
    pop = Population(func=func)
    pop.select()

'''

if __name__ == "__main__":
    a = Solution()
    b = Solution()
    a.generate()
    a.printf()
    b.generate()
    b.printf()
    a.mutate()
    a.printf()
    b.mutate()
    b.printf()
    c = a.crosover(b)
    c.printf()
    print(c.eval())
'''
