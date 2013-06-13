__author__ = 'Chaitanya'

__author__ = 'Chaitanya'

#import inspect
#import os
#from memory import *
import struct
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

    #mod_file = inspect.getfile(inspect.currentframe())
    #mod_dir = os.path.dirname(mod_file)
    #test_file = os.path.join(mod_dir, file)
    #return open(test_file, mode)
    fp=open('C:\Users\Chaitanya\PycharmProjects\cl2013\project13_forums\project13_forums\store\data.bin','rb')
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
    print user_metadata[3].username

    ''' fp=open('C:\Users\Chaitanya\PycharmProjects\cl2013\project13_forums\project13_forums\store\data.bin','rb')
    fp.seek(43526)
    list1=[]
    while fp!=None:
        list1.append(fp.read(122))
    fp.close()
    for string in list1:
        i=0
        count=0
        obj=forum_metadata()
        while i<len(string):
          temp=''
          count+=1
          while string[i]!='}':
             temp+=string[i]
          i+=1
          if count==1:
              obj.forum_name=temp
          elif count==2:
              obj.password=temp
          elif count==3:
              obj.email=temp
          elif count==4:
              obj.DOB=temp
        user_metadata.append(obj)

'''

if __name__=="__main__":
    load_user_metadata()
