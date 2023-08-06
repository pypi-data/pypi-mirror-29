# -*- coding:utf-8 -*-
# Created by qinwei on 2017/11/24
#

from hunters.constant import Const
from hunters.cookie import MemoryCookieStore


class UserAgent(Const):
    """常用UA"""
    CHROME = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
    ANDROID = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36"


class BrowserConfig(object):
    """ 统一浏览器配置项, 统一抽象的描述实现浏览器所具备的一些特性"""
    LOCAL_STORE = "/data/hunter/"

    def __init__(self,
                 user_agent=None,
                 local_store=None,
                 image=True,
                 headless=True,
                 execute_bin=None,
                 cookie_store=MemoryCookieStore(),
                 max_body_size=-1,
                 width=1440,
                 height=1000,
                 gpu=False,  # if in gui, can use gpu
                 extra_options=[],
                 manual_url="",  # manual to connect to current open chrome, not auto start..
                 # manual_url="127.0.0.1:9222"
                 disk_cache_size=None):
        """ The Common base Browser Config """

        self.user_agent = user_agent or UserAgent.CHROME

        self.local_store = local_store or BrowserConfig.LOCAL_STORE

        self.image = image

        self.headless = headless

        #: 分布式Cookie/会话保持, 在分布式环境中, 每产生的URL都插入中央队列, 每个爬虫(可能多台机)从中央队列里取出来的内容
        #: 是无状态的, 如果需要维持爬虫的上下文关系, 需要保证有分布式的session维持cookie内容,
        #: 这个cookie可以集中存储.
        self.cookie_store = cookie_store

        self.max_redirects = 3

        self.max_body_size = max_body_size

        self.disk_cache_size = disk_cache_size  # in bytes

        self.execute_bin = execute_bin

        self.height = height

        self.width = width

        self.gpu = gpu

        self.extra_options = extra_options

        self.manual_url = manual_url


DEFAULT_BROWSER_CONFIG = BrowserConfig()
