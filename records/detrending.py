from matplotlib import pyplot
import data_loader
from data_loader import max_index
import numpy
import time
import copy
from scipy import optimize

sample_data = data_loader.load_files()
full_sample = sample_data['sample_1.txt']
times = sorted(sample_data['sample_1.txt'].keys())

single_run = full_sample[times[695]]
Comparisons = {'data':[]}

def detrender(data, scale):
    detrended_data = copy.copy(data)
    point_basin = scale/2
    data_size = len(data)
    start = 0
    while start + scale < data_size:
        left_average = float(sum(data[start:start+point_basin]))/point_basin
        right_average = float(sum(data[start+point_basin:start+scale]))/point_basin
        slope = (right_average-left_average)/point_basin
        b = left_average-slope*(start+point_basin/2)
        for index in range(start, start+point_basin):
            if index < point_basin or index > data_size-point_basin:
                detrended_data[index] -= (slope*index+b)
            else:
                detrended_data[index] -= (slope*index+b)*1
        start += point_basin
    return detrended_data

def auto_correlation(frequency_data):
    shift_zero = numpy.array(frequency_data)
    bin_count = len(frequency_data)
    output = []
    for n in range(80):
        output.append(
            numpy.dot(
                shift_zero,
                numpy.roll(shift_zero, n)
                )
            )
    return output

def small_run(data, keys):
    for i in range(620, 623):
        single_run = sample_data['sample_1.txt'][times[i]]
        sub_bin_res(single_run)
        # squared_run = map(lambda x: x**2, single_run)
        flattened_run = detrender(single_run, 80)
        filtered =  auto_correlation(single_run)
        flat_filter =  auto_correlation(flattened_run)
        # fourierd = numpy.fft.fft(filtered)
        print(i, max_index(filtered), max_index(flat_filter))
        # figure, plots = pyplot.subplots(4, sharex=False, sharey=False)
        # plots[0].plot(single_run)
        # plots[1].plot(flattened_run)
        # plots[2].plot(filtered)
        # plots[3].plot(flat_filter)
        # plots[4].plot(numpy.fft.fft(squared_run))
        # peak = numpy.amax(filtered)
        # plots[1].set_ylim([0,peak*1.1])
        # plots[3].set_ylim([-500,5000])
        # pyplot.show()
    return

def sub_bin_res(data):
    detrended_data = detrender(data, 80)
    auto_correlated_data = auto_correlation(detrended_data)
    rough_guess = max_index(auto_correlated_data)
    if rough_guess < 3:
        return 0
    window = 2
    left_bound = rough_guess-window
    right_bound = rough_guess+window+2
    bins = range(left_bound, right_bound)
    fourier_correlation = numpy.fft.fft(auto_correlated_data)
    pyplot.plot(fourier_correlation[1:rough_guess+5])
    pyplot.show()
    subset_data = fourier_correlation[left_bound:right_bound].real
    # fit subset to gaussian
    #http://scipy-cookbook.readthedocs.io/items/FittingData.html
    fitGauss = lambda p, x: p[0]*numpy.exp(-(p[1]-x)**2/p[2])
    errorVal = lambda p, x, y: fitGauss(p, x) - y
    p0 = [float(subset_data[window]), float(rough_guess), 1.0]
    # print(subset_data)
    # print(rough_guess, p0, len(subset_data))
    try:
        print('looking around %d' % rough_guess)
        p1, success = optimize.leastsq(errorVal, p0[:], args=(bins, subset_data))
        Comparisons['data'].append([p1[1], rough_guess])
        print('found %f' % p1[1])
        pyplot.plot(bins, subset_data)
        pyplot.plot(bins, fitGauss(p1, bins))
        pyplot.show()
        return p1[1]
    except:
        return rough_guess

def total_scan(data, keys):
    picks = []
    start = time.time()
    for i in range(len(keys)):
        frequency_data = data[keys[i]]
        picks.append(sub_bin_res(frequency_data))
    end = time.time()
    print(end-start, len(keys), (end-start)/len(keys) )
    return picks


flattened_single = detrender(single_run, 80)

# pyplot.plot(single_run)
# pyplot.plot(flattened_single)
# pyplot.show()

# fouriered_single = numpy.fft.fft(single_run)
# fouriered_flattened = numpy.fft.fft(flattened_single)
# pyplot.plot(fouriered_single)
# pyplot.show()
# pyplot.plot(fouriered_flattened)
# pyplot.show()

# pyplot.plot(auto_correlation(flattened_single))
# pyplot.show()

# pyplot.plot(
#     numpy.fft.fft(auto_correlation(flattened_single))
#     )
# pyplot.show()

small_run(full_sample,times)

# results = total_scan(full_sample,times)
# pyplot.plot(results)
# pyplot.show()
# print(results[500:550])

# print(len(Comparisons['data']))
# for result in Comparisons['data']:
#     print(result)

# sub_bin_res(single_run)
