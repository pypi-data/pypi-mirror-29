'''
Created on Mar 9, 2018

@author: khiem
@python3

'''
from setuptools import setup, find_packages

setup(name='xinsonha',
      version='0.5',
      url='https://github.com/the-gigi/pathology',
      license='MIT',
      author='Gigi Sayfan',
      package=['bigQuery'],
      author_email='the.gigi@gmail.com',
      description='Add static script_dir() method to Path',
#       packages=find_packages(exclude=['tests']),
#       long_description=open('README.md').read(),
      zip_safe=False)



import pathlib
import inspect 

# script_dir = pathlib.Path(__file__).parent.resolve()
# print (script_dir)
# print(open(str(script_dir/'markdown.ipynb').read())


class Path(type(pathlib.Path())):
    @staticmethod
    def script_dir():
        file_name = inspect.stack()[1].filename
        p = pathlib.Path(file_name)
        return p.parent.resolve()

# print (Path.script_dir())