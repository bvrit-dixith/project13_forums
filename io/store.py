__author__ = 'SuSh'

from filecreation import createfile,writeUserData,writeForumData,retrieve
from project13_forums.project13_forums1.server.user import *
from projectutils import *




def addUserMetadata(user):
     userdata=[]
     userdata.append(user.username)
     userdata.append(user.password)
     userdata.append(user.email)
     userdata.append(user.birth_date)
     userdata.append(user.join_date)
     userdata.append(user.member_of_month)
     userdata.append(user.message_id)
     #retrieve("data.bin")
     writeUserData("data.bin",userdata)

def writesubForumData(filename,subForumData):
    pass

if __name__=="__main__":
    pass
    