from markdown import markdown

def say_it(message=''):
    print("hello Juan!")
    if message != '':
        print("Your message is '{0}'".format(message))

if __name__ == "__main__":
    say_it()
