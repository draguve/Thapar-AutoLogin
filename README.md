#Thapar-AutoLogin
Python Script To Keep Yourself Connected to the Internet At Thapar

##Dependencies
- [Docopt][190d4da5]

  [190d4da5]: http://docopt.org "docopt"

- [Selenium][adb5980f]

  [adb5980f]: http://www.seleniumhq.org/ "selenium"

 - [PhantomJS][6f9ffd6b]

  [6f9ffd6b]: http://phantomjs.org/ "phantomjs"

    Windows:
        pip install selenium docopt
    Linux :
        sudo pip install selenium docopt

## Setup
Use This to command to download PhantomJS binaries for your system

    python ./login -c


##Usage
    Usage:
        login.py
        login.py [--user <USERNAME>][--pass <PASSWORD>][--verbose][--file][--long][--wait <WAIT>][--check]
        login.py --help

    Options:
        -f --file                   Uses Default config.py File For Username Password
        -u --user <USERNAME>        Choose Username to Login
        -p --pass <PASSWORD>        Choose Password to Login
        -l --long                   Enable's Long Mode Where Screen Doent Shrink (Windows Only)
        -v --verbose                Enable Verbose Mode
        -w --wait <WAIT>            Select The Time Between Checks(Default 60)
        -c --check                  Only Checks(and Downloads) if binaries are present

##Make Life Easier

Modify "config.py" file with your username and password to login easily with the command

    python ./login.py -f
