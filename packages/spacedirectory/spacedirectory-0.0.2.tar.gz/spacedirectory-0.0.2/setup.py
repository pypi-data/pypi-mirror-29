#!/usr/bin/env python3
from setuptools import setup, find_packages
import spacedirectory


package = 'spacedirectory'
version = spacedirectory.version
url = 'https://framagit.org/SebGen/spacedirectory',
author = "Sébastien Gendre"
author_email = 'seb@k-7.ch'
license = 'GPLv3'

setup(
    name=package,
    version=version,
    url=url,
    description=spacedirectory.description,
    long_description=open('README.org').read(),
    author=author,
    author_email=author_email,
    license=license,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='spacedirectory space-api',
    python_requires='>=3',
    install_requires=open('requirements.txt').read(),
    entry_points={
        'console_scripts': [
            'spacedirectory = spacedirectory.cli:main',
        ],
    }
)
