# -*- coding:utf-8 -*-
# Created by qinwei on 2017/8/8
import unittest
from concurrent.futures import ThreadPoolExecutor
from time import sleep, time

from hunters.browser import ChromeTab, BaseChrome
from hunters.chrome import ChromeTabDevToolFactory
from hunters.config import BrowserConfig
from hunters.factory.browser_factory import ViewBrowserFactory
from hunters.pool import ResourcePool


class TestBrowser(unittest.TestCase):
    def setUp(self):
        canary = r"C:\Users\ADMIN\AppData\Local\Google\Chrome SxS\Application\chrome.exe"
        # chrome = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        self.config = BrowserConfig(
            execute_bin=canary,
            headless=False)

    def test_factory(self):
        factory = ChromeTabDevToolFactory(browser_config=self.config)
        chrome = BaseChrome(factory=factory)
        for i in range(10):
            r = chrome.get("https://baidu.com")
            # r = chrome.get("https://baidu.com")
            # r.window_size(1000, 1000)
            # r.scroll_by(0, 10000)
            print(r.execute_js("document.title"))
            print(r.text)
            print(r.cookies(urls=["baidu.com"]))
            # print(r.get_all_cookies())
            print(i)

    def test_pool(self):
        factory = ViewBrowserFactory(browser_config=self.config)
        pool = ResourcePool(factory=factory, init_count=2, max_count=4)
        threadpool = ThreadPoolExecutor(max_workers=5)

        def run_url(item):
            print("OK {}".format(item))
            start = time()
            c = pool.get()
            r = c.get("http://qq.com")
            pool.return_resource(c)
            print("end {}, {}".format(item, time() - start))

        for item in range(20):
            threadpool.submit(run_url, (item))

        while True:
            sleep(1)

    def test_multi_chrometab(self):
        cc = ChromeTab(browser_config=self.config)
        cc2 = ChromeTab(browser_config=self.config)
        r = cc.get("http://baidu.com")
        r2 = cc2.get("http://qq.com")
        print(r.text)


if __name__ == '__main__':
    main = TestBrowser()
    main.setUp()
    main.test_pool()
