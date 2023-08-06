# -*- coding:utf-8 -*-

from setuptools import setup
from setuptools import find_packages
from TkToolsD import __version__

setup(
    name='TkToolsD',
    version=__version__,
    description=(
        'Some usefull tk widgets like: ImgView, ScrollView.'
    ),
    long_description=open('README.rst').read(),
    author='dekiven',
    author_email='dekiven@163.com',
    # maintainer='<维护人员的名字>',
    # maintainer_email='<维护人员的邮件地址',
    license='BSD License',
    packages=find_packages(),
    install_requires=[
    	'DKVTools',			# common funcs include
    	'Pillow',
    	# 'other>=1.1'
    ],
    data_files=[
        # 'version.txt',
    ],
    platforms=["all"],
    url='https://www.baidu.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
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