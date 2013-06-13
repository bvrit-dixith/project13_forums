__author__ = 'Sumzy'

import JSON_Socket
import socket
from serialization import *

import datetime
import re


class mySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        else:
            self.sock = sock

    def connect(self, (host, port)):
        self.sock.connect((host, port))

    def send(self, msg):
        sent = self.sock.send(msg)
        if sent == 0:
            print "Runtime error"

    def receive(self):
        return self.sock.recv(1024)

    def close(self):
        self.sock.close()

uname = ""
dict_user = {}
authen_dict = {}
forum_details = {}

def signin():
    global dict_user
    while True:
        username = raw_input("Enter Username : ")
        if len(username) <= 20 and re.match("^[a-zA-Z]{1}[a-zA-Z0-9]*$", username):
            break
        else:
            print "Invalid Username: Username should be of less than 20 characters and should contains alphanumerics"
    while True:
        password = raw_input("Enter Password : ")
        if len(password) >= 6 and len(password) <= 10 and re.match(
                "^[a-zA-Z]{1}[a-zA-Z0-9]*$", password):
            break
        else:
            print "Invalid password: Password should be of 6-10 characters and alphanumeric"
    authen_dict['action'] = "login"
    authen_dict['username'] = username
    authen_dict['password'] = password
    return authen_dict
    pass


def serialize_date(input):
    check = '('
    year = ""
    month = ""
    date = ""
    for i in range(len(input)):
        if check == '(':
            if input[i] == ',':
                check = ','
                continue
            if i == 0:
                continue
            year += input[i]
            continue
        if check == ',':
            if input[i] == ',':
                check = ')'
                continue
            month += input[i]
            continue
        if check == ')':
            if input[i] == ')':
                break
            date += input[i]
            continue
    return [int(year), int(month), int(date)]


def signup():
    global dict_user
    while True:
        username = raw_input("Choose your Username : ")
        if len(username) <= 20 and re.match("^[a-zA-Z]{1}[a-zA-Z0-9]*$", username):
            break
        else:
            print "Invalid Username: Username should be of less than 20 characters and should contains alphanumerics"
    while True:
        password = raw_input("Create a Password : ")
        if len(password) >= 6 and len(password) <= 10 and re.match("^[a-zA-Z]{1}[a-zA-Z0-9]*$", password):
            break
        else:
            print "Invalid password: Password should be of 6-10 characters and alphanumeric"
    print("Enter DOB:")
    while True:
        year = raw_input("Enter Year:")
        month = raw_input("Enter Month:")
        date = raw_input("Enter Date:")
        DOB = int(year), int(month), int(date)
        year, month, date = serialize_date(str(DOB))
        if datetime.date.today() - datetime.date(year, month, date):
            break
        else:
            print "Invalid Date. Please Enter a Valid Date."
    while True:
        email = raw_input("Your current Email Address : ")
        if len(email) <= 30 and re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                                         email):
            break
        else:
            print "Invalid Email. Please Enter a Valid Email Address"
    dict_user['action'] = "signup"
    dict_user['username'] = username
    dict_user['password'] = password
    dict_user['DOB'] = DOB
    dict_user['email'] = email
    return dict_user

def exit_connection():
    dict_user={}
    dict_user['action']="exit"
    return dict_user

def print_sub_forums(dict):
    header = ("SubForums","Created By")
    dict_list=dict.items()
    dict_list.insert(0,header)
    col_width = max(len(word) for row in dict_list for word in row) + 2 # padding
    for row in dict_list:
        print "".join(word.ljust(col_width) for word in row)

def display():
    print "The forums listed are :"
    print "\t1. EDUCATION"
    print "\t2. SPORTS"
    print "\t3. ENTERTAINMENT"
    print "\t4. TECHNOLOGY"
    print "\t5. NEWS"
    print "\t6. HEALTH"
    print "\t7. MISCELLANEOUS"
    print "\n"

def split_client(dict):
    dict="#".join(dict.values())
    dict_keys=dict.keys()
    return dict.split('#'),dict_keys

def main():
    global dict_user
    global uname

    client = mySocket()
    host = socket.gethostname()
    port = 8999
    client.connect((host, port))
    while True:
        print "Welcome To TEAM 13 Forum :P"
        print "\t 1. Sign in"
        print "\t 2. Sign Up for Free"
        print "\t 3. View Forums"
        print "\t 4. Exit"

        choice = raw_input("Please Select an Option : ")

        if choice == '1':
            input = signin()
            uname = input['username']
            client_json = JSON_Socket.json()
            json_object = client_json.deserializer(input)
            client.send(json_object)
            received = client.receive()
            serialized = serialize_auth(received)
            if serialized == "True":
                print "Welcome, " + uname
                while True:
                    forum_name,f_name = display_user(uname)
                    client.send(forum_name)
                    display_forums_from_server = client.receive()
                    subforums_Json = JSON_Socket.json()
                    output = subforums_Json.serializer(display_forums_from_server)
                    output += output.split()
                    data_send,sub_forum = display_user_selected_forum(f_name,output,uname)
                    client.send(data_send)
                    questions = client.receive()
                    cli_json=JSON_Socket.json()
                    questions= cli_json.serializer(questions)
                    questions,id_q = split_client(questions)
                    while True:
                        result = display_questions(questions,uname,f_name,sub_forum,id_q)
                        if result == "break":
                            break
                        elif result == "exit":
                            exit(0)
                        client.send(result)
                        about_question = client.receive()
                        print_info = serialize_auth(about_question)
                        print_info.split()
                        while True:
                            for i in print_info:
                                print i
                            #replies_Json = JSON_Socket.json()
                            #replies = replies_Json.serializer(about_question)
                            result = display_replies(uname,f_name,sub_forum)
                            if result == "break":
                                break
                            elif result =="exit":
                                exit(0)
                            client.send(result)
                            about_reply = client.receive()
                            print_rep_info = serialize_auth(about_reply)
                            print_rep_info.split()
                            for i in print_rep_info:
                                print i
            else:
                print "Invalid Login Credentials. Please re-check them"

        elif choice == '2':
            input = signup()
            client_json = JSON_Socket.json()
            client.send(str(client_json.deserializer(input)))
            received = client.receive()
            print received

        elif choice == '3':
            display()


        elif choice == '4':
            input = exit_connection()
            client_json = JSON_Socket.json()
            client.send(str(client_json.deserializer(input)))
            client.close()
            break

        else:
            print "\nPlease Select a Valid Option"

    pass

def serialize_auth(input):
    return convert_from_json_object(input)

def view_forum(forum_name):
    global forum_details
    forum_details['action'] = "view_forum"
    forum_details['forum_name'] = forum_name

    forum_json = JSON_Socket.json()
    json_object = forum_json.deserializer(forum_details)

    return json_object,forum_name

    pass



def display_questions(questions,uname,forum_name,sub_forum,id_q):
    while True:
        print "1.View Questions"
        print "2.Post a Question"
        print "3.Back"
        print "4.LogOut"
        option = raw_input("Enter your Choice")
        if option == "1":
            for i in range(len(questions)):
                print str(i+1) + ":" + questions[i]
            option = raw_input("Enter the Question Number you wish to view: ")
            if option <len(questions) or option>len(questions):
                print "Enter a valid Question No."
            else:
                d = {}
                d['action'] = "select_question"
                d['forum_name'] = forum_name
                d['sub_forum'] = sub_forum
                d['question'] = id_q[option - 1]
                return str(d)
        elif option == "2":
            question_new = raw_input("Enter your Question : ")
            d = {}
            d['action'] = "post_question"
            d['forum_name'] = forum_name
            d['sub_forum'] = sub_forum
            d['created_by'] = uname
            d['new_question'] = question_new
            return str(d)
            pass
        elif option == "3":
            return "break"
            pass
        elif option == "4":
            return "exit"
            pass
        else:
            print "Please Select a Valid Option"

def display_replies(uname,forum_name,sub_forum):
    while True:
        print "\t1. Post a Reply"
        print "\t2. Back"
        print "\t3. LogOut"
        option = raw_input("Enter your Choice : ")
        if option == "1":
            reply_new = raw_input("Post your Reply here : ")
            d = {}
            d['action'] = "post_answer"
            d['forum_name'] = forum_name
            d['sub_forum'] = sub_forum
            d['new_reply'] = reply_new
            d['created_by'] = uname
            return str(d)
            pass
        elif option == "2":
            return "break"
        elif option == "3":
            return "exit"
            pass
        else:
            print "Please Select a Valid Option"

def display_user(user):
    display()
    while True:
        option = raw_input("Select the Forum you wish to View " + user + ":" )
        if option == '1':
            return view_forum("Education")
        elif option == '2':
            return view_forum("Health")
        elif option == '3':
            return view_forum("Entertainment")
        elif option == '4':
            return view_forum("Technology")
        elif option == '5':
            return view_forum("News")
        elif option == '6':
            return view_forum("Health")
        elif option == '7':
            return view_forum("Miscellaneous")
        else:
            print "\nPlease select a Valid option"

    pass


def display_user_selected_forum(forum_name,output,uname):
    while True:
        print "\t1. Select a Sub-forums"
        print "\t2. Create a Sub-forum"
        print "\t3. Back"
        print "\t4. LogOut"
        option = raw_input("Select your option " + uname + ":" )
        if option == "1":
            while True:
                for i in range(len(output)):
                    print str(i+1)
                    output_dict=convert_from_json_object(output)
                    print_sub_forums(output_dict)
                option = raw_input("Select a Sub-forum : ")
                if option<len(output.split()) or option>len(output.split()):
                    print "Enter a valid option"
                else:
                    output = output.split()
                    d = {}
                    d['action'] = "open_sub_forum"
                    d['forum_name'] = forum_name
                    d['sub_forum']= output[option - 1]
                    return str(d),output[option - 1]
            return
        elif option == "2":
            new_sub_forum = raw_input("Enter the name of the Sub-forum :")
            d = {}
            d['action'] = "new_sub_forum"
            d['forum_name'] = forum_name
            d['new_sub_forum'] = new_sub_forum
            d['created_by'] = uname
            return str(d)
            return
        elif option == "3":
            return "break"
        elif option == "4":
            return "exit"
        else:
            print "Enter a Valid Option"
        pass



if __name__ == "__main__":
    main()


