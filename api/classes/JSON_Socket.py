__author__ = 'ProfAVR'

import os
import sys
import inspect
import glob
from api.serialization import *

def convert_list(input_set):
    dict={}
    id_list=[None]*len(input_set)
    i,length=0,len(input_set)
    print input_set,"input_set"
    while i < length:
        dict[input_set[i][1]]= input_set[i][2]
        id_list[i]=input_set[i][0]
        i=i+1
    a= str(dict)+str(';')+str(id_list)
    return a

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










