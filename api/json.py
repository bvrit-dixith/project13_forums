__author__ = 'ProfAVR'

import os
import sys
import inspect
import glob
from serialization import *




class json(object):
    dict={}
    def __init__(self, command="", forum_name="", message=""):
        self.command = command
        self.forum_name = forum_name
        self.message = message
        self.reply = ""

    def deserializer(self, input):
        dict['message']=input
        return str(dict)
    pass

    def serializer(self, msg):
        return convert_from_json_object(msg)













