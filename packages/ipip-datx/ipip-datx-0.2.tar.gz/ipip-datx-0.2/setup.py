# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='ipip-datx',
    version=0.2,
    description=(
        'IPIP.net官方支持维护的IP数据库datx格式解析代码库'
    ),
    author='IPIP.net',
    author_email='frk@ipip.net',
    maintainer='frk',
    maintainer_email='frk@ipip.net',
    license='Apache License Version 2.0',
    packages=['datx'],
    platforms=["all"],
    url='https://github.com/ipipdotnet/datx-python',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)