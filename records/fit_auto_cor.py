from matplotlib import pyplot
import data_loader
from data_loader import max_index, maxima_finder
import numpy
import time
import copy
import sys
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
    auto_correlated_data = numpy.array(auto_correlation(detrended_data))
    rough_guess = max_index(auto_correlated_data)
    print(type(auto_correlated_data))
    # fit subset to gibberish
    #http://scipy-cookbook.readthedocs.io/items/FittingData.html
    def fitGib(p, x):
        # print(len(p),type(p), len(x), type(x))
        # print(p[4], len(x))
        # print(p, x[0:5], p[4]*x[0:5])
        return (
            # p[0]*numpy.exp(-p[1]*x)+
            # p[2]*
            # numpy.exp(-p[3]*x)*
            numpy.cos(p[4]*x)*p[0]
            )
    # fitGib = lambda p, x: p[0]*numpy.exp(-p[1]*x)+p[2]*numpy.exp(-p[3]*x)*numpy.cos(p[4]*x)
    errorVal = lambda p, x, y: fitGib(p, x) - y
    p0 = [
        float(auto_correlated_data[0]),
        float(rough_guess),
        float(auto_correlated_data[0]**(0.5)),
        float(rough_guess),
        float(rough_guess)
    ]
    bins = numpy.array(range(len(auto_correlated_data)))
    # print(subset_data)
    print(rough_guess, p0, len(subset_data))
    # try:
    print(len(bins), len(auto_correlated_data), len(p0))
    print('looking around %d' % rough_guess)
    p1, success = optimize.leastsq(
        errorVal, p0[:],
        args=(bins, auto_correlated_data)
        )
    # Comparisons['data'].append([p1[4], rough_guess])
    print('found %f' % p1[4])
    print(p0)
    print(p1)
    pyplot.plot(auto_correlated_data)
    pyplot.plot(fitGib(p1, bins))
    pyplot.show()
    return p1[4]
    # except Exception as error:
    #     print(error, sys.exc_info()[-1].tb_lineno, type(error))
    #     return rough_guess

def total_scan(data, keys):
    picks = []
    start = time.time()
    for i in range(len(keys)):
        if 380< i and i<900:
            frequency_data = data[keys[i]]
            picks.append(sub_bin_res2(frequency_data))
        else:
            picks.append(0)
    end = time.time()
    runs = 900-380
    print(end-start, runs, (end-start)/runs )
    return picks

def average_gap(data):
    total = data[0]
    for index in range(len(data)-1):
        total+= (data[index+1] - data[index])
    return float(total)/(len(data))

def sub_bin_res2(data):
    detrended_data = detrender(data, 80)
    auto_correlated_data = numpy.array(auto_correlation(detrended_data))
    rough_guess = max_index(auto_correlated_data)
    peaks = maxima_finder(auto_correlated_data)
    if len(peaks) <2:
        return 0
    average_spacing = average_gap(peaks)
    calced_freq = "%.1f" % (average_spacing*21.5)
    note_data = data_loader.freq_to_note(average_spacing*21.5)
    print(rough_guess, average_spacing,
        calced_freq, "%d:%s" % (note_data['octave'], note_data['note']))
    return average_spacing

flattened_single = detrender(single_run, 80)
flat_correlate = auto_correlation(flattened_single)
peaks = maxima_finder(flat_correlate)
# print(peaks, max_index(flat_correlate))
# print(average_gap(peaks), max_index(flat_correlate))


# pyplot.plot(single_run)
pyplot.plot(numpy.fft.fft(flattened_single))
# pyplot.savefig('fourier_detrend_695.png')
pyplot.clf()
pyplot.plot(flattened_single)
# pyplot.savefig('detrended_695.png')
pyplot.clf()
pyplot.plot(flat_correlate)
# pyplot.savefig('detrend_auto_cor_695.png')
pyplot.clf()
pyplot.plot(numpy.fft.fft(flat_correlate))
# pyplot.savefig('fourier_detrend_cor_695.png')
pyplot.clf()


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

# small_run(full_sample,times)

results = total_scan(full_sample,times)
# pyplot.plot(results)
pyplot.plot(results[380:900])
# pyplot.savefig('fundamentals_sample_1.png')
# print(results[500:550])

# print(len(Comparisons['data']))
# for result in Comparisons['data']:
#     print(result)

# sub_bin_res(single_run)
