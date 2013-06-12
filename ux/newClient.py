__author__ = 'Sumzy'

import JSON_Socket
import socket

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


dict_user = {}
authen_dict = {}


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
    return int(year), int(month), int(date)


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
        if len(password) >= 6 and len(password) <= 10 and re.match(
                "^[a-zA-Z]{1}[a-zA-Z0-9]*$", password):
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
    dict_user['username'] = username
    dict_user['password'] = password
    dict_user['DOB'] = DOB
    dict_user['email'] = email
    return dict_user


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

    option = raw_input("Select the Forum you wish to View : ")

    if option == '1':
        print "\nYou have entered Education Forum"
    elif option == '2':
        print "\nYou have entered Sports Forum"
    elif option == '3':
        print "\nYou have entered Entertainment Forum"
    elif option == '4':
        print "\nYou have entered Technology Forum"
    elif option == '5':
        print "\nYou have entered News Forum"
    elif option == '6':
        print "\nYou have entered Health Forum"
    elif option == '7':
        print "\nYou have entered Miscellaneous Forum"
    else:
        print "\nPlease select a Valid option"

    pass


def main():
    global dict_user

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
            client_json = JSON_Socket.json()
            client_json.deserializer(input)
            client.send(client_json.representation())
            received = client.receive()
            print received

        elif choice == '2':
            input = signup()
            client_json = JSON_Socket.json()
            client_json.deserializer(input)
            client.send(client_json.representation())
            received = client.receive()
            print received

        elif choice == '3':
            display()


        elif choice == '4':
            client.close()

        else:
            print "\nPlease Select a Valid Option"

    pass


if __name__ == "__main__":
    main()


