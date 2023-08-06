import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mkeditor',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='A custom form widget of Django for markdown',
    long_description=README,
    url='https://github.com/sugar2015/mkeditor',
    author='wim',
    author_email='wim114@dingtalk.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python :: 3.6',
    ]
)
