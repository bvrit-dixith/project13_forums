__author__ = 'ProfAVR'

import socket
import json
from api.classes.user import *
from cache.cache import *
from api.classes.UserAuth import *
from api.classes.ViewForum import *
from api.classes.ViewSubForum import *
from api.classes.CreateSubForum import *
from api.classes.postcomment import *
from api.classes.postQuestion import *



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


def server():
    serv = server_socket()
    host = socket.gethostname()
    port = 8999
    serv.bind((host, port))
    serv.listen(5)
    c, addr = serv.accept()
    while True:
        msg = c.recv(1024)
        server_json = json.json()
        serialized = "".join(server_json.serializer(msg).values())
        serialized = serialized.split()
        if serialized[0] == "signup":
            U = User(serialized[1], serialized[2], serialized[3], serialized[4])
            validation = U.validate()
            if not validation.isstring():
            #if project13_forums.model.memory.sign_up(U):
                if sign_up(U):
                    c.send(U.deserializer("Succesful"))
                else:
                    c.send(U.deserializer("Username already exists"))
            else:
                c.send(U.deserializer("Invalid Credentials " + validation))
            pass
        elif serialized[0] == "login":
            UA = UserAuth(serialized[1], serialized[2])
            validation = UA.validate()
            if not validation.isstring():
                if checkUsername(serialized[1]):
                    pw = getPassword(serialized[1])
                if pw == serialized[1]:
                    c.send(UA.deserializer('True'))
                else:
                    c.send(UA.deserializer("username password mismatch"))
            else:
                c.send(UA.deserializer("Invalid Credentials " + validation))
                pass
        elif serialized[0] == "view_forum":
            VF = ViewForum(serialized[1])
            forum_list=view_forum(VF.forum_name)
            forum_json=convert_list(forum_list)
            c.send(VF.deserializer(forum_json))
            pass
        elif serialized[0] == 'view_sub_forum':
            VSF=ViewSubForum(serialized[1],serialized[2])


        elif serialized[0] == "create_sub_forum":
            CSF=CreateSubForum(serialized[1],serialized[2],serialized[3])
            if create_sub_forum(CSF):
                c.send(CSF.deserializer(serialized[2]+"subforum is created"))
            else:
                c.send(CSF.deserializer("subforum name already exists"))
        elif serialized[0] == "view_sub_forum":
            VSF = ViewSubForum(serialized[1],serialized[2],serialized[3])
            sub_forum_question_list=view_sub_forum(VSF)

        elif serialized[0] == "post_question":
            PQ = PostQuestion(serialized[1],serialized[2],serialized[3],serialized[4:])
            if create_sub_forum(PQ):
                c.send(PQ.deserializer("successfully posted"))
        elif serialized[0] == "post_answer":
            PC=PostComment(serialized[1],serialized[2],serialized[3])
            if post_comment(PC):
                c.send(PC.deserializer("successfully posted")






            pass

    serv.close()

    pass


if __name__ == "__main__":
    server()