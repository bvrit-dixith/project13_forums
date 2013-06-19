__author__ = 'ProfAVR'

import os
import sys
import inspect
import glob
from serialization import *

def convert_list(input_set):
    dict={}
    i,length=0,len(input_set)
    while i < length:
        dict[input_set[i][0]]= input_set[i][1]
        i=i+1
    return str(dict)

class json(object):
    def __init__(self, command = "", forum_name = "", message = ""):
        self.command = command
        self.forum_name = forum_name
        self.message = message
        self.reply = ""

    def deserializer(self,input):
        return str(input)

    def serializer(self,msg):
        print msg,"Line 28 Socket!"
        return convert_from_json_object(str(msg))










