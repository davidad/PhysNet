from math import log, exp

def weighted_log_average(items):
    total_v = 0.0
    total_w = 0.0
    for value, weight in items:
        total_v += log(value)*weight
        total_w += weight
    return exp(total_v / total_w)
