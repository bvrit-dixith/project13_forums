__author__ = 'ProfAVR'
class CreateSubForum(object):
    def __init__(self, forum_name="", sub_forum_name="", created_by=""):
        self.forum_name = forum_name
        self.sub_forum_name = sub_forum_name
        self.created_by = created_by
    def deserializer(self, input):
        dict['message'] = input
        return str(dict)
        pass

