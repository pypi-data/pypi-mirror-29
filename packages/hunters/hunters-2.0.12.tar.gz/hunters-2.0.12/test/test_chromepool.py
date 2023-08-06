# -*- coding:utf-8 -*-
# Created by qinwei on 2017/11/23
#
import unittest
from time import sleep

import pychrome

from hunters.chrome import open_chrome

NEW_LIST = ['http://news.xinhuanet.com/world/2017-11/15/c_129741004.htm',
            'http://news.xinhuanet.com/politics/leaders/2017-11/14/c_1121953758.htm',
            'http://world.huanqiu.com/special/2017APEC/index.html?from=bdwz',
            'http://news.xhby.net/system/2017/11/14/030765790.shtml',
            'http://news.xinhuanet.com/politics/2017-11/15/c_1121959898.htm',
            'http://news.xinhuanet.com/world/2017-11/14/c_1121955602.htm',
            'http://news.cctv.com/2017/11/14/ARTIQvcSOAjXcaZ5OIFtJf4D171114.shtml',
            'http://news.ifeng.com/mainland/special/xsdjj/?_zbs_baidu_news',
            'http://www.ddcpc.cn/2017/jr_1113/113598.html', 'http://news.gmw.cn/2017-11/15/content_26790042.htm',
            'http://www.am774.com/activity/laoshezhangdegushi.shtml',
            'http://news.youth.cn/gn/201711/t20171115_11012409.htm',
            'http://world.huanqiu.com/article/2017-11/11380352.html?from=bdwz ',
            'http://china.huanqiu.com/article/2017-11/11380050.html?from=bdwz',
            'http://news.ifeng.com/a/20171115/53265266_0.shtml?_zbs_baidu_news',
            'http://china.huanqiu.com/article/2017-11/11379982.html?from=bdwz',
            'http://china.huanqiu.com/article/2017-11/11379260.html?from=bdwz',
            'http://news.ifeng.com/a/20171115/53264294_0.shtml?_zbs_baidu_news',
            'https://baijia.baidu.com/topic?topic_id=718', 'http://xinwen.eastday.com/a/xjump.html?id=171115121048639',
            'http://china.huanqiu.com/article/2017-11/11379367.html?from=bdwz',
            'http://news.china.com/domestic/945/20171115/31665340.html',
            'http://china.huanqiu.com/article/2017-11/11379874.html?from=bdwz?',
            'http://china.huanqiu.com/article/2017-11/11380275.html?from=bdwz ',
            'http://world.huanqiu.com/exclusive/2017-11/11380341.html?from=bdwz',
            'http://news.ifeng.com/a/20171115/53266932_0.shtml?_zbs_baidu_news',
            'http://world.huanqiu.com/exclusive/2017-11/11379416.html?from=bdwz?',
            'http://news.ifeng.com/a/20171115/53270527_0.shtml?_zbs_baidu_news',
            'http://xinwen.eastday.com/a/xjump.html?id=171115130117314',
            'http://news.ifeng.com/a/20171115/53265948_0.shtml?_zbs_baidu_news',
            'http://society.huanqiu.com/article/2017-11/11379721.html?from=bdwz',
            'http://finance.china.com.cn/hz/sh/2345/20171115/18061.shtml',
            'http://society.huanqiu.com/article/2017-11/11380111.html?from=bdwz',
            'http://finance.china.com.cn/hz/sh/2345/20171115/18060.shtml',
            'http://finance.china.com.cn/hz/sh/2345/20171115/18066.shtml',
            'http://xinwen.eastday.com/a/xjump.html?id=171115123025402',
            'http://news.ifeng.com/a/20171115/53273421_0.shtml?_zbs_baidu_news',
            'http://china.huanqiu.com/article/2017-11/11379326.html?from=bdwz',
            'http://news.china.com/socialgd/10000169/20171115/31666218.html',
            'http://finance.china.com.cn/hz/sh/2345/20171115/18040.shtml',
            'http://society.huanqiu.com/article/2017-11/11379497.html?from=bdwz',
            'http://news.ifeng.com/a/20171115/53266049_0.shtml?_zbs_baidu_news']


class TestChromePool(unittest.TestCase):
    def setUp(self):
        open_chrome(9223, headless=False)

    def test_main(self):
        def responseReceived(**kwargs):
            request_id = kwargs.get("requestId")
            print(request_id, kwargs.get("type"), kwargs.get("response").get("url"))
            print(tab.Network.getResponseBody(requestId=request_id))  # {"body":"",  "base64Encoded": True/False }
            # Network.getResponseBody

        browser = pychrome.Browser(url="http://127.0.0.1:{}".format(9223))
        # tab = browser.new_tab("chrome://settings/content/images")
        tab = browser.new_tab("about:blank")
        tab.Network.enable()
        tab.Network.responseReceived = responseReceived
        tab.Network.setBlockedURLs(urls=[".css", ".jpg", ".png", ".ico", ".gif", ".jpeg", "img="])
        tab.Network.setDataSizeLimitsForTest(maxTotalSize=1024 * 1024, maxResourceSize=300 * 1024)
        tab.Page.navigate(url="http://baidu.com")
        try:
            # 实验性的接口测试通过, 可以动态调整windows大小, GUI模式下才行, Headless不行
            bounds = tab.Browser.getWindowBounds(windowId=1)

            bounds = {'height': 1100,
                      'left': 502,
                      'top': 22,
                      'width': 1440,
                      'windowState': 'normal'}

            tab.Browser.setWindowBounds(windowId=1, bounds=bounds)
        except Exception as e:
            print(e)

        data = tab.Network.getAllCookies()
        tab.Page.navigate(url="http://www.sohu.com/a/205949961_255783?_f=index_news_18?pvid=ab2a3f3fa09b29b9")
        chromedata = tab.Runtime.evaluate(expression="chrome.contentSettings", returnByValue=True, awaitPromise=True)
        print(chromedata)
        # tab.Browser.close()
        # print(data)
        while True:
            sleep(10)
