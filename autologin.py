import requestmanager
import signal
import argparse
import os.path as path

time_between_heartbeats = 120

passwords = {}
file = "thapar.autologin"

currentuser = ""

parser = argparse.ArgumentParser()

#function called when ctrl_c is called
def ctrl_c(signal, frame):
    logout()
    print("Logging out " + currentuser)
    exit()

def logout():
    global currentuser
    requestmanager.logout_user(currentuser)

def login_all():
    global currentuser
    for username,password in passwords.items():
        currentuser = username
        requestmanager.login(username,password,time_between_heartbeats)
        print("could not reconnect,switching user")
    print("no more passwords entered or available")

def file_exists():
    global file
    if(not(path.isfile(file))):
        file = "thapar.autologin"
        print("Could not find file,using default file 'thapar.autologin'")

def set_arguments(parser):
    parser.add_argument('-u', action="store", dest="user")
    parser.add_argument('-p', action="store", dest="password")
    parser.add_argument('-f', action="store", dest="filename")

def manage_input(arg_input):
    global file,passwords
    if(arg_input.filename != None):
        file = arg_input.filename
    file_exists()
    passwords = requestmanager.load_pwds(file)
    if(arg_input.user != None and arg_input.password!= None):
        passwords[arg_input.user] = arg_input.password
        requestmanager.add_user(arg_input.user,arg_input.password,file)
        print("user " + arg_input.user + "added to the file " + file)
    elif(arg_input.user == None and arg_input.password == None):
        print("")
    else:
        print("Please input both username and password")


if __name__ == "__main__":
    #set custom function at ctrl_c
    signal.signal(signal.SIGINT, ctrl_c)
    set_arguments(parser)
    arg_input = parser.parse_args()
    manage_input(arg_input)
    login_all()
    #requestmanager.login(username,password,120)