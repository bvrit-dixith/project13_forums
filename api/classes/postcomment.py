__author__ = 'pranee'
class PostComment(object):
    def __init__(self, forum_name="", sub_forum_name="",created_by="",question="",answer=""):
        self.forum_name = forum_name
        self.sub_forum_name = sub_forum_name
        self.createf_by = created_by
        self.question = question
        self.answer = answer
