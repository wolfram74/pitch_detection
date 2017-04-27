import os
import re
import numpy

def max_index(data):
    # finds max index after positive derivatives found
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

def maxima_finder(data):
    peaks = []
    last_delta = 0
    for index in range(len(data)-1):
        delta = data[index+1]-data[index]
        # print(delta)
        if delta < 0 and delta*last_delta<0:
            peaks.append(index)
        last_delta = delta
    return peaks

def extrema_finder(data):
    peaks = []
    last_delta = 0
    for index in range(len(data)-1):
        delta = data[index+1]-data[index]
        if delta*last_delta<0:
            peaks.append(index)
        last_delta = delta
    return peaks


def freq_to_note(hertz):
    #establishes 55 hz as note 0
    notes = "A A+ B C C+ D D+ E F F+ G G+".split(' ')
    n = 12*numpy.log(hertz/55)/numpy.log(2)
    n_round = round(n)
    octave = int(n_round/12)
    note = int(n_round % 12)
    return {'n_round': n_round, 'n': n, 'octave':octave, 'note':notes[note]}
