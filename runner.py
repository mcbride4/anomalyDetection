import csv
import time
import datetime
import pandas
import matplotlib.pyplot as plt
import re
import sys

from algorithms import (mean_stddev, median_deviation)


class Runner:

    def __init__(self, filename):
        self.filename = filename
        self.path = "data/" + filename
        self.time_series = []
        self.read_file()
        self.anomalies = []
        self.results = []
        self.series = self.__set_series()
        self.algorithms = [mean_stddev, median_deviation]
        self.results_true = []

    def read_file(self):
        with open(self.path, 'rb') as csv_file:
            reader = csv.reader(csv_file)
            reader.next()  # skip line 'timestamp' => 'value'
            self.__create_time_series(reader)

    def get_results(self):
        return self.results

    def run(self, algo, param):
        self.results = [self.run_algorithm(i, algo, param) for i in xrange(len(self.time_series))]

    def run_algorithm(self, index, algo, param):
        series_part = self.__set_series_part(index)
        value = self.series[index]
        check = self.algorithms[algo](value, series_part, param)
        if check:
            self.add_to_anomalies(index)
            # print "anomaly fonund! value: {0}, index: {1}".format(value, index)
        return check

    def add_to_anomalies(self, index):
        self.anomalies.append(self.time_series[index][1])

    def define_range(self, i):
        if i<50:
            return self.time_series[:2 * i + 1]
        if i+50 > len(self.time_series):
            return self.time_series[len(self.time_series) - 2 * (len(self.time_series) - i) - 1:]
        return self.time_series[i - 50:i + 51]

    def update_results(self):
        for i in xrange(len(self.results)):
            if self.results[i]:
                self.results[i] = self.series[i]

    def plot_with_anomalies(self):
        plt.plot(self.series, 'ro', self.results, 'b^')
        plt.show()

    def add_anomalies_to_results(self):
        for i in xrange(len(self.results)):
            if self.results[i]:
                self.results_true.append(self.results[i])

    def __create_time_series(self, reader):
      for row in reader:
          s = time.mktime(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").timetuple())
          self.time_series.append([s, float(row[1])])

    def __set_series_part(self, index):
          return pandas.Series(x[1] for x in self.define_range(index))

    def __set_series(self):
        return pandas.Series([x[1] for x in self.time_series])


def set_param_for_file(filename):
    if filename == 'ec2_cpu_utilization_5f5533.csv':
        param = [2.5, 6]
    elif re.match('exchange-\d.*\.csv', filename):
        param = [2.5, 1.5]
    elif re.match('Twitter.*\.csv', filename):
        param = [3, 1]
    else:
        param = [3, 6]
    return param


def create_fusion_results():
    fusion_results = list(runners[0].results)
    for j in xrange(len(runner.algorithms) - 1):
        for i in xrange(len(runners[j+1].results)):
            if runners[j+1].results[i]:
                fusion_results[i] = runners[j+1].results[i]
    return fusion_results


def do_the_staff(i, plot_results):
    runners.append(Runner(filename))
    runners[i].run(i, set_param_for_file(filename)[i])
    runners[i].update_results()
    if plot_results:
        runners[i].plot_with_anomalies()
    runners[i].add_anomalies_to_results()


if __name__ == '__main__':

    filename = 'ec2_cpu_utilization_5f5533.csv'
    filename = 'art_daily_nojump.csv'
    filename = 'exchange-3_cpc_results.csv'

    try:
        if sys.argv[1]:
            filename = sys.argv[1]
    except:
        print "default filename chosen"

    try:
        if sys.argv[2]:
            plot_results = sys.argv[1]
    except:
        plot_results = 0

    runner = Runner(filename)
    runners = []

    for i in xrange(len(runner.algorithms)):
        do_the_staff(i, plot_results)
        print "number of anomalies: " + str(len(runners[i].anomalies))
        print "length of input data: " + str(len(runners[i].time_series))

    fusion = create_fusion_results()
    fusion_anomalies = [x for x in fusion if x]
    print "total number of anomalies: " + str(len(fusion_anomalies))

