__author__ = 'ProfAVR'

import socket
import sys
import datetime
from cache.cachefile import *
import threading

sys.path.append('E:\project13_branch\project13_forums\\api\classes')
from api.classes.user import User1
from backend.projectutils import *
from classes.UserAuth import UserAuth
from classes.JSON_Socket import *


lock1=threading.Lock()
lock2=threading.Lock()
lock3=threading.Lock()
class server_socket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        else:
            self.sock = sock

    def bind(self, (host, port)):
        self.sock.bind((host, port))

    def listen(self, num):
        self.sock.listen(num)

    def accept(self):
        return self.sock.accept()

    def send(self, msg):
        self.sock.send(msg)

    def close(self):
        self.sock.close()


def server():
    serialized={}
    serv = server_socket()
    #host = socket.gethostname()
    host="10.3.8.141"
    port = 8999
    serv.bind((host, port))

    while True:
        serv.listen(5)
        c, addr = serv.accept()
        print "clientObj",c
        t=threading.Thread(None,target=newClient,args=(c,)).start()
        pass
    return "done"

def newClient(c):
    while True:
        msg = c.recv(1024)
        print "starting",msg,"received msg"
        serialized = convert_from_json_object(msg)
        print serialized,"hello vaisham"
        serialized_list = [None]*6
        serialized_list[0]=serialized['action']
        print serialized_list[0]
        print serialized_list
        if serialized_list[0] == "exit":
            print "enter here"
            c.close()
            break
        if serialized_list[0] == "signup":
            serialized_list[1]=serialized['name']
            serialized_list[2]=serialized['password']
            serialized_list[3]=serialized['DOB']
            serialized_list[4]=serialized['email']
            serialized_list[5]=datetime.date.today()
                # user_obj=User()
                # user_obj.name=serialized['username']
                # user_obj.password=serialized['password']
                # user_obj.birth_date=serialized['DOB']
                # user_obj.mail=serialized['email']
            print serialized_list
            U = User1(serialized_list[1], serialized_list[2], serialized_list[3], serialized_list[4],serialized_list[5])

            validation = U.validate()
            if not isinstance(validation,str):
                #if project13_forums.model.memory.sign_up(U):
                if sign_up(U):
                        c.send(U.deserializer("Successful"))
                else:
                    c.send(U.deserializer("Username already exists"))
            else:
                c.send(U.deserializer("Invalid Credentials xyz" + validation))
            pass
        elif serialized_list[0] == "login":
            serialized_list[1]=serialized['name']
            serialized_list[2]=serialized['password']
            print serialized_list
            UA = UserAuth(serialized_list[1], serialized_list[2])
                #validation = UA.validate()
                #print type(validation)
                #if not isinstance(validation,str):
                 #   print "rache"
            if sign_in(UA):
                print UA.deserializer("login successful"), "Line 103 Server"
                c.send(UA.deserializer("login successful"))
            else:
                print UA.deserializer("login successful"), "Line 103 Server"
                c.send(UA.deserializer("username password mismatch"))
                #else:
                #    c.send(UA.deserializer("Invalid Credentials " + validation))
                 #   pass
        elif serialized_list[0] == "view_forum":
            serialized_list[1]=serialized['forumname']
            VF = Forum(name=serialized_list[1],id=-1)
            forum_list=view_forum_in_memory(VF)
            forum_json=convert_list(forum_list)
            c.send(forum_json)
            pass
        elif serialized_list[0] == "open_sub_forum":
            serialized_list[1]=serialized['forumname']
            serialized_list[2]=serialized['sub_forum']
                #serialized_list[3]=serialized['action']
            print serialized_list,serialized,"121\n"
            VSF = SubForum(name=serialized_list[2],forumname=serialized_list[1])
            sub_forum_question_list=view_que_in_subforum(VSF)
            question_json=convert_list(sub_forum_question_list)
            print "question-json",question_json
            c.send(question_json)

        elif serialized_list[0] == "new_sub_forum":
            print "entered"
            lock1.acquire()
            print "lock acquired"
            serialized_list[1]=serialized['forumname']
            serialized_list[2]=serialized['name']
            serialized_list[3]=serialized['createdby']
            print serialized_list,serialized,"131"
                #CSF=CreateSubForum(serialized_list[1],serialized_list[2],serialized_list[3])
            CSF = SubForum(serialized_list[2],serialized_list[3],serialized_list[1])
            print CSF
            lock1.release()
            if create_sub_forum(CSF):
                c.send(CSF.deserializer(serialized_list[2]+"subforum is created"))
            else:
                c.send(CSF.deserializer("subforum name already exists"))


        elif serialized_list[0] == "post_question":
            lock2.acquire()
            serialized_list[1]=serialized['forumname']
            serialized_list[2]=serialized['name']
            serialized_list[3]=serialized['createdby']
            serialized_list[4:]=serialized['new_question']
            PQ = Message(serialized_list[1],serialized_list[2],serialized_list[3],serialized_list[4:])
            if post_msg_in_sub_forum(PQ):
                c.send(PQ.deserializer("successfully posted"))
            lock2.acquire()
            #elif serialized[0] == "post_answer":
             #   PC=PostComment(serialized[1],serialized[2],serialized[3])
              #  if post_comment(PC):
               #     c.send(PC.deserializer("successfully posted"))
        elif serialized_list[0] == "view_question":
            VQ=Message(serialized[1],serialized[2],serialized[3])
            reply_list=view_replies_for_que_in_sub_forum(VQ)
            c.send(VQ.deserializer(reply_list))
            pass
    c.close()

if __name__ == "__main__":
    load_database()
    server()
