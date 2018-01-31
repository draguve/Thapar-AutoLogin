import requestmanager
import argparse
import signal

username = "username"
password = "password"

#function called when ctrl_c is called
def ctrl_c(signal, frame):
    requestmanager.logout_user(username)
    print("Logging out " + username)
    exit()

signal.signal(signal.SIGINT, ctrl_c)

if __name__ == "__main__":
    requestmanager.login(username,password,120)