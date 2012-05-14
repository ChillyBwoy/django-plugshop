import os
from setuptools import setup, find_packages
import plugshop 

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
    install_requires = (
        'Django>=1.3.1',
        'django-mptt>=0.5.2',
    ),
    keywords = "plugshop",
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    license = "BSD",
    name = "django-plugshop",
    packages = find_packages(exclude=['testshop']),
    platforms = ['OS Independent'],
    url = "https://github.com/ChillyBwoy/django-plugshop",
    version = plugshop.__version__,
    zip_safe = False
)