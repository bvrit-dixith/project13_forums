__author__ = 'ProfAVR'
import datetime
class CreateSubForum(object):
    def __init__(self, name="", forumname="", created_by=""):
        self.name = name
        self.forumname = forumname
        self.createdby = created_by
        self.nextSubForum=-1
        self.prevSubForum=-1
        self.firstQuestion=-1
        self.num_of_questions=0
        self.num_of_views=-1
        self.date_of_creation=datetime.date.today()
        self.last_accessed_time=""

    def deserializer(self, input):
        dict = {}
        dict['message'] = input
        return str(dict)
        pass

