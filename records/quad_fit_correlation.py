from matplotlib import pyplot
import data_loader
from data_loader import max_index, maxima_finder
import numpy
import time
import copy
import sys

sample_data = data_loader.load_files()
full_sample = sample_data['sample_1.txt']
times = sorted(sample_data['sample_1.txt'].keys())

single_run = full_sample[times[695]]

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

def average_gap(data):
    total = data[0]
    for index in range(len(data)-1):
        total+= (data[index+1] - data[index])
    return float(total)/(len(data))

def sub_bin_res(data):
    detrended_data = detrender(data, 80)
    auto_correlated_data = numpy.array(auto_correlation(detrended_data))
    rough_guess = max_index(auto_correlated_data)
    extrema = data_loader.extrema_finder(auto_correlated_data)
    if len(extrema) <2:
        return 0
    # print(extrema)
    fits = [
        data_loader.quad_fitter(
            center,
            auto_correlated_data[center-1:center+2]
            )
        for center in extrema
        ]
    # print(fits)
    fit_extrema = map(lambda p: -1.0*p[1]/(2.0*p[0]), fits)
    # print(fit_extrema)
    # for ind in range(len(extrema)):
        # print(extrema[ind], fits[ind], fit_extrema[ind])
    average_result = average_gap(fit_extrema)
    lin_fit_result = data_loader.linear_even_fit(fit_extrema)
    #(spacing/2)n=extrema
    # calced_spacing = lin_fit_result['fit']*2
    calced_spacing = average_result*2
    # print(lin_fit_result)
    calced_freq = "%.1f" % (calced_spacing*21.5)
    note_data = data_loader.freq_to_note(calced_spacing*21.5)
    print(rough_guess, calced_spacing,
        calced_freq, "%d:%s" % (note_data['octave'], note_data['note']))
    return calced_spacing

def total_scan(data, keys):
    picks = []
    start = time.time()
    for i in range(len(keys)):
        if 380< i and i<900:
            frequency_data = data[keys[i]]
            picks.append(sub_bin_res(frequency_data))
        else:
            picks.append(0)
    end = time.time()
    runs = 900-380
    print(end-start, runs, (end-start)/runs )
    return picks


print( sub_bin_res(single_run))

results = total_scan(full_sample,times)
pyplot.plot(results[380:900])
pyplot.show()
