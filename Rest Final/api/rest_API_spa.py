

from bottle import route, run, request, get, post, response

import socket
import sys
import datetime
#import backend.projectutils
import threading
import string

from cache.cachefile import *
sys.path.append('E:\project13_branch\project13_forums\\api\classes')
from api.classes.user import *
from classes.UserAuth import UserAuth
from classes.ViewForum import *
from classes.ViewSubForum import *
from classes.CreateSubForum import *
from classes.postcomment import *
from classes.postQuestion import *
from classes.viewQuestion import *
from classes.JSON_Socket import *

serialized_list = [None] * 5

@route('/')
def load():
    load_database()
    return "loded successfully"


@route('/exit')
def exit():


    print "enter here"
    exit(0)



@route('/signup', method="POST")
def signup():
    serialized_list[0] = request.POST['username']
    serialized_list[1] = request.POST['password']
    serialized_list[2] = request.POST['DOB']
    date_tuple=serialize_date(serialized_list[2])
    serialized_list[2]=list(date_tuple)
    serialized_list[3] = request.POST['email']
    serialized_list[4] = datetime.date.today()

    U = User1(serialized_list[0], serialized_list[1], serialized_list[2], serialized_list[3], serialized_list[4])

    validation = U.validate()
    if not isinstance(validation, str):

        if sign_up(U):
            return "Successful"
        else:
            return "Username already exists"
    else:
        return "Invalid Credentials xyz" + validation
    pass



@route('/login', method="POST")
def login():

    serialized_list[0] = request.POST['username']
    serialized_list[1] = request.POST['password']
    print serialized_list
    UA = UserAuth(serialized_list[0], serialized_list[1])

    if sign_in(UA):

        return "login successful"
    else:

        return "username password mismatch"


@route('/view_forums',method='GET')
def display():
    return "The forums listed are :\n\t1. EDUCATION \n\t2. SPORTS\n\t3. ENTERTAINMENT\n\t4. TECHNOLOGY\n\t5. NEWS\n\t6. HEALTH\n\t7. MISCELLANEOUS"
    pass

@route('/view_forum/<forum_name>', method="GET")
def view_forum(forum_name):
    serialized_list[0]=forum_name
    VF = Forum(name=serialized_list[0])
    forum_list = view_forum_in_memory(VF)
    print forum_list,'list'
    str = "SubForum Created by"
    for i in forum_list:
        for j in range(len(i)):
            if j == 1 or j == 2:
                str += i[j]+'\t'
                continue
            str+="\n"
    print str
    return str




@route('/open_sub_forum/<forum_name>/<sub_forum>', method="GET")
def open_sub_forum(forum_name,sub_forum):
    serialized_list[0] = forum_name
    serialized_list[1] = sub_forum
    VSF = SubForum(name=serialized_list[1],forumname= serialized_list[0])
    sub_forum_question_list = view_que_in_subforum(VSF)
    string ="id\t\tquestion\t\t\t\t\tposted by\n"
    for i in sub_forum_question_list:
        for j in range(len(i)):
            string += str(i[j])+'\t\t'
            continue
        string+="\n"
    print string
    return string



@route('/new_sub_forum', method="POST")
def new_sub_forum():
    serialized_list[0] = request.POST['forum_name']
    serialized_list[1] = request.POST['new_forum_name']
    serialized_list[2] = request.POST['created_by']
    CSF = SubForum(serialized_list[1], serialized_list[2], serialized_list[0])
    if create_sub_forum(CSF):
        return serialized_list[1] + " subforum is created"
    else:
        return "subforum name already exists"


@route('/post_question', method="POST")
def post_question():

    serialized_list[0] = request.POST['forum_name']
    serialized_list[1] = request.POST['sub_forum']
    serialized_list[2] = request.POST['created_by']
    serialized_list[3]= request.POST['new_question']
    serialized_list[4]=len(serialized_list[3])
    PQ = Message(forumname=serialized_list[0],subForumname=serialized_list[1],postedby=serialized_list[2],length=serialized_list[4],msg=serialized_list[3])
    if post_msg_in_sub_forum(PQ):
        return "successfully posted"

@route('/post_answer', method="POST")
def post_answer():
#elif serialized_list[0] == "post_answer":
    serialized_list[0] = request.POST['forum_name']
    serialized_list[1] = request.POST['sub_forum']
    serialized_list[2] = request.POST['created_by']
    serialized_list[3] = request.POST['reply_new']
    serialized_list[4] = request.POST['question_id']
    PC = Reply(forumname=serialized_list[0],subForumname= serialized_list[1],message_id=int(serialized_list[4]),postedby= serialized_list[2],msgLength= len(serialized_list[3]),msg=serialized_list[3])
    if post_rply_in_sub_forum(PC):
        return "successfully posted"

@route('/select_question/<forum_name>/<sub_forum>/<question_id>', method="GET")
def select_question(forum_name,sub_forum,question_id):
    string=''
    serialized_list[0] = forum_name
    serialized_list[1] = sub_forum
    serialized_list[2] = question_id
    VQ = Message(forumname=serialized_list[0],subForumname= serialized_list[1],id= serialized_list[2])
    reply_list = view_replies_for_que_in_sub_forum(VQ)
    if  reply_list==[]:
        return "selected question has No replies"
    else:
        for i in reply_list:

                string += i[1]+'\n'
        print string
        return string



run(host='localhost', port=8180, debug=True, reloader=True)


