__author__ = 'ProfAVR'

import socket
import sys
import datetime
from cache.cachefile import *
import threading

sys.path.append('E:\project13\project13_forums\\api\classes')
from api.classes.user import User1
from backend.projectutils import *
from classes.UserAuth import UserAuth
# from classes.ViewForum import *
# from classes.ViewSubForum import *
# from classes.CreateSubForum import *
# from classes.postcomment import *
# from classes.postQuestion import *
# from classes.viewQuestion import *
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
    host = socket.gethostname()
    port = 8999
    serv.bind((host, port))
    serv.listen(5)
    while True:
        serv.listen(5)
        c, addr = serv.accept()
        print "clientObj",c
        t=threading.Thread(None,target=newClient,args=(c,)).start()
        pass
    return "done"

def newClient(c):
        while True:
            msglen = int(c.recv(1024))
            print msglen
            msg=c.recv(msglen)
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
                VF = Forum(name=serialized_list[1])
                forum_list=view_forum_in_memory(VF)
                forum_json=convert_list(forum_list)
                c.send(forum_json)
                pass
            elif serialized_list[0] == "open_sub_forum":
                print "entering openining of a subforum"
                serialized_list[1]=serialized['forumname']
                serialized_list[2]=serialized['name']
                serialized_list[3]=serialized['id']
                print serialized_list,serialized,"121\n"
                VSF = SubForum(name=serialized_list[2],forumname=serialized_list[1])
                sub_forum_question_list=view_que_in_subforum(VSF)
                print sub_forum_question_list,"125"
                question_json=convert_list(sub_forum_question_list)
                print "128"
                c.send(question_json)

            elif serialized_list[0] == "new_sub_forum":
                lock1.acquire()
                serialized_list[1]=serialized['forumname']
                serialized_list[2]=serialized['name']
                serialized_list[3]=serialized['createdby']
                print serialized_list,serialized,"131\n"
                #CSF=CreateSubForum(serialized_list[1],serialized_list[2],serialized_list[3])
                CSF = SubForum(serialized_list[2],serialized_list[3],serialized_list[1])
                print CSF
                lock1.release()
                if create_sub_forum(CSF):
                    c.send(CSF.deserializer(serialized_list[2]+"subforum is created"))
                else:
                    c.send(CSF.deserializer("subforum name already exists"))


            elif serialized_list[0] == "post_question":
                print "entering posting a question"
                #lock2.acquire()
                serialized_list[1]=serialized['forumname']
                serialized_list[2]=serialized['sub_forum']
                serialized_list[3]=serialized['createdby']
                serialized_list[4]=serialized['new_question']
                serialized_list[5]=len(serialized['new_question'])
                print serialized,serialized_list,"hello",serialized_list[4]
                print "149"
                PQ = Message(forumname=serialized_list[1],subForumname=serialized_list[2],postedby=serialized_list[3],length=serialized_list[5],msg=serialized_list[4])
                print "151"
                print PQ,"message"
                #lock2.release()
                print post_msg_in_sub_forum(PQ),"posted or not"
                if post_msg_in_sub_forum(PQ):
                    print "153"
                    c.send(PQ.deserializer("successfully posted"))
                else:
                    c.send(PQ.deserializer("unsuccessful"))
            elif serialized_list[0] == "post_answer":
                lock3.acquire()
                serialized_list[1]=serialized['sub_forum']
                serialized_list[2]=serialized['createdby']
                serialized_list[3]=serialized['new_reply']
                serialized_list[4]=serialized['forumname']
                print "posting answer"
                # forumname="",subForumname="",message_id="",postedby="",msgLength="",msg=""
                PC=Reply(forumname=serialized_list[4],subForumname=serialized_list[1],message_id="",postedby=serialized_list[2],msgLength=len(serialized_list[3]),msg=serialized_list[3])
                print "created a reply object"
                lock3.release()
                if post_rply_in_sub_forum(PC):
                    print "after cache's file"
                    c.send(PC.deserializer("successfully posted"))
                else:
                    c.send(PC.deserializer("unsuccesfull in posting a reply"))
            elif serialized_list[0] == "view_question":
                # d['action'] = "view_question"
                # d['forumname'] = forum_name
                # d['sub_forum'] = sub_forum
                # d['question_id'] = id_q[int(option) - 1]
                serialized_list[1]=serialized['forumname']
                serialized_list[2]=serialized['sub_forum']
                serialized_list[3]=serialized['question_id']
                # forumname="",subForumname="",message_id="",postedby="",msgLength="",msg=""
                VQ=Message(forumname=serialized_list[1],subForumname=serialized_list[2],id=serialized_list[3])
                reply_list=view_replies_for_que_in_sub_forum(VQ)
                c.send(VQ.deserializer(reply_list))
                pass
        c.close()

if __name__ == "__main__":
    load_database()
    server()
