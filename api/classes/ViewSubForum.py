__author__ = 'pranee'
class ViewSubForum(object):
    def __init__(self, forum_name="", sub_forum_name=""):
        self.forum_name = forum_name
        self.sub_forum_name = sub_forum_name

    def deserializer(self, input):
        dict['message'] = input
        return str(dict)
        pass
