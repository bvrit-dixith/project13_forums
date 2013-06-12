__author__ = 'ProfAVR'

import datetime
import re


class User(object):
    def __init__(self, username="", password="", DOB="", email="", ):
        self.username = username
        self.password = password
        self.email = email
        self.birth_date = DOB
        self.join_date = datetime.date.today()

    def validate(self):
        if len(self.username) <= 20 and re.match("^[a-zA-Z]{1}[a-zA-Z]*[0 9]*[a-zA-Z]*$", self.username):
            pass
        else:
            return "Invalid Username: username should be of lesss than 20 characters and should contains alphanumerics"
        if len(self.password) >= 6 and len(self.password) <= 10 and re.match("^[a-zA-Z]{1}[a-zA-Z]*[0-9]*[a-zA-Z]*$",
                                                                             self.password):
            pass
        else:
            return "Invalid password: password should be of min length 6 and should contain alphanumerics only"
        if len(self.email) <= 30 and re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                                              self.email):
            pass
        else:
            return "Invalid Email: email should be a valid one"
        year, month, date = serialize_date(str(self.birth_date))
        try:
            if datetime.date.today() - datetime.date(year, month, date):
                return True
        except Exception as ex:
            return "Invalid Date"

    def deserializer(self, input):
        dict={}
        dict['message'] = input
        return str(dict)
        pass

def serialize_date(input):
    print input
    print type(input)
    check = '['
    year = ""
    month = ""
    date = ""
    for i in range(len(input)):
        if check == '[':
            if input[i] == ',':
                check = ','
                continue
            if i == 0:
                continue
            year += input[i]
            continue
        if check == ',':
            if input[i] == ',':
                check = ']'
                continue
            month += input[i]
            continue
        if check == ']':
            if input[i] == ']':
                break
            date += input[i]
            continue
    return int(year), int(month), int(date)




