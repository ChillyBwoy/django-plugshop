import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-plugshop",
    version = "0.0.1",
    author = "Eugene Cheltsov",
    author_email = "chill.icp@gmail.com",
    description = ("A small shop for Django Framework"),
    long_description = read('README.md'),
    license = "BSD",
    keywords = "plugshop",
    url = "https://github.com/ChillyBwoy/django-plugshop",
    packages = ['plugshop'],
    platforms = ['OS Independent'],
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)