#!/usr/bin/env python2

import sys
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import chi2
 

if (len(sys.argv) > 1):
    max_n = int(sys.argv[1])
else:
    max_n = 50
    
if (len(sys.argv) > 2):
    iterations = int(sys.argv[2])
else:
    iterations = 300

if (len(sys.argv) > 3):
    trust = float(sys.argv[3])
else:
    trust = 0.95
   
chi2_ppf1 = 0
chi2_ppf2 = 0
    
norm_ppf1 = norm.ppf((3 - trust) / 4.0)
norm_ppf2 = norm.ppf((3 + trust) / 4.0)
    
    
def mean(values):
    return sum(values) / len(values)      
    
def segment_length_a(xs):
    s = sum([x * x for x in xs])
    return s * (1 / chi2_ppf1 - 1 / chi2_ppf2)
    
def segment_length_b(xs):
    ns = len(xs) * (mean(xs) ** 2)
    return ns * (1 / norm_ppf1 ** 2 - 1 / norm_ppf2 ** 2)
    
def save_estimation(results, name):
    plt.plot([i + 4 for i in range(1, len(results) + 1)], results, label=name)
    plt.xlabel("n")
    plt.ylabel("Length of interval")
    plt.legend()
    plt.savefig(name + ".png")
    plt.close()  
    
variants = [(segment_length_a, "a"), (segment_length_b, "b")]
    
for seg_len, name in variants:
    results = []
    for n in range(5, max_n + 1):
        chi2_ppf1 = chi2.ppf((1 - trust) / 2.0, n)
        chi2_ppf2 = chi2.ppf((1 + trust) / 2.0, n)
    
        lens = []
        for i in range(iterations):
            observations = [norm.rvs() for j in range(n)]
            lens.append(seg_len(observations))
            
        results.append(mean(lens))
    
    save_estimation(results, name)         

