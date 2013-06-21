__author__ = 'Dixith Kurra'
__author__ = 'ProfAVR'
from bottle import post,route,request,run
import sys
import datetime
from cache.cachefile import *

sys.path.append('E:\project13_branch\project13_forums\\api\classes')
from api.classes.user import User1
from backend.projectutils import *
from classes.UserAuth import UserAuth
from classes.ViewForum import *
from classes.ViewSubForum import *
from classes.CreateSubForum import *
from classes.postcomment import *
from classes.postQuestion import *
from classes.viewQuestion import *
from classes.JSON_Socket import*
serialized_list = [None] * 6
@route('/')
def load():
   load_database()
   return "loaded successfully"


@route('/signup',method="POST")
def signup():

    serialized_list[1] = request.POST['username']
    print serialized_list[1]
    serialized_list[2] = request.POST['password']
    serialized_list[3] = request.POST['DOB']
    serialized_list[4] = request.POST['email']
    serialized_list[5] = datetime.date.today()
    # user_obj=User()
    # user_obj.name=serialized['username']
    # user_obj.password=serialized['password']
    # user_obj.birth_date=serialized['DOB']
    # user_obj.mail=serialized['email']
    print serialized_list
    U = User1(str(serialized_list[1]), serialized_list[2], serialized_list[3], serialized_list[4], serialized_list[5])

    validation = U.validate()
    print validation
    if not isinstance(validation, str):
    #if project13_forums.model.memory.sign_up(U):
        if sign_up(U):
            return "sucessful registration"
        else:
            return "username already exists"
    else:
        return "Invalid credentials"
@route('/login',method='POST')
def log():
    serialized_list[1] = request.POST['username']
    serialized_list[2] = request.POST['password']

    UA = UserAuth(serialized_list[1], serialized_list[2])

    if sign_in(UA):
        return "Login Successful"
    else:
        return "username password mismatch"



@route('/opensubforum',method='POST')
def open():
    serialized_list[1]=request.POST['forumname']
    serialized_list[2]=request.POST['name']
    serialized_list[3]=request.POST['createdby']
    print serialized_list,serialized_list,"131\n"
                #CSF=CreateSubForum(serialized_list[1],serialized_list[2],serialized_list[3])
    CSF = SubForum(serialized_list[2],serialized_list[3],serialized_list[1])
    print CSF
    lock1.release()
    if create_sub_forum(CSF):
        return "subforum created"
        #c.send(CSF.deserializer(serialized_list[2]+"subforum is created"))
    else:
        #c.send(CSF.deserializer("subforum name already exists"))
        return "subforum name already exists"


run(host='localhost',port=8234,debug=True)



