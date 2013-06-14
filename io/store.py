__author__ = 'SuSh'

from filecreation import writeUserData,writeMessagedata,writeReplyData,writeSubforumdata,getForumUpdated,getSubForumUpdated
from projectutils import *

def addUserMetadata(user):
     writeUserData("data.bin",user)

def writesubForumData(subForumData):
    writeSubforumdata("data.bin",subForumData)
    present_forum_name=subForumData.forumname
    present_subforum_id=subForumData.id
    getForumUpdated(present_forum_name,present_subforum_id)

def writeMessageData(messageData):
    writeMessagedata("data.bin",messageData)
    present_forumname=messageData.forumName
    present_subforum_name=messageData.subForumname
    present_message_id=messageData.id
    getSubForumUpdated(present_forumname,present_subforum_name,present_message_id)

def writereplyData(replydata):
    writeReplyData("data.bin",replydata)



if __name__=="__main__":
    i=0
    while i <200:
        subforum=SubForum("hashing","amani","Education")
        writesubForumData(subforum)
        i+=1

    while i<400:
        msg=Message("Education","hashing","amani",50)
        writeMessageData(msg)
        i+=1