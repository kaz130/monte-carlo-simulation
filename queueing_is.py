# coding: utf-8

import math
import time
import csv
import numpy as np
import matplotlib.pyplot as plt

sim_time = 100000

np.random.seed(seed = 0)

def simulation(arrive_rate, service_rate, reset=False):
    reset_interval = 1000
    queue_length = 0
    lb = arrive_rate / (arrive_rate + service_rate)
    path = np.empty(sim_time)
    path[0] = 0

    for t in range(1, sim_time):
        u = np.random.random()
        if u <= lb:
            queue_length += 1
        else:
            queue_length = max(queue_length - 1, 0)

        if reset and t%reset_interval == 0:
            queue_length = 0

        path[t] = queue_length

    return path

def calc_cycle(path):
    start_time = []
    stop_time = []

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

    start_time.pop()
    stop_time.pop()
    return start_time, stop_time

def estimation(path, n):
    start_time, stop_time = calc_cycle(path)
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

def is_estimation(path, n, arrive_rate, service_rate,
                  arrive_rate2, service_rate2):
    start_time, stop_time = calc_cycle(path)
    l = 0
    for k in range(len(stop_time)):
        for t in range(start_time[k], stop_time[k]):
            l += (path_probability(path[start_time[k]:t+2], arrive_rate, service_rate)
                    / path_probability(path[start_time[k]:t+2], arrive_rate2, service_rate2))

    l /= len(stop_time)

    pis = 0
    for k in range(len(stop_time)):
        for t in range(start_time[k], stop_time[k]):
            if path[t] > n:
                pis += (path_probability(path[start_time[k]:t+2], arrive_rate, service_rate)
                        / path_probability(path[start_time[k]:t+2], arrive_rate2, service_rate2))
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
    queue_n = 30
    arrive_rate = 0.5
    service_rate = 1.0
    arrive_rate2 = 1.0
    service_rate2 = 0.5

    pth = []
    pmc = []
    pis = []

    path_mc = simulation(arrive_rate, service_rate)
    path_is = simulation(arrive_rate2, service_rate2, reset=True)
    for n in range(0, queue_n + 1):
        p = 1
        rho = arrive_rate / service_rate
        for m in range(n):
            p -= rho**m * (1-rho)
        pth.append(p)

        pmc.append(estimation(path_mc, n))
        pis.append(is_estimation(path_is, n, arrive_rate, service_rate, arrive_rate2, service_rate2))

        print([n, pth[n], pmc[n], pis[n]])


    # with open('result.csv', 'w', newline='') as f:
    #     writer = csv.writer(f, delimiter=',')
    #     for n in range(len(pth)):
    #         writer.writerow([n, pth[n], pmc[n], pis[n]])

