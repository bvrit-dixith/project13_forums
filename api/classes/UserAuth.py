__author__ = 'ProfAVR'

from api.serialization import *
import re



class UserAuth(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def validate(self):
        if len(self.username) <= 20 and re.match("^[a-z A-Z]{1}[a-z A-Z]*[0 9]*[a-z A-Z]*$", self.username):
            pass
        else:
            return "Invalid Username: username must consist atmost 20 alphanumerics"
        if len(self.password) >= 6 and len(self.password) <= 10 and re.match("^[a-z A-Z]{1}[a-z A-Z]*[0 9]*[a-z A-Z]*$",
                                                                             self.password):
            pass
        else:
            return "Invalid password: password should be of min length 6 and should contain alphanumerics only"
        return "Valid Credentials"
    def deserializer(self, input):
        dict['message'] = input
        return str(dict)
        pass



