import sys
import getopt
from . import say_hello
from . import _version

def usage(msg_error=''):

    print(f'\nusage: hello_juan -m "message"')
    print('-h\tHelp')
    print('-v\tVersion')

    if msg_error != '':
        print(f'\nerror: {msg_error}\n')
        sys.exit(1)

    sys.exit(0)

def printVersion():
    print(f'\nversion: {_version.version}\n')
    sys.exit(0)

def check_params():
    global message
    message = ''
    try:
        options, remainder = getopt.gnu_getopt(sys.argv[1:], 'm:hv', ['message=', 'help', 'version', ])
    except:
        usage('Invalid parameters')

    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-v', '--version'):
            printVersion()
        elif opt in ('-m', '--message'):
            message = arg

def main():
    check_params()
    say_hello.say_it(message)

if __name__ == '__main__':
    main()


