from distutils.core import setup
setup(
  name = 'hello_juan',
  packages = ['hello_juan'], # this must be the same as the name above
  version = '0.6',
  description = 'Un saludo a Juan',
  author = 'Juan Manuel Mosca',
  author_email = 'juanmosca@gmail.com',
  url = 'https://github.com/juanmosca/hello_juan.git', # use the URL to the github repo
  download_url = 'https://github.com/juanmosca/hello_juan/archive/0.2.tar.gz', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
  entry_points={
      'console_scripts' : [
          'hello_juan = hello_juan.say_hello:say_it' 
          ]
      }
)
