import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    author = "Eugene Cheltsov",
    author_email = "chill.icp@gmail.com",
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    description = ("A small shop for Django Framework"),
    download_url='',
    include_package_data = True,
    keywords = "plugshop",
    long_description = read('README.md'),
    license = "BSD",
    name = "django-plugshop",
    packages = ['plugshop'],
    packages = find_packages(exclude=('testshop',),
    platforms = ['OS Independent'],
    url = "https://github.com/ChillyBwoy/django-plugshop",
    version = "0.0.1dev",
    zip_safe = True,
)