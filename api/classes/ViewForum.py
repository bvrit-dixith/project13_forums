__author__ = 'ProfAVR'
class ViewForum(object):
    def __init__(self, forum_name="" ):
        self.forum_name = forum_name

    def deserializer(self, input):
        dict['message'] = input
        return str(dict)
        pass