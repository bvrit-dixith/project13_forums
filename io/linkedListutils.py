__author__ = 'amani'

class Forum(object):
    def __init__(self,id,name):
        self.id=id
        self.name=name
        self.nextForum=-1
        self.prevForum=-1
        self.firstsubForum=-1


class SubForum(object):
    def __init__(self,id):
        self.id=id
        self.nextSubForum=None
        self.prevSubForum=None
        self.firstQuestion=None

class Question(object):
    def __init__(self,id):
        self.id=id
        self.nextQuestion=None
        self.prevQuestion=None
        self.firstReply=None

class Reply(object):
    def __init__(self,id):
        self.id=id
        self.nextReply=None
        self.prevReply=None

