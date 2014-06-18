import re

# used to do some sexy conversions


def hex_to_ascii(hex_string):
    ascii_string = ''
    x = 0
    y = 2
    l = len(hex_string)
    while y <= l:
        ascii_string += chr(int(hex_string[x:y], 16))
        x += 2
        y += 2
    return (ascii_string)

def raw_to_string(raw_read):

    data = [line.strip().split(':') for line in raw_read.split('\n') if line.strip()]
    hex_data = ''
    for each in data:
        if len(each) == 2:
            hex_data += each[1]
    return hex_data

def strip_sapces(some_string):

    pattern = re.compile(r'\s+')
    some_string = re.sub(pattern, '', some_string)
    return some_string