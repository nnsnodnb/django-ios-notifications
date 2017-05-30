# coding: utf-8
import sys
from setuptools import setup, find_packages

NAME = 'ios-notification'
VERSION = '0.0.4'


def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as f:
        return f.read()


def readlist(filename):
    rows = read(filename).split('\n')
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)


setup(
    name=NAME,
    version=VERSION,
    description='A Django plugin for Apple Notification Service',
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django ios push notification apple apns',
    author='nnsnodnb',
    author_email='ahr63_gej@me.com',
    url='https://github.com/nnsnodnb/django-ios-notifications',
    download_url='https://github.com/nnsnodnb/django-ios-notifications/tarball/master',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['README.rst',
             'requirements.txt',
             'requirements-test.txt'],
    },
    zip_safe=True,
    install_requires=readlist('requirements.txt'),
    test_suite='runtests.run_tests',
    tests_require=readlist('requirements-test.txt')
)

