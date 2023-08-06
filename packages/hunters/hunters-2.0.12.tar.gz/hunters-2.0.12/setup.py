# -*- coding:utf-8 -*-
# Created by qinwei on 2017/8/9
from setuptools import setup, find_packages

setup(
    name='hunters',
    version='2.0.12',
    description="A spider automation framework, provide uniform API to use chrome Dev Protocol and requests",
    author='Qin Wei (ChineseTiger)',
    long_description='Hunters provide a uniform API to call Chrome DevTools  and requests for web crawlers',
    author_email='imqinwei@qq.com',
    url="https://github.com/LoginQin/hunters",
    license='Apache License, Version 2.0',
    packages=find_packages(),
    keywords='hunters spider headless crawlers screenshot',
    install_requires=['requests', 'lxml', 'cssselect', 'redis', 'pychrome==0.2.2', 'cachetools']
    # requests==2.18.1, lxml==3.8.0, cssselect==1.0.1, redis==2.10.5, cachetools==2.0.1
)
