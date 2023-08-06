from distutils.core import setup
from hello_juan._version import version

setup(
  name = 'hello_juan',
  packages = ['hello_juan'], # this must be the same as the name above
  version = version,
  description = 'Un saludo a Juan',
  author = 'Juan Manuel Mosca',
  author_email = 'juanmosca@gmail.com',
  licence = 'MIT',
  url = 'https://pypi.python.org/pypi/hello_juan', 
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
  install_requires = ['markdown', ],
  entry_points={
      'console_scripts' : [
          'hello_juan = hello_juan.command_line:main' ,
          ]
      }
)
