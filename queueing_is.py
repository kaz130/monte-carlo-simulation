# coding: utf-8

import math
import time
import csv
import numpy as np
import matplotlib.pyplot as plt

sim_time = 100000

np.random.seed(seed = 0)

def simulation(arrive_rate, service_rate, reset_interval=None):
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

        if reset_interval is not None and t%reset_interval == 0:
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
        probability0 = arrive_rate
        probability_is = arrive_rate2
        for t in range(start_time[k]+1, stop_time[k]+1):
            if path[t] > path[t-1]:
                probability0 *= arrive_rate
                probability_is *= arrive_rate2
            else:
                probability0 *= service_rate
                probability_is *= service_rate2

            l += probability0 / probability_is

    l /= len(stop_time)

    pis = 0
    for k in range(len(stop_time)):
        probability0 = arrive_rate
        probability_is = arrive_rate2
        for t in range(start_time[k]+1, stop_time[k]+1):
            if path[t] > path[t-1]:
                probability0 *= arrive_rate
                probability_is *= arrive_rate2
            else:
                probability0 *= service_rate
                probability_is *= service_rate2
            if path[t-1] > n:
                pis += probability0 / probability_is

    pis /= len(stop_time) * l

    return pis

if __name__ == '__main__':
    recurring_times = 30
    queue_n = 30
    arrive_rate = 0.5
    service_rate = 1.0
    arrive_rate2 = 1.0
    service_rate2 = 0.5

    pth = np.empty(queue_n + 1)
    # 理論値を計算
    rho = arrive_rate / service_rate
    for n in range(0, queue_n + 1):
        p = 1.0
        for m in range(n):
            p -= rho**m * (1-rho)
        pth[n] = p


    pmc = np.empty([recurring_times, queue_n + 1])
    pis = np.empty([recurring_times, queue_n + 1])
    for i in range(recurring_times):
        path_mc = simulation(arrive_rate, service_rate)
        path_is = simulation(arrive_rate2, service_rate2, reset_interval=1000)
        print("{0}:".format(i))
        for n in range(0, queue_n + 1):
            pmc[i][n] = estimation(path_mc, n)
            pis[i][n] = is_estimation(path_is, n, arrive_rate, service_rate,
                                      arrive_rate2, service_rate2)
            print("{0:<2}, {1:<.10f}, {2:<.10f}, {3:<.10f}"
                    .format(n, pth[n], pmc[i][n], pis[i][n]))

    pmc_ave = np.average(pmc, axis=0)
    pis_ave = np.average(pis, axis=0)
    pmc_var = np.var(pmc, axis=0)
    pis_var = np.var(pis, axis=0)
    pmc_std = np.std(pmc, axis=0)
    pis_std = np.std(pis, axis=0)

    with open('result1.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for i in range(recurring_times):
            for n in range(queue_n + 1):
                writer.writerow([n, pth[n], pmc[i][n], pis[i][n]])

    with open('result2.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for n in range(queue_n + 1):
            writer.writerow([n, pth[n],
                pmc_ave[n], pis_ave[n],
                pmc_var[n], pis_var[n],
                pmc_std[n], pis_std[n]])

    with open('result.txt', 'w', newline='') as f:
        f.write("{0:>2}, {1:>12}, {2:>12}, {3:>12}, {4:>12}\n"
                .format("n", "pmc_ave", "pis_ave", "pmc_var", "pis_var"))
        for n in range(queue_n + 1):
            f.write("{0:<2}, {1:12.4e}, {2:12.4e}, {3:12.4e}, {4:12.4e}\n"
                    .format(n, pmc_ave[n], pis_ave[n], pmc_var[n], pis_var[n]))

