"""
Usage:
    login.py
    login.py [--user <USERNAME>][--pass <PASSWORD>][--verbose][--file][--long][--wait <WAIT>][--check]
    login.py --help

Options:
    -f --file                   Uses Default login.conf File For Username Password
    -u --user <USERNAME>        Choose Username to Login
    -p --pass <PASSWORD>        Choose Password to Login
    -l --long                   Enable's Long Mode Where Screen Doent Shrink (Windows Only)
    -v --verbose                Enable Verbose Mode
    -w --wait <WAIT>            Select The Time Between Checks(Default 60)
    -c --check                  Only Checks(and Downloads) if binaries are present
"""
#Written By Draguve
#Twitter : @Draguve
#Github : https://github.com/Draguve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from docopt import docopt
import urllib2,os,zipfile,sys,httplib,platform,tarfile,time
art = """
                 __           ___
                /\\ \\__       /\\_ \\                   __
   __     __  __\\ \\ ,_\\   ___\\//\\ \\     ___      __ /\\_\\    ___
 /'__`\\  /\\ \\/\\ \\\\ \\ \\/  / __`\\\\ \\ \\   / __`\\  /'_ `\\/\\ \\ /' _ `\\
/\\ \\L\\.\\_\\ \\ \\_\\ \\\\ \\ \\_/\\ \\L\\ \\\\_\\ \\_/\\ \\L\\ \\/\\ \\L\\ \\ \\ \\/\\ \\/\\ \\
\\ \\__/.\\_\\\\ \\____/ \\ \\__\\ \\____//\\____\\ \\____/\\ \\____ \\ \\_\\ \\_\\ \\_\\
 \\/__/\\/_/ \\/___/   \\/__/\\/___/ \\/____/\\/___/  \\/___L\\ \\/_/\\/_/\\/_/
                                                 /\\____/
                                                 \\_/__/
"""
verbose = False
lmode = False
user = "Put Username Here"
pwd = "Put Password Here"
wait = 60

def downloadFile(url):
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print status,
    f.close()

def extractAndDelete(file_name):
    if sysOS == "Windows":
        with zipfile.ZipFile(file_name,'r') as zfile:
            zfile.extractall()
    elif sysOS == "Linux":
        tar = tarfile.open(file_name)
        tar.extractall()
        tar.close()
    else:
        print "System Not Supported"
        exit()
    os.remove(file_name)

def checkForPhantom():
    if sysOS=="Windows":
        if(not(os.path.isfile("phantomjs-2.1.1-windows/bin/phantomjs.exe"))):
            print "Press Y to Download PhantomJS and N to Exit"
            answer = raw_input(">>>")
            if(answer.lower() == "y"):
                downloadFile("https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip")
                extractAndDelete("phantomjs-2.1.1-windows.zip")
            else:
                print "Download Canceled,Exiting..."
                exit()
    if sysOS=="Linux":
        if(not(os.path.isfile("phantomjs-2.1.1-linux-x86_64/bin/phantomjs"))):
            print "Press Y to Download PhantomJS and N to Exit"
            answer = raw_input(">>>")
            if(answer.lower() == "y"):
                downloadFile("https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2")
                extractAndDelete("phantomjs-2.1.1-linux-x86_64.tar.bz2")
            else:
                print "Download Canceled,Exiting..."
                exit()


def startScript():
    start = True
    sys.stdout.write("\x1b]2;Thapar AutoLogin\x07")
    if sysOS=="Windows":
        if not(verbose) and not(lmode):
            os.system("mode 68,13")
    currentDriver = putInPass(user,pwd)
    currentUsageDriver = startUsageDriver(user,pwd)
    usage = getUsage(currentUsageDriver)
    waitWithTimer(5)
    while True:
        if checkNet():
            if start == True:
                print "Logged In"
                print "Logged in"
                start = False
            waitTimerWithUsage(wait,usage)
            usage = getUsage(currentUsageDriver)
            if usage>3072.0:
                print "All Data Used.. Exiting"
                exit()
        else:
            currentDriver.close()
            start = True
            currentDriver = putInPass(user,pwd)
            currentUsageDriver = startUsageDriver(user,pwd)
            usage = getUsage(currentUsageDriver)
            waitTimerWithUsage(5,usage)

def checkNet():
    h = httplib.HTTPConnection('216.58.192.142')
    h.request('HEAD', '/')
    response = h.getresponse()
    if 300 <= response.status < 400:
        location = response.getheader('Location')
        return True
    print "Problem Connecting To The Net"
    return False


def putInPass(username,password):
    #b = webdriver.Chrome("chromedriver.exe")
    if sysOS=="Windows":
        if verbose:
            b = webdriver.PhantomJS("phantomjs-2.1.1-windows/bin/phantomjs.exe",service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',"--webdriver-loglevel=DEBUG"])
        else:
            b = webdriver.PhantomJS("phantomjs-2.1.1-windows/bin/phantomjs.exe",service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'],service_log_path=os.path.devnull)
    elif sysOS=="Linux":
        if verbose:
            b = webdriver.PhantomJS("phantomjs-2.1.1-linux-x86_64/bin/phantomjs",service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',"--webdriver-loglevel=DEBUG"])
        else:
            b = webdriver.PhantomJS("phantomjs-2.1.1-linux-x86_64/bin/phantomjs",service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'],service_log_path=os.path.devnull)
    else:
        print "This OS isnt Supported"
        exit()
    b.get("http://172.31.1.6:8090/httpclient.html")
    b.set_window_size(1024, 768)
    try:
        userbar = b.find_element_by_xpath('//*[@id="usernametxt"]/td/input')
    except NoSuchElementException :
        print "Could Not Find Page"
        print "Please Check If the Laptop is Connected to TU Wifis"
        exit()
    userbar.clear()
    userbar.click()
    userbar.send_keys(username)
    passbar = b.find_element_by_xpath('/html/body/form/div[1]/div[2]/div[2]/table/tbody/tr[4]/td/input')
    passbar.clear()
    passbar.send_keys(password)
    button = b.find_element_by_xpath('//*[@id="logincaption"]')
    button.click()
    return b

def waitWithTimer(seconds):
    clearWindow()
    completed = False
    sec = seconds
    print " "
    while not(completed):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        print("Time Till Next Check "+str(sec))
        sec=sec-1
        time.sleep(1)
        if(not(sec>0)):
            completed=True

def waitTimerWithUsage(seconds,data):
    clearWindow()
    completed = False
    sec = seconds
    print " "
    print " "
    while not(completed):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        print("Time Till Next Check "+str(sec))
        print "Data Left To Use :"+str(3072.0 - data)
        sec=sec-1
        time.sleep(1)
        if(not(sec>0)):
            completed=True

def startUsageDriver(username,password):
    #c = webdriver.Chrome(executable_path="chromedriver.exe")
    if sysOS=="Windows":
        if verbose:
            c = webdriver.PhantomJS("phantomjs-2.1.1-windows/bin/phantomjs.exe",service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',"--webdriver-loglevel=DEBUG"])
        else:
            c = webdriver.PhantomJS("phantomjs-2.1.1-windows/bin/phantomjs.exe",service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'],service_log_path=os.path.devnull)
    elif sysOS=="Linux":
        if verbose:
            c = webdriver.PhantomJS("phantomjs-2.1.1-linux-x86_64/bin/phantomjs",service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',"--webdriver-loglevel=DEBUG"])
        else:
            c = webdriver.PhantomJS("phantomjs-2.1.1-linux-x86_64/bin/phantomjs",service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'],service_log_path=os.path.devnull)
    else:
        print "This OS isnt Supported"
        exit()
    c.get("https://172.31.1.6/userportal/webpages/myaccount/login.jsp")
    c.set_window_size(1024,768)
    usageUser = c.find_element_by_xpath('//*[@id="username"]')
    usageUser.clear()
    usageUser.click()
    usageUser.send_keys(username)
    usagePass = c.find_element_by_xpath('//*[@id="password"]')
    usagePass.clear()
    usagePass.click()
    usagePass.send_keys(password)
    usageButton = c.find_element_by_xpath('//*[@id="normalTBody"]/input[3]')
    usageButton.click()
    waitWithTimer(5)
    return c

def getUsage(c):
    c.refresh()
    waitWithTimer(5)
    try:
        mbs = c.find_element_by_xpath('//*[@id="content3"]/div[2]/table/tbody/tr/td/table/tbody/tr[5]/td[5]')
    except NoSuchElementException :
        print "Could Not Find Page"
        print "Please Check If The UserName And Password Are Correct "
        exit()

    usageS = str(mbs.text)
    usageF = float(usageS[:-2])
    return usageF

def getAnswer(question):
    print question
    return raw_input(">>>")

def clearWindow():
    if verbose==False:
        if sysOS=="Linux":
            os.system("clear")
        elif sysOS=="Windows":
            os.system("cls")
        else :
            print "There is an OS Problem"
            exit()
        print art

if __name__ == '__main__':
    sys.dont_write_bytecode = True
    arguments = docopt(__doc__)
    sysOS = platform.system()
    checkForPhantom()
    if arguments['--check']==True:
        exit()
    if arguments['--file']==True:
        import config
        user,pwd,verbose,lmode,wait = config.getUP()
        if arguments['--verbose']==True:
            verbose = True
        if arguments['--long']==True:
            lmode = True
        if arguments['--wait']!=None:
            wait = int(arguments['--wait'])

    else:
        if arguments['--user']==None:
            user=getAnswer("Please Insert A Username")
        else:
            user=arguments['--user']
        if arguments['--pass']==None:
            pwd=getAnswer("Please Insert A Password")
        else:
            pwd=arguments['--pass']
        if arguments['--wait']!=None:
            wait = int(arguments['--wait'])
        verbose = arguments['--verbose']
        lmode = arguments['--long']
    print user,pwd
    startScript()
