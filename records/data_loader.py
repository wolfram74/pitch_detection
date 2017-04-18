import os
import re


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
