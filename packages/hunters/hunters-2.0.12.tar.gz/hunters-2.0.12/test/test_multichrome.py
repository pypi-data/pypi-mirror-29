# -*- coding:utf-8 -*-
# Created by qinwei on 2017/11/17
#
import re
import threading
from base64 import b64decode
from time import sleep

from hunters.factory import ResourcePool, ChromeTabDevToolFactory
from test.test_chromepool import NEW_LIST

COUNT = 20
chrome_factory = ChromeTabDevToolFactory(headless=True)
# chrome_factory = ChromeFactory(headless=True)
pool = ResourcePool(factory=chrome_factory, init_count=COUNT)


def get_page(url_):
    tab = pool.get()
    tab.Page.enable()
    tab.Page.setAdBlockingEnabled(enabled=True)
    result = tab.Page.navigate(url=url_, timeout=10)
    pool.return_resource(tab)


def scroll_by():
    tab = pool.get()
    print(tab.Runtime.evaluate(expression="window.scrollBy(0, 3000)", returnByValue=False, awaitPromise=True))
    pool.return_resource(tab)


def get_title():
    tab = pool.get()
    print(tab.Runtime.evaluate(expression="document.title", returnByValue=False, awaitPromise=True))
    pool.return_resource(tab)


def set_value(value):
    tab = pool.get()
    print(tab.Runtime.evaluate(expression="data_url={}".format(value), returnByValue=False, awaitPromise=True))
    pool.return_resource(tab)


def sceenshot():
    print("start screenshot")
    # XXX 不能带clip, 并且需要fromSurface=True headless才能截屏!!!
    tab = pool.get()
    sleep(2)
    # bounds = {'height': 800,
    #           'left': 0,
    #           'top': 0,
    #           'width': 800,
    #           'windowState': 'normal'}
    #
    # tab.Browser.setWindowBounds(windowId=1, bounds=bounds)  # XXX headless模式下找不到setWindowBounds
    width, height = 1280, 2000
    tab.Target.activateTarget(targetId=tab.id)
    data = tab.Emulation.setDeviceMetricsOverride(width=width, height=height, deviceScaleFactor=0, mobile=False,
                                                  fitWindow=True)
    print(data)
    data = tab.Emulation.setVisibleSize(width=width, height=height)
    print(data)
    result = tab.Page.captureScreenshot(format="png", quality=1, fromSurface=True, fullPage=True)
    base64 = result.get('data', "")
    data = tab.Runtime.evaluate(expression="document.title", returnByValue=True, awaitPromise=True)
    print(data)
    filename = data.get("result").get("value")
    unsafe_code = re.compile("[^\u4e00-\u9fa5a-z0-9]+", re.I)
    save_file = "D:/{}.jpg".format(unsafe_code.sub("", filename))
    print(save_file)
    with open(save_file, "wb+") as f:
        f.write(b64decode(base64))
    pool.return_resource(tab)


def main():
    for i in NEW_LIST[:COUNT]:
        get_page(i)

    sleep(3)

    threads = []
    for i in range(COUNT):
        try:
            t = threading.Thread(target=sceenshot, args=())
            threads.append(t)
            # scroll_by()
            # get_title()
            # set_value(i)
            # sceenshot()  # XXX 执行截图需要tab必须是activity的.
            # sleep(1)
        except Exception as e:
            print(e)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    sleep(20)

    pool.close_all()


main()

# for i in range(10):
#     print(tab.Runtime.evaluate(expression="location.href", returnByValue=False, awaitPromise=True))
