import requests,time
import urllib.request
import ssl
import xml.etree.ElementTree as xml
import pickle 
import socket
import os.path as path 

requests.packages.urllib3.disable_warnings() 

#uses this server 
REMOTE_SERVER = "https://github.com/"

#sends login ajax request 
def login_user(user,password):
    try:
        time_in_ms = time.time()*1000
        data = {"mode" : 191,"username":user,"password":password,"a":str(int(time_in_ms)),"producttype":0}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded;',
            'X-Requested-With': 'XMLHttpRequest'
        }
        s = requests.Session()
        response = s.post(
            url='https://172.31.1.6:8090/login.xml',
            data=data,
            headers=headers,
            verify=False
        )
        return response.text
    except requests.exceptions.ConnectionError:
        print("Could not connect to server")


def logout_user(user):
    time_in_ms = time.time()*1000
    data = {"mode" : 193,"username":user,"a":str(int(time_in_ms)),"producttype":0}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
       'Content-Type': 'application/x-www-form-urlencoded;',
        'X-Requested-With': 'XMLHttpRequest'
    }
    s = requests.Session()
    response = s.post(
        url='https://172.31.1.6:8090/login.xml',
        data=data,
        headers=headers,
        verify=False
    )

#verifies the xml returned is logged in
def verify_login(xml_data):
        if(xml_data == None):
            return False
        root = xml.fromstring(xml_data)
        retdata = root[1].text
        if(retdata=='You have successfully logged in'):
            return True
        elif(retdata=='The system could not log you on. Make sure your password is correct'):
            print("Wrong password or username")
            return False
        else:
            #print("Could not log you on")
            return False

#sends a single is live request 
def send_heartbead(username):
    url = "https://172.31.1.6:8090/live?mode=192&username=" + username + "&a=" + str(int(time.time()*1000)) + "&producttype=0"
    check =  urllib.request.urlopen(url,context=ssl._create_unverified_context()).read()
    if check!=None:
        return True
    return False

#load a dict from a file 
def load_pwds(filename):
    if(not(path.isfile(filename))):
        save_pwds(filename,{})
        return {}
    with open(filename,'rb') as f:
        __passwords__ = pickle.load(f)
    return __passwords__

#saves a dict containing username:password to a file
def save_pwds(filename,pwds):
    with open(filename,'wb') as f:
        pickle.dump(pwds,f)

#adds user to filename
def add_user(username,password,filename):
    passes = load_pwds(filename)
    passes[username]=password
    save_pwds(filename,passes)  

#checks if the device is connected to the internet
def is_connected():
    try:
        response = urllib.request.urlopen(REMOTE_SERVER)
        return True
    except:
        pass
    return False

#log's in and checks if the response was positive   
def checked_login(username,password):
    response = login_user(username,password)
    if(verify_login(response)):
        return True
    else:
        return False

#logs in the website and checks if connected to the internet
def try_login(username,password):
    if(checked_login(username,password)):
        if(is_connected()):
            return True
        else:
            return False
    else:
        return False

#sends heartbeat and checks if connected to the internet
def heartbeat_checked(username):
    return send_heartbead(username) and is_connected()

#login to username and persist for as long as possible
def login(username,password,time_between_heartbeats):
    if(try_login(username,password)):
        print("Logged into user " + username)
        while(True):
            #sleeps cut into 1 seconds to handle sigint
            for i in range(time_between_heartbeats):
                time.sleep(1)
            if(not(heartbeat_checked(username))):
                break
            else:
                print("*")
    else:
        print("Could not login " + username)

#logs in all user one by one,pwds stored in filename
def login_from_file(filename,time_between_heartbeats):
    passes = load_pwds(filename)
    for username,password in passes.items():
        login(username,password,time_between_heartbeats)
