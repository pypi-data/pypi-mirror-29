import sys
from markdown import markdown

def say_it():
    print("hello Juan!")
    args = sys.argv[1:]
    if len(args) > 0:
        str_args = " ".join(args)
        print("You told me: '{0}'".format(str_args))

if __name__ == "__main__":
    say_it()
