import os 
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='uidgenerator_utils',
    version='0.3',
    packages=['uidgenerator'],
    include_package_data=True,
    description='A Django app to generate model id based on a snowflake of twitter.',
    url='https://github.com/sugar2015/uidgenerator_utils',
    long_description=README,
    author='wim',
    author_email='wim114@dingtalk.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python :: 3.6',
    ],
)
