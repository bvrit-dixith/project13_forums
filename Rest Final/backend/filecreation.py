__author__ = 'amani'

import os
import inspect
import datetime
import struct
from projectutils import *


#update forum metadata in the 1Gb file
def forumcreation():
    forum_count=0
    offset=70
    forum_list=["Education","Sports","Entertainment","Technology","News","Health","Miscellaneous"]
    forum_object_list=[]
    for forum_name in forum_list:
        id=1030+offset*forum_count
        forum_object=Forum(id=id,name=forum_name)
        forum_object_list.append(forum_object)
        forum_count+=1
    num_of_forums=len(forum_object_list)
    #print num_of_forums
    i=0
    while i<num_of_forums-1:
        forum_object_list[i].nextForum=forum_object_list[i+1].id
        i+=1
    while i>0:
        forum_object_list[i].prevForum=forum_object_list[i-1].id
        i-=1
    for forum_object in forum_object_list:
        writeForumData("data.bin",forum_object)
    #print "successfully forums created"

#creates a 1GB file
def createfile(filename):
    file=getFilePath(filename)
    f=open(file,"wb")
    f.truncate(1024*1024*1024)
    f.seek(1526)
    f.write(struct.pack('I',0)) #user count
    f.seek(1026)
    f.write(struct.pack('I',0))     #forum count
    f.seek(43526)
    f.write(struct.pack('I',0))     #sub forum count
    f.seek(86226)
    f.write(struct.pack('I',0))        #message count
    f.seek(2500000)
    f.write(struct.pack('I',0))         #reply count
    f.seek(4000000)
    f.write(struct.pack('I',4194304))   #address of free message unit
    f.seek(104857620)
    f.write(struct.pack('I',104857630))     #address of free reply unit
    forumcreation()
    f.close()

#writes forum metadata into a file
def writeForumData(filename,forumdata):
    file=getFilePath(filename)
    with open(file,"rb+") as f:
        f.seek(1026)
        forum_count=struct.unpack('I',f.read(4))[0]
        f.seek(1030+70*forum_count)
        f.write(struct.pack('i',forumdata.id))
        f.write(struct.pack('30s',forumdata.name))
        f.write(struct.pack('i',forumdata.nextForum))
        f.write(struct.pack('i',forumdata.prevForum))
        f.write(struct.pack('i',forumdata.firstsubForum))
        f.write(struct.pack('i',forumdata.num_of_subforums))
        f.write(struct.pack('i',forumdata.num_of_views))
        forum_count+=1
        f.seek(1026)
        f.write(struct.pack('I',forum_count))
    f.close()

#writes user metadata into a file
def writeUserData(filename,userdata):
    file=getFilePath(filename)
    with open(file,"rb+") as f:
        f.seek(1526)
        user_count=struct.unpack('I',f.read(4))[0]
        user_id=1530+104*user_count
        f.seek(user_id)
        f.write(struct.pack('i',userdata.id))
        f.write(struct.pack('20s',userdata.name))
        f.write(struct.pack('10s',userdata.password))
        f.write(struct.pack('30s',userdata.mail))
        t=datetime.date(userdata.birth_date[0],userdata.birth_date[1],userdata.birth_date[2])
        strTime=t.strftime('%y-%m-%d')
        f.write(struct.pack('10s',strTime))
        joinTime=userdata.join_date.strftime('%y-%m-%d')
        f.write(struct.pack('10s',joinTime))
        f.write(struct.pack('i',userdata.num_of_posted_messages))
        user_count+=1
        f.seek(1526)
        f.write(struct.pack('I',user_count))
    f.close()
    return True

#writes subforum metadata into a file
def writeSubforumdata(filename,subforumData):
    file=getFilePath(filename)
    with open(file,"rb+") as f:
        f.seek(43526)
        subforum_count=struct.unpack('I',f.read(4))[0]
        subforum_id=43530+124*subforum_count
        f.seek(subforum_id)
        subforumData.id=subforum_id
        f.write(struct.pack('i',subforumData.id))
        f.write(struct.pack('30s',subforumData.name))
        f.write(struct.pack('30s',subforumData.forumname))
        f.write(struct.pack('20s',subforumData.createdby))
        pos=f.tell()
        if not subforum_count==0:
            f.seek(43530+124*(subforum_count-1))
            subforumData.prevSubForum=struct.unpack('i',f.read(4))[0]
        subforumData.nextSubForum=43530+124*(subforum_count+1)
        f.seek(pos)
        f.write(struct.pack('i',subforumData.prevSubForum))
        f.write(struct.pack('i',subforumData.nextSubForum))
        f.write(struct.pack('i',subforumData.firstQuestion))
        f.write(struct.pack('i',subforumData.num_of_questions))
        f.write(struct.pack('i',subforumData.num_of_views))
        f.write(struct.pack('10s',subforumData.date_of_creation))
        f.write(struct.pack('10s',subforumData.last_accessed_time))
        subforum_count+=1
        f.seek(43526)
        f.write(struct.pack('I',subforum_count))
    f.close()
    return True

#writes message metadata into a file
def writeMessagedata(filename,msgdata):
    file=getFilePath(filename)
    with open(file,"rb+") as f:
        f.seek(86226)
        message_count=struct.unpack('I',f.read(4))[0]
        message_id=86230+120*message_count
        f.seek(message_id)
        msgdata.id=message_id
        f.write(struct.pack('i',msgdata.id))
        f.write(struct.pack('30s',msgdata.forumName))
        f.write(struct.pack('30s',msgdata.subForumname))
        f.write(struct.pack('20s',msgdata.postedby))
        f.write(struct.pack('I',msgdata.length))
        f.write(struct.pack('i',msgdata.nextQuestion))
        f.write(struct.pack('i',msgdata.prevQuestion))
        f.write(struct.pack('i',msgdata.firstReply))
        msg_id=actualMsgStore(msgdata)                      #store actual message
        f.write(struct.pack('i',msg_id))                    #stores location of the message
        f.write(struct.pack('i',msgdata.num_of_replies))
        f.write(struct.pack('i',msgdata.num_of_views))
        f.write(struct.pack('i',msgdata.num_of_likes))
        f.write(struct.pack('?',msgdata.isResolved))
        message_count+=1
        f.seek(86226)
        f.write(struct.pack('I',message_count))
    f.close()
    return True

def writeReplyData(filename,replydata):
    file=getFilePath(filename)
    with open(file,"rb+") as f:
        print "enter io"
        f.seek(2500000)
        reply_count=struct.unpack('I',f.read(4))[0]
        reply_id=2500004+120*reply_count
        f.seek(reply_id)
        replydata.id=reply_id
        f.write(struct.pack('i',replydata.id))
        f.write(struct.pack('30s',replydata.forumname))
        f.write(struct.pack('30s',replydata.subForumname))
        f.write(struct.pack('20s',replydata.postedby))
        f.write(struct.pack('i',replydata.nextReply))
        f.write(struct.pack('i',replydata.prevReply))
        replydata_id=actualReplyStore(replydata)
        f.write(struct.pack('i',replydata_id))
        f.write(struct.pack('i',replydata.num_of_views))
        f.write(struct.pack('i',replydata.num_of_likes))
        reply_count+=1
        f.seek(2500000)
        f.write(struct.pack('I',reply_count))
    f.close()
    print "exited io"

    return True

#gets file path
def getFilePath(filename):
    mod_file=inspect.getfile(inspect.currentframe())
    mod_dir=os.path.dirname(mod_file)
    file=os.path.join(mod_dir,filename)
    return file

def checkUsername(username):
    file=getFilePath("data.bin")
    f=open(file,"rb")
    f.seek(1526)
    user_count=struct.unpack('I',f.read(4))[0]
    checked_users=0
    f.seek(1530)
    while checked_users<user_count:
        present_username=""
        char=f.read(1)
        while char!="}":
            present_username+=char
            char=f.read(1)
        if present_username==username:
            return True
    else:
        return False


def getForumUpdated(present_forum_name,present_subforum_id):
    file=getFilePath("data.bin")
    f=open(file,"rb+")
    i=0
    f.seek(1026)
    count=struct.unpack('i',f.read(4))[0]           #reads num of forums
    while i<count:
        f.seek(1034+70*i)
        temp=f.read(30).strip('\x00')
        if temp==present_forum_name:
            f.seek(1072+70*i)
            break
        i+=1
    else:
        pass
    if struct.unpack('i',f.read(4))[0]==-1:
        f.seek(1072+70*i)
        f.write(struct.pack('i',present_subforum_id))
    f.seek(1076+70*i)
    count1=struct.unpack('I',f.read(4))[0]
    count1+=1
    f.seek(1076+70*i)
    f.write(struct.pack('I',count1))                #resets num of subforums in a forum
    f.close()
    return True


def getSubForumUpdated(present_forumname,present_subforum_name,present_message_id,msgData):
    file=getFilePath("data.bin")
    f=open(file,"rb+")
    i=0
    f.seek(1026)                            #reads num of forums
    count=struct.unpack('i',f.read(4))[0]
    while i<count:
        f.seek(1034+70*i)
        temp=f.read(30).strip('\x00')
        if temp==present_forumname:
            f.seek(1072+70*i)
            first_subForum_id=struct.unpack('I',f.read(4))[0]
            break
        i+=1
    else:
        pass
    f.seek(1076+70*i)
    numOfSubF=struct.unpack('I',f.read(4))[0]       #reads num of subforums
    i=0
    while i<numOfSubF:
        f.seek((first_subForum_id+124*i)+4)
        subFName=f.read(30).strip('\x00')
        pos=f.tell()
        if subFName==present_subforum_name:
            f.seek(pos+58)
            break
        i+=1
    else:
        pass
    if struct.unpack('i',f.read(4))[0]==-1:
        f.seek(pos+58)
        f.write(struct.pack('I',present_message_id))
        msgData.prevQuestion=first_subForum_id+124*i
    else:
        msgData.prevQuestion=present_message_id-120   #links to previous message in the same subforum
    msgData.nextQuestion=present_message_id+120         #links to next message in the same subforum
    msgid=msgData.id
    f.seek(msgid+88)
    f.write(struct.pack('I',msgData.nextQuestion))
    f.write(struct.pack('I',msgData.prevQuestion))
    f.seek(43626+124*i)
    count1=struct.unpack('I',f.read(4))[0]
    count1+=1
    f.seek(43626+124*i)
    f.write(struct.pack('i',count1)) #writes message count in the subforum
    f.close()
    return True

def getFirstSubforumId(forumname):
    file=getFilePath("data.bin")
    f=open(file,"rb+")
    flag=0
    f.seek(1026)
    print forumname, "in store"
    count=struct.unpack('I',f.read(4))[0]
    i=0
    while i<count:
        print "entered while"
        f.seek(1034+70*i)
        name=f.read(30).strip('\x00')
        print name
        if name==forumname:
            flag=1
            break
        i+=1
    if flag==1:
        f.seek(1072+70*i)
        id=struct.unpack('I',f.read(4))[0]
        num=struct.unpack('I',f.read(4))[0]
        return id,num                           #returns first subforumid, no of subforums
    else:
        return "No such forum"





def getFirstMessageId(link1,count,subForumname):
    print "link1",link1,"count",count,subForumname
    file=getFilePath("data.bin")
    f=open(file,"rb+")
    i=0
    while i<count:
        f.seek(link1+124*i+4)
        temp=f.read(30).strip('\x00')
        print temp
        if temp==subForumname:
            print "found"
            break
        i+=1
    else:
        print "no such subforum"
    f.seek(58,1)  #seeks to the place where first message id is stored
    id=struct.unpack('I',f.read(4))[0]
    count=struct.unpack('I',f.read(4))[0]
    print id,count
    return id,count


def getRequiredMessageId(link2,count1,question_id,id,replydata):
    file=getFilePath("data.bin")
    f=open(file,"rb+")
    i=0
    while i<count1:
        f.seek(link2+120*i)
        if question_id==struct.unpack('I',f.read(4))[0]:
            break
        i+=1
    else:
        print "no question with given id"
    pos=f.tell()
    f.seek(pos+92)
    if struct.unpack('i',f.read(4))[0]==-1:    #update first reply
        f.seek(pos+92)
        f.write(struct.pack('I',id))
        replydata.prevReply=replydata.q_id
    else:
        replydata.prevReply=id-120
    f.seek(pos+100)
    count=struct.unpack('I',f.read(4))[0]
    count+=1                                #update num of replies
    f.seek(pos+100)
    f.write(struct.pack('I',count))
    replydata.nextReply=id+120
    f.seek(id+84)
    f.write(struct.pack('I',replydata.nextReply))   #update previous and next replies
    f.write(struct.pack('I',replydata.prevReply))
    f.close()
    return True

def actualMsgStore(messageObj):
    file=getFilePath("data.bin")
    f=open(file,"rb+")
    f.seek(4000000)
    address=struct.unpack('I',f.read(4))[0]
    f.seek(address)
    f.write(messageObj.msg)
    position=f.tell()
    f.seek(4000000)                         #adress of free memory unit in message block
    f.write(struct.pack('I',position))
    updateUserDetails(messageObj)
    return address

# updates user posted message count
def updateUserDetails(messageObj):
    uname=messageObj.postedby
    file=getFilePath("data.bin")
    f=open(file,"rb+")
    f.seek(1526)
    usercount=struct.unpack('I',f.read(4))[0]
    i=0
    while i<usercount:
        f.seek(1534+i*104)
        temp=f.read(20).strip('\x00')
        if temp==uname:
            f.seek(60,1)
            count=struct.unpack('I',f.read(4))[0]
            count+=1
            f.seek(-4,1)
            f.write(struct.pack('I',count))
            break
        i+=1
    else:
        print "no such user exists"


def actualReplyStore(replyObj):
    file=getFilePath("data.bin")
    f=open(file,"rb+")
    f.seek(104857620)
    address=struct.unpack('I',f.read(4))[0]
    f.seek(address)
    f.write(replyObj.msg)
    position=f.tell()
    f.seek(104857620)                         #adress of free memory unit in reply block
    f.write(struct.pack('I',position))
    updateUserDetails(replyObj)
    return address

def getQuestionIds(link2,num_of_msgs):
    idList=[]
    postedBy_list=[]
    if num_of_msgs==0:
        print "no questions in selected forum"
        return idList,postedBy_list
    else:
        file=getFilePath("data.bin")
        f=open(file,"rb+")
        i=0
        while i<num_of_msgs:
            postField=link2+64
            f.seek(postField)
            postedBy_list.append(f.read(20).strip('\x00'))
            link=link2+88
            f.seek(link+12)
            idList.append(struct.unpack('I',f.read(4))[0])
            f.seek(link)
            link2=struct.unpack('I',f.read(4))[0]
            i+=1
    return idList,postedBy_list

def getFirstReplyId(link2,count1,id):
    file=getFilePath("data.bin")
    f=open(file,"rb+")
    i=0
    while i<count1:
        f.seek(link2+120*i)
        if id==struct.unpack('I',f.read(4))[0]:
            break
        i+=1
    else:
        print "no question with given id"
    pos=f.tell()
    f.seek(pos+92)
    id= struct.unpack('i',f.read(4))[0]
    f.seek(pos+100)
    num_of_replies=struct.unpack('i',f.read(4))[0]
    return id,num_of_replies

def getReplies(link3,count):
    replyList=[]
    i=0
    if link3==-1 or count==0:
        print "question has no replies posted"

    else:
        file=getFilePath("data.bin")
        f=open(file,"rb+")
        while i<count:
            link=link3+92
            f.seek(link)
            replyList.append(struct.unpack('I',f.read(4))[0])
            f.seek(link3+84)
            link3=struct.unpack('I',f.read(4))[0]
            i+=1
        f.seek(104857620)
        replyList.append(struct.unpack('I',f.read(4))[0])
    return replyList



if __name__=="__main__":
    createfile("data.bin")