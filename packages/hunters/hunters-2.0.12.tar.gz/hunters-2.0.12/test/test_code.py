# -*- coding:utf-8 -*-
# Created by qinwei on 2017/8/8
import logging
import re

from hunters.browser import MiniBrowser
from hunters.constant import Regex
from hunters.defaults import DefaultFilter

print("window.scrollBy({}, {})".format(10, 10))

filter = DefaultFilter()
FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] %(module)s[%(lineno)d]-%(message)s"

logging.basicConfig(level=logging.INFO, format=FORMAT)


def lookup(func):
    print(func("url"))
    print(func("url"))
    print(func("url"))
    print(func("url"))


