__author__ = 'ProfAVR'

import socket
import json
import sys

sys.path.append('E:\project13_branch\project13_forums\api\classes')
from classes.user import User,serialize_date
from cache.cache import *
from classes.UserAuth import UserAuth
from classes.ViewForum import *
from classes.ViewSubForum import *
from classes.CreateSubForum import *
from classes.postcomment import *
from classes.postQuestion import *
from classes.viewQuestion import *
from classes.JSON_Socket import *



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
    c, addr = serv.accept()
    while True:
        msg = c.recv(1024)

        #server_json = json()
        serialized = convert_from_json_object(msg)
        serialized_list = [None]*5
        serialized_list[0]=serialized['action']

        if serialized_list[0] == "signup":
            serialized_list[1]=serialized['username']
            serialized_list[2]=serialized['password']
            serialized_list[3]=serialized['DOB']
            serialized_list[4]=serialized['email']
            U = User(serialized_list[1], serialized_list[2], serialized_list[3], serialized_list[4])
            validation = U.validate()
            if not isinstance(validation,str):
            #if project13_forums.model.memory.sign_up(U):
                if sign_up(U):
                    c.send(U.deserializer("Succesful"))
                else:
                    c.send(U.deserializer("Username already exists"))
            else:
                c.send(U.deserializer("Invalid Credentials " + validation))
            pass
        elif serialized_list[0] == "login":
            serialized_list[1]=serialized['username']
            serialized_list[2]=serialized['password']
            UA = UserAuth(serialized_list[1], serialized_list[2])
            validation = UA.validate()
            if not validation.isstring():
                if sign_in(UA):
                    c.send(UA.deserializer("login successful"))
                else:
                    c.send(UA.deserializer("username password mismatch"))
            else:
                c.send(UA.deserializer("Invalid Credentials " + validation))
                pass
        elif serialized_list[0] == "view_forum":
            serialized_list[1]=serialized['forum_name']
            VF = ViewForum(serialized_list[1])
            forum_list=view_forum(VF.forum_name)
            forum_json=convert_list(forum_list)
            c.send(VF.deserializer(forum_json))
            pass
        elif serialized_list[0] == "new_sub_forum":
            serialized_list[1]=serialized['forum_name']
            serialized_list[2]=serialized['new_sub_forum']
            serialized_list[3]=serialized['created_by']
            CSF=CreateSubForum(serialized_list[1],serialized_list[2],serialized_list[3])
            if create_sub_forum(CSF):
                c.send(CSF.deserializer(serialized_list[2]+"subforum is created"))
            else:
                c.send(CSF.deserializer("subforum name already exists"))
        elif serialized[0] == "open_sub_forum":
            serialized_list[1]=serialized['forum_name']
            serialized_list[2]=serialized['new_sub_forum']
            VSF = ViewSubForum(serialized_list[1],serialized_list[2])
            sub_forum_question_list=view_sub_forum(VSF)
            question_json=convert_list(sub_forum_question_list)
            c.send(question_json)



        elif serialized_list[0] == "post_question":
            serialized_list[1]=serialized['forum_name']
            serialized_list[2]=serialized['sub_forum']
            serialized_list[3]=serialized['created_by']
            serialized_list[4:]=serialized['new_question']
            PQ = PostQuestion(serialized_list[1],serialized_list[2],serialized_list[3],serialized_list[4:])
            if post_question_in_sub_forum(PQ):
                c.send(PQ.deserializer("successfully posted"))
        elif serialized[0] == "post_answer":
            serialized_list[1]=serialized['forum_name']
            serialized_list[2]=serialized['sub_forum']
            serialized_list[3]=serialized['created_by']
            serialized_list[4]=serialized['question_new']
            PC=PostComment(serialized_list[1],serialized_list[2],serialized_list[3])
            if post_comment(PC):
                c.send(PC.deserializer("successfully posted"))
        elif serialized_list[0] == "view_question":
            serialized_list[1]=serialized['forum_name']
            serialized_list[2]=serialized['sub_forum']
            serialized_list[3:]=serialized['question']
            VQ=viewQuestion(serialized_list[1],serialized_list[2],serialized_list[3])
            reply_list=view_ques_in_sub_forum(VQ)
            c.send(VQ.deserializer(reply_list))
            pass
        elif serialized_list[0] == 'exit':
            c.close()
        serv.close()

if __name__ == "__main__":
    server()__author__ = 'pranee'
