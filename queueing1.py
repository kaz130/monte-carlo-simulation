# coding: utf-8

import math
import time
import numpy as np

N = 1000000

def simulation1(arrival_rate, service_rate):
    queue_length = 0
    count = 0
    queue_sum = 0

    for k in range(N):
        queue_length = max(queue_length, 1)
        x = np.random.exponential(1/arrival_rate)
        y = np.random.exponential(1/service_rate)
        if x <= y:
            queue_length += 1
        else:
            queue_length -= 1
            queue_sum += queue_length
            count += 1
    return queue_sum / count

def simulation2(arrival_rate, service_rate):
    queue_length = 0
    count = 0
    queue_sum = 0
    delta = 0.001

    for k in range(N):
        x = np.random.random()
        if x <= service_rate * delta:
            queue_length = max(queue_length - 1, 0)
        elif x > 1 - arrival_rate * delta:
            queue_length += 1
        queue_sum += queue_length

    return queue_sum / N

def simulation3(arrival_rate, service_rate):
    queue_length = 0
    queue_sum = 0
    lb = arrival_rate / (arrival_rate + service_rate)

    for k in range(N):
        u = np.random.random()
        if u <= lb:
            queue_length += 1
        else:
            queue_length = max(queue_length - 1, 0)
        queue_sum += queue_length

    return queue_sum / N

if __name__ == '__main__':
    arrival_rate = 0.5
    service_rate = 1.0
    theory = arrival_rate / (service_rate - arrival_rate)
    print("theory: {0}".format(theory))
    simulations = [simulation1, simulation2, simulation3]
    for simu in simulations:
        start_time = time.time()
        average_queue_length = simu(arrival_rate, service_rate)
        elapsed_time = time.time() - start_time
        print("{0}: {1}  time: {2}".format(simu.__name__, average_queue_length, elapsed_time))

