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
