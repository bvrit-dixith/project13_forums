__author__ = 'pranee'
class viewQuestion(object):
    def __init__(self, forum_name="", sub_forum_name="",question=""):
        self.forum_name = forum_name
        self.name = sub_forum_name
        self.question = question

    def deserializer(self, input):
        dict={}
        dict['message'] = input
        return str(dict)
        pass