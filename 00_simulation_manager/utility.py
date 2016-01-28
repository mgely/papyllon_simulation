import time

def two_digit_two_digit_str2int2int(n):
    two_digit_str2inting = two_digit_str2int(n)
    if len(two_digit_str2inting) == 1:
        two_digit_str2inting = '0'+two_digit_str2inting
    return two_digit_str2inting

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