__author__ = 'amani'

import os
import inspect
import re
import datetime
import struct
from projectutils import *
import string

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
    print num_of_forums
    i=0
    while i<num_of_forums-1:
        forum_object_list[i].nextForum=forum_object_list[i+1].id
        i+=1
    while i>0:
        forum_object_list[i].prevForum=forum_object_list[i-1].id
        i-=1
    for forum_object in forum_object_list:
        writeForumData("data.bin",forum_object)
    print "successfully forums created"

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
    print "forum closed"
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
        f.write(struct.pack('10s',userdata.birth_date))
        f.write(struct.pack('10s',userdata.join_date))
        f.write(struct.pack('i',userdata.num_of_posted_messages))
        user_count+=1
        f.seek(1526)
        f.write(struct.pack('I',user_count))
    f.close()

#writes subforum metadata into a file
def writeSubforumdata(filename,subforumData):
    file=getFilePath(filename)
    with open(file,"rb+") as f:
        f.seek(43526)
        subforum_count=struct.unpack('I',f.read(4))[0]
        subforum_id=43530+122*subforum_count
        f.seek(subforum_id)
        subforumData.id=subforum_id
        f.write(struct.pack('i',subforumData.id))
        f.write(struct.pack('30s',subforumData.name))
        f.write(struct.pack('30s',subforumData.forumname))
        f.write(struct.pack('20s',subforumData.createdby))
        f.write(struct.pack('i',subforumData.nextSubForum))
        f.write(struct.pack('i',subforumData.prevSubForum))
        f.write(struct.pack('i',subforumData.firstQuestion))
        f.write(struct.pack('i',subforumData.num_of_questions))
        subforum_count+=1
        f.seek(43526)
        f.write(struct.pack('I',subforum_count))
    #f.close()

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
        message_count+=1
        f.seek(86226)
        f.write(struct.pack('I',message_count))
    f.close()

def writeReplyData(filename,replydata):
    file=getFilePath(filename)
    with open(file,"rb+") as f:
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
        reply_count+=1
        f.seek(2500000)
        f.write(struct.pack('I',reply_count))
    f.close()

#gets file path
def getFilePath(filename):
    mod_file=inspect.getfile(inspect.currentframe())
    mod_dir=os.path.dirname(mod_file)
    file=os.path.join(mod_dir,filename)
    return file


def retrieve(filename):
    file=getFilePath(filename)
    f=open(file,"rb")
    f.seek(1530)
    data=f.read(20)
    print data

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


def getSubForumUpdated(present_forumname,present_subforum_name,present_message_id):
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
        f.seek((first_subForum_id+122*i)+4)
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
    f.seek(43626+122*i)
    count1=struct.unpack('I',f.read(4))[0]
    count1+=1
    f.seek(43626+122*i)
    f.write(struct.pack('I',count1))                  #writes message count in the subforum


def getFirstSubforumId(forumname):
    file=getFilePath("data.bin")
    f=open(file,"rb+")
    f.seek(1026)
    count=struct.unpack('I',f.read(4))
    i=0
    while i<count:
        f.seek(1034+70*i)
        name=f.read(30).strip('\x00')
        if name==forumname:
            break
        i+=1
    else:
        print "no such forum"
        return
    f.seek(1072+70*i)
    id=struct.unpack('I',f.read(4))[0]
    num=struct.unpack('I',f.read(4))[0]
    return id,num                           #returns first subforumid, no of subforums


def getFirstMessageId(link1,count,subForumname):
    file=getFilePath("data.bin")
    f=open(file,"rb+")
    i=0
    while i<count:
        f.seek(link1+122*i+4)
        temp=f.read(30).strip('\x00')
        pos=f.tell()
        if temp==subForumname:
            break
        i+=1
    else:
        print "no such subforum"
    f.seek(pos+58)  #seeks to the place where first message id is stored
    id=struct.unpack('I',f.read(4))[0]
    count=struct.unpack('I',f.read(4))[0]
    return id,count


def getRequiredMessageId(link2,count1,question_id,id):
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
    if struct.unpack('I',f.read(4))==-1:    #update first reply
        f.seek(-4,1)
        f.write(struct.pack('I',id))
    f.seek(pos+100)
    count=struct.unpack('I',f.read(4))[0]
    count+=1                                #update num of replies
    f.seek(pos+100)
    f.write(struct.pack('I',count))
    f.close()

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


if __name__=="__main__":
    createfile("data.bin")