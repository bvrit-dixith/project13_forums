__author__ = 'SuSh'

from filecreation import writeUserData,writeMessagedata,writeReplyData,writeSubforumdata

def addUserMetadata(user):
     writeUserData("data.bin",user)

def writesubForumData(subForumData):
    writeSubforumdata("data.bin",subForumData)

def writeMessageData(messageData):
    writeMessagedata("data.bin",messageData)

def writereplyData(replydata):
    writeReplyData("data.bin",replydata)

if __name__=="__main__":
    pass
    