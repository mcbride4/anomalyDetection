import numpy as np


def mean_stddev(value, series, param):
    mean = series.mean()
    std_dev = series.std()
    return abs(value - mean) > param * std_dev


def median_deviation(value, series, param):
    median = series.median()
    demedianed = np.abs(value - median)

    if demedianed == 0 or value == 0:
        return False

    test_statistic = value / demedianed
    if test_statistic < param:
        return True
    else:
        return False



