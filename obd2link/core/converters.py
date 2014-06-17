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
