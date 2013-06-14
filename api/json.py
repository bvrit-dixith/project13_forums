__author__ = 'ProfAVR'

import os
import sys
import inspect
import glob
from serialization import *




class json(object):
    def __init__(self):
        pass

    def deserializer(self, input):
        dict={}
        dict['message']=input
        return str(dict)
    pass

    def serializer(self, msg):
        return convert_from_json_object(msg)













