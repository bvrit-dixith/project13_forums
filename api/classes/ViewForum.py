__author__ = 'ProfAVR'
class ViewForum(object):
    def __init__(self, forum_name="" ):
        self.forumname = forum_name
        self.nextForum=-1
        self.prevForum=-1
        self.firstsubForum=-1
        self.num_of_subforums=0
        self.num_of_views=-1

    def deserializer(self, input):
        dict['message'] = input
        return str(dict)
        pass