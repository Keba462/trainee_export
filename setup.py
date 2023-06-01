# -*- coding: utf-8 -*-
import os

from setuptools import find_packages
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='trainee-export',
    version='0.0.1',
    author=u'Kebadiretse Motlhabi',
    author_email='kmotlhabi@bhp.org.bw',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/Keba462/trainee_export.git',
    license='GPL license, see LICENSE',
    description='Trainee Exports',
    long_description=README,
    zip_safe=False,
    keywords='django trainee export',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)