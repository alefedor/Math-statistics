#!/usr/bin/env python3

import sys
import numpy
import matplotlib.pyplot as plt
from functools import partial

if (len(sys.argv) > 1):
    n = int(sys.argv[1])
else:
    n = 200
    
if (len(sys.argv) > 2):
    iterations = int(sys.argv[2])
else:
    iterations = 100
    
if (len(sys.argv) > 3):
    max_k = int(sys.argv[3])
else:
    max_k = 50
    
if (len(sys.argv) > 4):
    theta = int(sys.argv(4))
else:
    theta = 1.0
    
def uniform_inverse(mean, k):
    return ((k + 1) * mean) ** (1.0 / k)    
    
def exponential_inverse(mean, k):
    return (mean / numpy.math.factorial(k)) ** (1.0 / k)    
    
def mean(values):
    return sum(values) / len(values)    
    
def save_estimation(results, name):
    plt.plot([i for i in range(1, len(results) + 1)], results, label=name)
    plt.xlabel("k")
    plt.ylabel("Mean square of error")
    plt.legend()
    plt.savefig(name + ".png")
    plt.close()  
    
variants = [(partial(numpy.random.uniform, 0.0), "uniform", uniform_inverse), (numpy.random.exponential, "exponential", exponential_inverse)]
    
for distribution, name, inverse in variants:
    results = []
    for k in range(1, max_k + 1):
        diffs = []
        for i in range(iterations):
            observations = [distribution(theta) for j in range(n)]
            values = [x ** k for x in observations]
            m = mean(values)
            inv = inverse(m, k)
            diffs.append((theta - inv) ** 2)
        
        results.append(mean(diffs))
    
    save_estimation(results, name)         

