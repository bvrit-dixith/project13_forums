__author__ = 'Dixith Kurra'



import io.projectutils

list1=[]  #category1
list2=[]  #2
list3=[]  #3
list4=[]  #4
list5=[]  #5
list6=[]  #6
list7=[]  #7

user_metadata=[]

forum_metadata=[]

sub_forum_metadata=[list1,list2,list3,list4,list5,list6,list7]

messages_metadata=[]

def sign_up(user_obj):
        user_flag=1
        for i in  user_metadata:
           if user_obj.username!=i.username:
               pass
           else:
               return False
        if user_flag==1:
            return insert(user_obj)

def insert(user_obj):
    user_metadata.append(user_obj)
    return True


def sign_in(user_sign_in_obj):
    print user_metadata
    for  i in user_metadata:
        if i.username==user_sign_in_obj.username and i.password==user_sign_in_obj.password:
            return True #print 'authorized user'
    return False # print 'invalid user'


def create_sub_forum(sub_forum_obj):
    forum_name=sub_forum_obj.forum_name
    i=get_number(forum_name)
    sub_forum_name = sub_forum_obj.sub_forum_name
    #temp_list=[sub_forum_obj.sub_forum_name,sub_forum_obj.forum_name,sub_forum_obj.createdby,sub_forum_obj.number_of_views,sub_forum_obj.no_of_questions,sub_forum_obj.pointer_to_next_sub_forum,sub_forum_obj.pointer_to_prev_sub_forum,sub_forum_obj.pointer_to_first_msg,sub_forum_obj.last_modified_time,sub_forum_obj.date_of_creation,sub_forum_obj.time_of_creation,sub_forum_obj.last_accessed_time,sub_forum_obj.last_back_up_time]

    for k in sub_forum_metadata[i]:
        if k.sub_forum_name==sub_forum_name:
            return False
    sub_forum_metadata[i].append(sub_forum_obj)
    return True
    #sub_forum_value_cache.append(list_obj)
    pass

def get_number(forum_name):
    if forum_name == "Education":
        return 1
    elif forum_name == "Health":
        return 2
    elif forum_name == "Entertainment":
        return 3
    elif forum_name == "Technology":
        return 4
    elif forum_name == "News":
        return 5
    elif forum_name == "Health":
        return 6
    elif forum_name == "Miscellaneous":
        return 7


def view_forum_in_memory(forum_obj):
    forum_name=forum_obj.forum_name
    i=get_number(forum_name)
    '''view_sub_forum_list=[]
    for i in sub_forum_metadata:
        if i.forum_name==forum_name:
           view_sub_forum_list.append(i.sub_forum_name)
    return view_sub_forum_list '''
    view_sub_forum_list=[["cse","chaitanya"]]
    for k in sub_forum_metadata[i]:
        temp=[]
        temp.append(k.forumname)
        temp.append(k.createdby)
        view_sub_forum_list.append(temp)
    return view_sub_forum_list

def delete_sub_forum(i,sub_forum_name):
    '''del_flag=0
    for i in sub_forum_metadata:
        if i.sub_forum_name==sub_forum_name:
           del_flag=1
           del i
    if del_flag==0:
        return False
    return True
    pass   '''
    pass
    for k in sub_forum_metadata[i]:
        if k.forum_name==sub_forum_name:
            del k
            return True
    return False


def view_sub_forum():
    #call io(obj)
    pass

def view_ques_in_sub_forum(forum_name,sub_forum_name):
    #call io(obj)

    pass



def post_question_in_sub_forum(forum_name,sub_forum_name,created_by,msg):
    pass






#if __name__=="__main__":
#      return sign_up(sign_up_object)
#      return log_in(login_object)


