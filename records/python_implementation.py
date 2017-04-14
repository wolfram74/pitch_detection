from matplotlib import pyplot
import numpy
# from scipy import integrate
import os
import re

def load_files():
    print('loading files')
    output = {}
    file_addresses = os.listdir('.')
    sample_regx = re.compile("\d.txt")
    for address in file_addresses:
        match = sample_regx.search(address)
        # print(address, match, sample_regx)
        if(match):
            print('huzzah', address)
            output[address] = parse_file('./%s' % address)
            return output
    return output

def parse_file(address):
    # file has formatted lines timeStamp, frequency data
    stored_data = open(address, 'r')
    output = {}
    for line in stored_data:
        formatted_line = [int(string) for string in line.split(',')]
        time_stamp=formatted_line.pop(0)
        output[time_stamp] = formatted_line
    return output

def cepstrum_filter(frequency_data):
    log_of_amp = numpy.log(frequency_data)
    cleaned_log_of_amp = [ 0 if (val < -1) else val  for val in log_of_amp]
    ceptstrum = numpy.fft.fft(cleaned_log_of_amp)
    magnitude_cepstrum = [abs(value) for value in ceptstrum]
    return cleaned_log_of_amp, magnitude_cepstrum

sample_data = load_files()

print(sample_data.keys())
# print(sample_data['sample_1.txt'].keys())
# print(sorted(sample_data['sample_1.txt'].keys())[695])
times = sorted(sample_data['sample_1.txt'].keys())
# print(test_case_time)
for time_index in range(100, 750):
    time_stamp = times[time_index]
    frequency_data = sample_data['sample_1.txt'][time_stamp]
    log_of_amp, cepstrum = cepstrum_filter(frequency_data)
    top_signal = 0
    index_of_top = 0
    for c_index in range(10,500):
        if(cepstrum[c_index] > top_signal):
            index_of_top = c_index
            top_signal = cepstrum[c_index]
    print(time_index, index_of_top, index_of_top*22)
    if time_index % 50 == -1:
        fig = pyplot.figure(1)
        ax1 = fig.add_subplot(111)
        figure, process_plots = pyplot.subplots(3, sharex=True, sharey=False)
        process_plots[0].plot(range(len(frequency_data)),frequency_data)
        process_plots[1].plot(range(len(frequency_data)),log_of_amp)
        process_plots[2].plot(range(len(frequency_data)),cepstrum)
        pyplot.show()
# time step 695 in sample_1 has pretty wide spacing


