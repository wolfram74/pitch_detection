from matplotlib import pyplot
import data_loader
import numpy
import time
import numpy


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

def small_run(data, keys):
    for i in range(620, 623):
        single_run = sample_data['sample_1.txt'][times[i]]
        squared_run = map(lambda x: x**2, single_run)
        filtered =  auto_correlation(single_run)
        fourierd = numpy.fft.fft(filtered)
        print(i, max_index(filtered), max_index(fourierd))
        figure, plots = pyplot.subplots(5, sharex=False, sharey=False)
        plots[0].plot(single_run)
        plots[1].plot(filtered)
        plots[2].plot(fourierd)
        plots[3].plot(numpy.fft.fft(single_run))
        plots[4].plot(numpy.fft.fft(squared_run))
        # peak = numpy.amax(filtered)
        # plots[1].set_ylim([0,peak*1.1])
        plots[3].set_ylim([-500,5000])
        pyplot.show()
    return

sample_data = data_loader.load_files()
full_sample = sample_data['sample_1.txt']
times = sorted(sample_data['sample_1.txt'].keys())

single_run = full_sample[times[695]]

# sample1_processed = total_scan(sample_data['sample_1.txt'], times)
# pyplot.plot(sample1_processed)
# pyplot.show()

# pyplot.plot(single_run)
# pyplot.show()


filtered = auto_correlation(single_run)
pyplot.plot(
    filtered
    )
pyplot.show()
# fourierd = numpy.fft.fft(filtered)
# pyplot.plot(
#     fourierd
#     )
# pyplot.show()
# print(max_index(filtered), max_index(fourierd))


# small_run(sample_data['sample_1.txt'], times)
