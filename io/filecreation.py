__author__ = 'amani'

import os
import inspect
import re
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
    f.write(struct.pack('I',0))
    f.seek(1026)
    f.write(struct.pack('I',0))
    f.seek(43526)
    f.write(struct.pack('I',0))
    f.seek(86226)
    f.write(struct.pack('I',0))
    f.seek(2500000)
    f.write(struct.pack('I',0))
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
    f.close()

#writes message metadata into a file
def writeMessagedata(filename,msgdata):
    file=getFilePath(filename)
    with open(file,"rb+") as f:
        f.seek(43526)
        message_count=struct.unpack('I',f.read(4))[0]
        subforum_id=43530+122*message_count
        f.seek(subforum_id)
        f.write(struct.pack('i',msgdata.id))
        f.write(struct.pack('30s',msgdata.forumname))
        f.write(struct.pack('30s',msgdata.subForumname))
        f.write(struct.pack('20s',msgdata.postedby))
        f.write(struct.pack('i',msgdata.nextQuestion))
        f.write(struct.pack('i',msgdata.prevQuestion))
        f.write(struct.pack('i',msgdata.firstReply))
        f.write(struct.pack('i',msgdata.messagedata))
        message_count+=1
        f.seek(43526)
        f.write(struct.pack('I',message_count))
    f.close()

def writeReplyData(filename,replydata):
    file=getFilePath(filename)
    with open(file,"rb+") as f:
        f.seek(2500000)
        reply_count=struct.unpack('I',f.read(4))[0]
        subforum_id=25000004+122*reply_count
        f.seek(subforum_id)
        f.write(struct.pack('i',replydata.id))
        f.write(struct.pack('30s',replydata.forumname))
        f.write(struct.pack('30s',replydata.subForumname))
        f.write(struct.pack('20s',replydata.postedby))
        f.write(struct.pack('i',replydata.nextReply))
        f.write(struct.pack('i',replydata.prevReply))
        f.write(struct.pack('i',replydata.replydata))
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


if __name__=="__main__":
    createfile("data.bin")