from matplotlib import pyplot
import data_loader
import numpy
import time

def max_index(data):
    index= 0
    value = 0
    positive_deltas = False
    for i in range(0, len(data)-1):
        if not positive_deltas:
            if data[i+1]-data[i] >0:
                positive_deltas = True
        if positive_deltas and (data[i] > value):
            index = i
            value = data[i]
    return index

def total_scan(data, keys):
    picks = []
    start = time.time()
    for i in range(len(keys)):
        frequency_data = data[keys[i]]
        picks.append(max_index(auto_correlation(frequency_data)))
    end = time.time()
    print(end-start, len(keys), (end-start)/len(keys) )
    return picks

sample_data = data_loader.load_files()
times = sorted(sample_data['sample_1.txt'].keys())

single_run = sample_data['sample_1.txt'][times[695]]


pyplot.plot(
    numpy.fft.fft(single_run)
    )
pyplot.show()
