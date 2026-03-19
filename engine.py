import math
import numpy as np
from sympy.utilities.iterables import multiset_permutations
import config as conf

# get all subsets of length n from cards
def inclusion(cards, n):
    consider=[]
    for x in range(math.comb(len(cards), n)):
        consider.append([])
    choose = [True]*n + [False]*(len(cards) - n)
    choose = list(multiset_permutations(choose))
    choose.reverse()
    for x in range(len(choose)):
        for y in range(len(choose[x])):
            if choose[x][y]:
                consider[x].append(cards[y])
    return consider

# get all permutations of x +s and (n-x) -s
def sign(n, x):
    signs = [1]*x + [-1]*(n - x)
    signs = list(multiset_permutations(signs))
    return signs

def subset_base_3(n, signs, consider):
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

def subset_base_4(n, consider):
    twin_sets = []
    for y in range(len(consider)):
        attempt = np.array([1] * conf.dim)
        for x in range(n):
            attempt = (attempt * ((2*consider[y][x])+1)) % 8
        if (attempt == 1).all():
            twin_sets.append(list(consider[y]))
    return twin_sets

def find_twin_sets_base_3(cards):
    twin_sets = []
    for n in range(len(cards) + 1):
        consider = np.array(inclusion(cards, n))
        for x in range((-n) % 3, math.floor(n / 2) + 1, 3):
            signs = np.array(sign(n, x))
            twin_sets.extend(subset_base_3(n, signs, consider))
    return twin_sets

def find_twin_sets_base_4(cards):
    twin_sets = []
    for n in range(0, len(cards) + 1, 2):
        consider = np.array(inclusion(cards, n))
        twin_sets.extend(subset_base_4(n, consider))
    return twin_sets

def find_twin_sets(cards):
    if conf.base == 3:
        return find_twin_sets_base_3(cards)
    elif conf.base == 4:
        return find_twin_sets_base_4(cards)
    else:
        return None