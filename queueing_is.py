# coding: utf-8

import math
import time
import numpy as np
import matplotlib.pyplot as plt

N = 1000000
# N = 10

np.random.seed(seed = 0)

def simulation(arrive_rate, service_rate):
    queue_length = 0
    lb = arrive_rate / (arrive_rate + service_rate)
    path = np.empty(N)
    path[0] = 0

    for t in range(1, N):
        u = np.random.random()
        if u <= lb:
            queue_length += 1
        else:
            queue_length = max(queue_length - 1, 0)
        path[t] = queue_length

    return path

def estimation(path, n):
    start_time = []
    stop_time = []
    number_of_cycles = 0

    t = 0
    while t < len(path):
        # サイクルが始まるまでループ
        while t < len(path) and path[t] == 0:
            t += 1
        start_time.append(t)

        # サイクルが終わるまでループ
        while t < len(path) and path[t] > 0:
            t += 1
        stop_time.append(t)

    l = 0
    for k in range(len(stop_time)):
        l += stop_time[k] - start_time[k]
    l /= len(stop_time)

    pmc = 0
    for k in range(len(stop_time)):
        for t in range(start_time[k], stop_time[k]):
            if path[t] > n:
                pmc += 1
    pmc /= len(stop_time) * l

    return pmc

def is_estimation(path, n, arrive_rate, service_rate, arrive_rate2, service_rate2):
    start_time = []
    stop_time = []
    number_of_cycles = 0

    t = 0
    while t < len(path):
        # サイクルが始まるまでループ
        while t < len(path) and path[t] == 0:
            t += 1
        start_time.append(t)

        # サイクルが終わるまでループ
        while t < len(path) and path[t] > 0:
            t += 1
        stop_time.append(t)

    l = 0
    for k in range(len(stop_time)):
        for t in range(start_time[k], stop_time[k]):
            l += path_probability(path[start_time[k]:t+2], arrive_rate, service_rate) \
                    / path_probability(path[start_time[k]:t+2], arrive_rate2, service_rate2)

    l /= len(stop_time)

    pis = 0
    for k in range(len(stop_time)):
        for t in range(start_time[k], stop_time[k]):
            if path[t] > n:
                pis += 1 * path_probability(path[start_time[k]:t+2], arrive_rate, service_rate) \
                / path_probability(path[start_time[k]:t+2], arrive_rate2, service_rate2)
    pis /= len(stop_time) * l

    return pis

def path_probability(path, arrive_rate, service_rate):
    # 系内数が増加m+1
    # p = arrive_rate / (arrive_rate + service_rate)
    p = arrive_rate
    for t in range(1, len(path)):
        # 系内数が増加
        if (path[t] - path[t-1] == 1):
            # p *= arrive_rate / (arrive_rate + service_rate)
            p *= arrive_rate
        # 系内数が減少
        else:
            # p *= service_rate / (arrive_rate + service_rate)
            p *= service_rate
    return p

if __name__ == '__main__':
    arrive_rate = 0.1
    service_rate = 0.9
    arrive_rate2 = 0.4
    service_rate2 = 0.6
    n = 5
    path = simulation(arrive_rate, service_rate)
    print(estimation(path, n))
    path = simulation(arrive_rate2, service_rate2)
    print(is_estimation(path, n, arrive_rate, service_rate, arrive_rate2, service_rate2))
    plt.plot(path, linewidth=1)
    plt.show()

    # theory_pn = []
    theory_p = 1
    rho = arrive_rate / service_rate
    for n in range(n):
        # theory_pn.append(rho**n * (1-rho))
        theory_p -= rho**n * (1-rho)

    print(theory_p)

