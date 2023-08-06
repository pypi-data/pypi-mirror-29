# -*- coding:utf-8 -*-
# Created by qinwei on 2017/8/8
import logging

from hunters.browser import ViewBrowser
from hunters.config import BrowserConfig

logging.basicConfig(level=logging.DEBUG)
# v = ViewBrowser()
canary = r"C:\Users\ADMIN\AppData\Local\Google\Chrome SxS\Application\chrome.exe"
chrome = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
c = BrowserConfig(execute_bin=canary, headless=False)
domain = "duba.com"
view = ViewBrowser(browser_config=c)
r = view.get("http://{}".format(domain), timeout=5)
for i in range(3):
    r.scroll_by(0, 2000)
    r.wait(2.5)

r.wait(10)
r.screenshot_as_png("{}.png".format(domain), full_page=True)

r.wait(10)
print("OK")
