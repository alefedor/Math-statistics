#!/usr/bin/env python2

import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import chi2
 

if (len(sys.argv) > 1):
    number_of_points = int(sys.argv[1])
else:
    number_of_points = 300000
    
if (len(sys.argv) > 2):
    a = float(sys.argv[2])
else:
    a = 1.0

c = 1.0 / (2 * np.exp(-a) + 2 * a)

if (len(sys.argv) > 3):
    delta = float(sys.argv[3])
else:
    delta = 0.2

def save_values(values, name):
    mp = dict()
    for x in values:
        if x >= 0:
            num = int(x / delta)
        else:
            num = int(x / delta - 1)
        
        if (abs(num) > 4.0 / delta):
            continue
        
        if num in mp:
            mp[num] = mp[num] + 1
        else:
            mp[num] = 1    
            
    items = sorted(mp.items())
            
    plt.plot([delta * items[i][0] for i in range(len(items))], [items[i][1] for i in range(len(items))], label=name)
    plt.xlabel("x")
    plt.ylabel("Number of points in range [x, x + delta)")
    plt.legend()
    plt.savefig(name + ".png")
    plt.close()  
    
def uniform_distribution(): # on the third day God created uniform distribution
    return np.random.uniform()
    
def inverse_distribution_function(alpha):
    if alpha < c * np.exp(-a):
        assert(math.log(alpha / c) < -a)    
        return math.log(alpha / c)
    
    if alpha < c * (np.exp(-a) + 2 * a):
        assert(-a <= -a + (alpha - c * np.exp(-a)) / c and -a + (alpha - c * np.exp(-a)) / c < a)
        return -a + (alpha - c * np.exp(-a)) / c
    
    assert(-math.log(np.exp(-a) - (alpha - c * (np.exp(-a) + 2 * a)) / c) > a)
    return -math.log(np.exp(-a) - (alpha - c * (np.exp(-a) + 2 * a)) / c)    

def model_using_inverse_function_method():
    return inverse_distribution_function(uniform_distribution())

def exponential():
    return -math.log(uniform_distribution())
    
def model_using_decomposition_method():
    random = uniform_distribution()
    
    if random < c * np.exp(-a):
        return -a - c * exponential()
        
    if random < c * (2 * a + np.exp(-a)):
        return uniform_distribution() * 2 * a - a
        
    return a + c * exponential()                    
       
variants = [(model_using_inverse_function_method, "inverse function method"), (model_using_decomposition_method, "decomposition method")]

for model, name in variants:
    values = []
    for i in range(number_of_points):
        values.append(model())
    save_values(values, name)    
