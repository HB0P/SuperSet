import math
import numpy as np
from sympy.utilities.iterables import multiset_permutations
import config as conf

def inclusion(cards, n):
    consider=[]
    for x in range(math.comb(conf.dim + 2, n)):
        consider.append([])
    choose = [True]*n + [False]*(conf.dim + 2 - n)
    choose = list(multiset_permutations(choose))
    choose.reverse()
    for x in range(len(choose)):
        for y in range(len(choose[x])):
            if choose[x][y]:
                consider[x].append(cards[y])
    return consider

def sign(n, x):
    signs = [1]*x + [-1]*(n - x)
    signs = list(multiset_permutations(signs))
    return signs

def subset(n, signs, consider):
    twin_sets = []
    for y in range(len(consider)):
        for s in range(len(signs)):
            attempt = np.array([0] * conf.dim)
            for x in range(n):
                    attempt = (attempt + (signs[s][x] * consider[y][x])) % 3
            if (attempt == 0).all():
                twin_sets.append(list(consider[y]))
                break
    return twin_sets

def find_twin_sets(cards):
    twin_sets = []
    for n in range(1, conf.dim + 3):
        consider = np.array(inclusion(cards, n))
        for x in range((-n) % 3, math.floor(n / 2) + 1, 3):
            signs = np.array(sign(n, x))
            twin_sets.extend(subset(n, signs, consider))
    return twin_sets

ts = find_twin_sets([
    np.array([1, 0, 2, 2]),
    np.array([2, 1, 2, 1]),
    np.array([2, 0, 1, 1]),
    np.array([1, 1, 2, 1]),
    np.array([2, 0, 1, 2]),
    np.array([2, 0, 2, 1])
])

for t in ts:
    print(t)
print(len(ts))
