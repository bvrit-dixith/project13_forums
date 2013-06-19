__author__ = 'pranee'
class ViewSubForum(object):
    def __init__(self, forum_name="", sub_forum_name="",list_id=None):
        self.forumname = forum_name
        self.name = sub_forum_name
        self.id= list_id


    def deserializer(self, input):
        dict={}
        dict['message'] = input
        return str(dict)
        pass
