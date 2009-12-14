from math import log, exp

def log_average(items):
    total_v = 0.0
    total_w = 0.0
    for value in items:
        total_v += log(value)
        total_w += 1.0
    return exp(total_v / total_w)
    
def weighted_log_average(items):
    total_v = 0.0
    total_w = 0.0
    for value, weight in items:
        total_v += log(value)*weight
        total_w += weight
    return exp(total_v / total_w)
