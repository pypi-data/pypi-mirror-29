"""
Python Package for Dingtalk Robot
Author: SF-Zhou
Date: 2018-03-15
"""

import dingtalk_robot
from setuptools import setup


with open('requirements.txt') as f:
    requirements = f.read().split('\n')

setup(
    name=dingtalk_robot.__name__,
    version=dingtalk_robot.__version__,
    description=dingtalk_robot.__description__,
    url=dingtalk_robot.__github__,
    author=dingtalk_robot.__author__,
    author_email=dingtalk_robot.__email__,

    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    keywords='tools dingtalk robot',
    py_modules=['dingtalk_robot'],
    install_requires=requirements,
    extras_require={'test': ['pytest']}
)