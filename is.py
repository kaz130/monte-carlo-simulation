# coding: utf-8

import math
import csv
import numpy as np

N = 1000000

def normal(x, loc = 0.0, scale = 1.0):
    return 1 / math.sqrt(2 * math.pi * scale**2) * math.exp(-(x-loc)**2 / (2 * scale**2))

if __name__ == '__main__':
    pmc = 0
    pic = 0
    c = 8
    m = 8

    for i in range(N):
        x = np.random.normal()
        if (x > c): pmc += 1
    pmc /= N

    for i in range(N):
        x = np.random.normal(loc = m)
        if (x > c): pic += 1 * normal(x) / normal(x, m)
    pic /= N

    theory = 1 - (1.0 + math.erf(c / math.sqrt(2.0))) / 2.0

    print(pic)
    print(theory)

