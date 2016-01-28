import time

def two_digit_str2int(n):
    string = str(n)
    if len(string) == 1:
        string = '0'+string
    return string

def gen_timestamp():
    now=time.localtime()
    return two_digit_str2int(now.tm_year) + '_' +\
            two_digit_str2int(now.tm_mon) + '_' +\
            two_digit_str2int(now.tm_mday) + '__' +\
            two_digit_str2int(now.tm_hour) + '_' +\
            two_digit_str2int(now.tm_min) + '_' +\
            two_digit_str2int(now.tm_sec)

def byteify(input):
    '''Utility function to parse all the unicode expressions in a dictionary
    to a string
    '''
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input