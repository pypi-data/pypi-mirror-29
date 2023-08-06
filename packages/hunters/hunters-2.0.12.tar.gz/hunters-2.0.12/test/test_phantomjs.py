# -*- coding:utf-8 -*-
# Created by qinwei on 2017/11/15
#
import unittest
from time import time

import logging
from selenium import webdriver

from hunters.browser import ViewBrowser

URL_LIST = ['http://www.jianshu.com/p/8b1a48833b94', 'http://www.jianshu.com/p/79df4bc92800', 'http://www.jianshu.com/p/84dd7caeb990',
            'http://www.jianshu.com/p/d1d2f1e8e2e4', 'http://www.jianshu.com/p/26507d708306', 'http://www.jianshu.com/p/6cfa6df9df68',
            'http://www.jianshu.com/p/45fae71ad26b', 'http://www.jianshu.com/p/aeb1eea885ae', 'http://www.jianshu.com/p/0fa1d71f2650',
            'http://www.jianshu.com/p/395c8b15d385', 'http://www.jianshu.com/p/9ddcf949676f', 'http://www.jianshu.com/p/c0ca2c230149',
            'http://www.jianshu.com/p/7813463e4772', 'http://www.jianshu.com/p/437c2ae96396', 'http://www.jianshu.com/p/11a958b4ea26',
            'http://www.jianshu.com/p/3ebd923f63b7', 'http://www.jianshu.com/p/8b14bbcbf886', 'http://www.jianshu.com/p/d29ce5cb9a0c',
            'http://www.jianshu.com/p/a8c936689233', 'http://www.jianshu.com/p/b81562687f3e']

NEW_LIST = ['http://news.xinhuanet.com/world/2017-11/15/c_129741004.htm', 'http://news.xinhuanet.com/politics/leaders/2017-11/14/c_1121953758.htm',
            'http://world.huanqiu.com/special/2017APEC/index.html?from=bdwz', 'http://news.xhby.net/system/2017/11/14/030765790.shtml',
            'http://news.xinhuanet.com/politics/2017-11/15/c_1121959898.htm', 'http://news.xinhuanet.com/world/2017-11/14/c_1121955602.htm',
            'http://news.cctv.com/2017/11/14/ARTIQvcSOAjXcaZ5OIFtJf4D171114.shtml', 'http://news.ifeng.com/mainland/special/xsdjj/?_zbs_baidu_news',
            'http://www.ddcpc.cn/2017/jr_1113/113598.html', 'http://news.gmw.cn/2017-11/15/content_26790042.htm',
            'http://www.am774.com/activity/laoshezhangdegushi.shtml', 'http://news.youth.cn/gn/201711/t20171115_11012409.htm',
            'http://world.huanqiu.com/article/2017-11/11380352.html?from=bdwz ', 'http://china.huanqiu.com/article/2017-11/11380050.html?from=bdwz',
            'http://news.ifeng.com/a/20171115/53265266_0.shtml?_zbs_baidu_news', 'http://china.huanqiu.com/article/2017-11/11379982.html?from=bdwz',
            'http://china.huanqiu.com/article/2017-11/11379260.html?from=bdwz', 'http://news.ifeng.com/a/20171115/53264294_0.shtml?_zbs_baidu_news',
            'https://baijia.baidu.com/topic?topic_id=718', 'http://xinwen.eastday.com/a/xjump.html?id=171115121048639',
            'http://china.huanqiu.com/article/2017-11/11379367.html?from=bdwz', 'http://news.china.com/domestic/945/20171115/31665340.html',
            'http://china.huanqiu.com/article/2017-11/11379874.html?from=bdwz?', 'http://china.huanqiu.com/article/2017-11/11380275.html?from=bdwz ',
            'http://world.huanqiu.com/exclusive/2017-11/11380341.html?from=bdwz', 'http://news.ifeng.com/a/20171115/53266932_0.shtml?_zbs_baidu_news',
            'http://world.huanqiu.com/exclusive/2017-11/11379416.html?from=bdwz?',
            'http://news.ifeng.com/a/20171115/53270527_0.shtml?_zbs_baidu_news', 'http://xinwen.eastday.com/a/xjump.html?id=171115130117314',
            'http://news.ifeng.com/a/20171115/53265948_0.shtml?_zbs_baidu_news', 'http://society.huanqiu.com/article/2017-11/11379721.html?from=bdwz',
            'http://finance.china.com.cn/hz/sh/2345/20171115/18061.shtml', 'http://society.huanqiu.com/article/2017-11/11380111.html?from=bdwz',
            'http://finance.china.com.cn/hz/sh/2345/20171115/18060.shtml', 'http://finance.china.com.cn/hz/sh/2345/20171115/18066.shtml',
            'http://xinwen.eastday.com/a/xjump.html?id=171115123025402', 'http://news.ifeng.com/a/20171115/53273421_0.shtml?_zbs_baidu_news',
            'http://china.huanqiu.com/article/2017-11/11379326.html?from=bdwz', 'http://news.china.com/socialgd/10000169/20171115/31666218.html',
            'http://finance.china.com.cn/hz/sh/2345/20171115/18040.shtml', 'http://society.huanqiu.com/article/2017-11/11379497.html?from=bdwz',
            'http://news.ifeng.com/a/20171115/53266049_0.shtml?_zbs_baidu_news']


class seleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS(executable_path=r"D:\data\apps\phantomjs-2.1.1-windows\bin\phantomjs.exe",
                                          service_args=["--disk-cache=true", "--load-images=true", "--web-security=false"])
        option = webdriver.ChromeOptions()
        option.add_argument('--allow-running-insecure-content')
        option.add_argument('--disable-web-security')
       # option.add_argument("--headless")
        # option.add_argument("--disable-gpu")
        option.add_argument("--disable-background-networking")
        option.add_argument("--disable-client-side-phishing-detection")

        #prefs = {"profile.managed_default_content_settings.images": 2}  # disable image
        #option.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(executable_path=r"D:\webdriver\chromedriver.exe", chrome_options=option)
        # self.driver = ViewBrowser()
        self.driver.get("http://baidu.com")

    def testEle(self):
        driver = self.driver
        MAX = 50
        for url in range(100):
            start = time()
            driver.get("http://baidu.com")
            #driver.page_source
            second = time() - start
            print("%.3f" % second)


if __name__ == "__main__":
    unittest.main()
