import math
from statistics import mean, median, stdev

def trunc_precision(num, decimals = 10):
    precision = 10**decimals
    return math.trunc(num * precision) / precision

def avg(nums = [], decimals = 10):
    if len(nums) == 0:
        return 0
    if len(nums) < 3:
        return trunc_precision(mean(nums), decimals)
    std = stdev(nums)
    med = median(nums)
    lower = med - std
    upper = med + std
    try:
        filtered = [x for x in nums if lower < x <upper ]
        return trunc_precision(mean(filtered), decimals)
    except:
        return 0

def list_max(lst = [], max=None):
    over = len(lst) - max
    if over > 0:
        lst = lst[over:]
    return lst