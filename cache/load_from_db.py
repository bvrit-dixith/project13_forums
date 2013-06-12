__author__ = 'Chaitanya'

__author__ = 'Chaitanya'

#import inspect
#import os
#from memory import *

import struct
from io.projectutils import *


class user_metadata_class:
    def __init__(self):
        self.username=None
        self.password=None
        self.email=None
        self.DOB=None
        self.join_date=None
        pass

user_metadata=[]


def load_user_metadata():
    fp=open('C:\Users\Chaitanya\PycharmProjects\project13_branch\project13_forums\io\data.bin','rb')
    fp.seek(1526)
    user_count=struct.unpack('I',fp.read(4))[0]
    user_metadata=[]
    c=1
    while c<=user_count:
        obj=User()
        obj.id=struct.unpack('I',fp.read(4))[0]
        obj.name=fp.read(20).strip('\x00')
        obj.password=fp.read(10).strip('\x00')
        obj.mail=fp.read(30).strip('\x00')
        obj.birth_date=fp.read(10).strip('\x00')
        obj.join_date=fp.read(10).strip('\x00')
        fp.read(122-84)
        user_metadata.append(obj)
        c+=1
    fp.close()



    #mod_file = inspect.getfile(inspect.currentframe())
    #mod_dir = os.path.dirname(mod_file)
    #test_file = os.path.join(mod_dir, file)
    #return open(test_file, mode)
    '''fp=open('C:\Users\Chaitanya\PycharmProjects\project13_branch\project13_forums\io\data.bin','rb')
    fp.seek(1526)
    user_count=struct.unpack('I',fp.read(4))[0]
    fp.seek(1530)
    list1=[]
    c=1
    while c<=user_count:
        list1.append(fp.read(104))
        c+=1
    fp.close()
    for string in list1:
        i=0
        count=0
        obj=user_metadata_class()
        while i<len(string):
          temp=''
          count+=1
          while string[i]!='}':
             temp+=string[i]
             i+=1
          i+=1
          if count==1:
              obj.username=temp
          elif count==2:
              obj.password=temp
          elif count==3:
              obj.email=temp
          elif count==4:
              obj.DOB=temp
          elif count==5:
              obj.join_date=temp
              break
        user_metadata.append(obj)
    print user_metadata
    print user_metadata[3].username'''

def load_forum_metadata():
    fp=open('C:\Users\Chaitanya\PycharmProjects\project13_branch\project13_forums\io\data.bin','rb')
    fp.seek(1026)
    forum_count=struct.unpack('I',fp.read(4))[0]
    forum_metadata=[]
    c=1
    while c<=forum_count:
        obj=Forum()
        obj.id=struct.unpack('I',fp.read(4))[0]
        obj.name=fp.read(30).strip('\x00')
        obj.nextForum=struct.unpack('I',fp.read(4))[0]
        obj.prevForum=struct.unpack('I',fp.read(4))[0]
        obj.firstsubForum=struct.unpack('I',fp.read(4))[0]
        fp.read(70-42)
        forum_metadata.append(obj)
        c+=1
    fp.close()


def load_sub_forum_metadata():
    fp=open('C:\Users\Chaitanya\PycharmProjects\project13_branch\project13_forums\io\data.bin','rb')
    fp.seek(43526)
    sub_forum_count=struct.unpack('I',fp.read(4))[0]
    sub_forum_metadata=[]
    c=1
    while c<=sub_forum_count:
        obj=SubForum()
        obj.id=struct.unpack('I',fp.read(4))[0]
        obj.name=fp.read(30).strip('\x00')
        obj.forumname=fp.read(30).strip('\x00')
        obj.createdby=fp.read(20).strip('\x00')
        obj.nextSubForum=struct.unpack('I',fp.read(4))[0]
        obj.prevSubForum=struct.unpack('I',fp.read(4))[0]
        obj.firstQuestion=struct.unpack('I',fp.read(4))[0]
        obj.num_of_questions=struct.unpack('I',fp.read(4))[0]
        fp.read(122-100)
        sub_forum_metadata.append(obj)
        c+=1
    fp.close()





if __name__=="__main__":
    load_user_metadata()
