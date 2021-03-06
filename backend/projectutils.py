__author__ = 'amani'

class Forum(object):
    def __init__(self,id,name):
        self.id=id
        self.name=name
        self.nextForum=-1
        self.prevForum=-1
        self.firstsubForum=-1
        self.num_of_subforums=0
        self.num_of_views=-1


class SubForum(object):
    def __init__(self,name,createdby,forumname):
        self.id=-1
        self.name=name
        self.forumname=forumname
        self.createdby=createdby
        self.nextSubForum=-1
        self.prevSubForum=-1
        self.firstQuestion=-1
        self.num_of_questions=0
        self.num_of_views=-1
        self.date_of_creation=""
        self.last_accessed_time=""

class Message(object):
    def __init__(self,forumname,subForumname,postedby,length,msg):
        self.forumName=forumname
        self.subForumname=subForumname
        self.postedby=postedby
        self.length=length
        self.id=-1
        self.nextQuestion=-1
        self.prevQuestion=-1
        self.firstReply=-1
        self.messagedata=-1
        self.num_of_replies=0
        self.msg=msg
        self.num_of_views=-1
        self.num_of_likes=-1
        self.isResolved=False

class Reply(object):
    def __init__(self,forumname,subForumname,message_id,postedby,msgLength,msg):
        self.id=-1
        self.q_id=message_id
        self.forumname=forumname
        self.subForumname=subForumname
        self.postedby=postedby
        self.nextReply=-1
        self.prevReply=-1
        self.replydata=-1
        self.length=msgLength
        self.msg=msg
        self.num_of_views=-1
        self.num_of_likes=-1


class User(object):
    def __init__(self,name,password,mail_id,birthdate,joiningdate):
        self.id=-1
        self.name=name
        self.password=password
        self.mail=mail_id
        self.birth_date=birthdate
        self.join_date=joiningdate
        self.num_of_posted_messages=0