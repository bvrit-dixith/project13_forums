__author__ = 'ProfAVR'

import os
import sys
import inspect
import glob
from serialization import *

def open_test_file(file, mode="rt"):
    import inspect, os.path
    mod_file = inspect.getfile(inspect.currentframe())
    mod_dir = os.path.dirname(mod_file)
    test_file = os.path.join(mod_dir, file)
    return open(test_file, mode)

#utility function which returns a full path which is (currentmoduledir + file), useful to generate temporary files in
# in the same directory as the module without worrying about the current path set by pycharm etc.
def get_file_path(file):
    mod_file = inspect.getfile(inspect.currentframe())
    mod_dir = os.path.dirname(mod_file)
    return os.path.join(mod_dir, file)

def write_file(filename,msg):
    mod_file = inspect.getfile(inspect.currentframe())
    mod_dir = os.path.dirname(mod_file)
    file=os.path.join(mod_dir, filename)
    with open(file,"a") as f:
        f.write(msg)
    f.close()

def create_file(filename,message):
    f=open(filename,"wb")
    f.write(message)
    f.close()

def getindex(message,index):
    for i in message:
        if i == ":":
            index += 1
            break
        else:
            index += 1
    return index

def getstring(message,index):
    str = ""
    for index in range(len(message)):
        if message[index] == ",":
            index += 1
            break
        else:
            str += message[index]
    return str,index


def my_len(input):
    len = 0
    for ch in input:
        len += 1
    return len


def endIndexOf(whole,sub):
    i = 0
    j = 0
    len = my_len(whole)
    sublen = my_len(sub)
    while i <= len-sublen :
        if whole[i] == sub[j]:
            presence = True
            j = 1
            while j < sublen:
                if whole[i+j] != sub[j]:
                    presence = False
                    break
                j += 1
            if presence:
                return (i+j-1)
            i = i+j-1
            j=0
        i += 1
    return -1

def getUptoChar(input,start,delimiter):
    buff = str()
    try:
        while input[start] != delimiter:
            buff += input[start]
            start += 1
    except IndexError as ie:
        pass
    return buff

class json(object):
    def __init__(self, command = "", forum_name = "", message = ""):
        self.command = command
        self.forum_name = forum_name
        self.message = message
        self.reply = ""

    def deserializer(self,input):
        return str(input)

    def serializer(self,msg):
        return convert_from_json_object(msg)










