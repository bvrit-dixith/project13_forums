__author__ = 'pranee'
import string
input_set ="{'message':'hu','forum_name':'hry','req_type':'create'}"

def string(input, index):
    string = ''
    while input[index] != '"' and input[index] != "'":
        string += input[index]
        index += 1
    return string, index + 1

def number(input, index):
    num_string = ''
    while input[index] != ':' and input[index] != ',' and input[index] != '}':
        num_string += input[index]
        index += 1
    num_string = num_string.replace(' ', '')
    return int(num_string), index

def dict(input, index):
    dict_gen = {}
    key, value, quote_hit, val = None, None, False, None
    while input[index] != '}':
        if input[index] == '"' or input[index] == "'":
            val, index = string(input, index+1)
            if quote_hit:
                value = val
            else:
                key = val
        elif input[index] in '0123456789':
            val, index = number(input, index)
            if quote_hit:
                value = val
            else:
                key = val
        elif input[index] == '[':
            val, index = array(input, index+1)
            if quote_hit:
                value = val
            else:
                key = val
        elif input[index] == ',':
            quote_hit = False
            dict_gen[key] = value
            index += 1
        elif input[index] == ':':
            quote_hit = True
            index += 1
        elif input[index] == '{':
            val, index = dict(input, index + 1)
            if quote_hit:
                value = val
            else:
                key = val
        else:
            index += 1
    if key is not None and value is not None:
        dict_gen[key] = value
    print dict_gen, index + 1
    return dict_gen, index + 1

def array(input, index):
    array_gen = []
    while input[index] != ']':
        if input[index] == '"' or input[index] == "'":
            val, index = string(input, index + 1)
            array_gen.append(val)
        elif input[index] == '[':
            val, index = array(input,index + 1)
            array_gen.append(val)
        elif input[index] in '0123456789':
            val, index = number(input, index)
            array_gen.append(val)
        elif input[index] == '{':
            dict_return, index = dict(input, index + 1)
            array_gen.append(dict_return)
        else:
            index += 1
    return array_gen, index + 1


def convert_from_json_object(input):
    i, length = 0, len(input)
    json_dict = None
    while i < length:
        if input[i] == '{':
            json_dict, i = dict(input, i + 1)
        else:
            i += 1
    return " ".join(json_dict.values())



if __name__=="__main__":
    c=convert_from_json_object(input_set)
    print c
