from matplotlib import pyplot
import data_loader
import numpy
import time
def auto_correlation(frequency_data):
    output = []
    bin_count = len(frequency_data)
    for n in range(bin_count):
        total = 0
        for offSet in range(bin_count-n):
            total += frequency_data[n]*frequency_data[offSet]
        output.append(total)
    return output

def max_index(data):
    index= 0
    value = 0
    for i in range(len(data)):
        if data[i] > value:
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

sample1_processed = total_scan(sample_data['sample_1.txt'], times)
# pyplot.plot(single_run)
# pyplot.show()

pyplot.plot(sample1_processed)
pyplot.show()

# pyplot.plot(auto_correlation(single_run))
# pyplot.show()
