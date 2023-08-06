# -*- coding:utf-8 -*-
# Created by qinwei on 2017/11/17
#

from hunters.browser import MiniBrowser, ViewBrowser
from hunters.factory import Factory


class MiniBrowserFactory(Factory):
    """"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def new_instance(self):
        return MiniBrowser(browser_config=self.config())

    def destroy(self, obj):
        """ """

    def destroy_all(self, pool_list=None):
        """ """


class ViewBrowserFactory(Factory):
    """"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def new_instance(self):
        return ViewBrowser(browser_config=self.config())

    def destroy(self, obj):
        obj.close()
        obj.quit()

    def destroy_all(self, pool_list=None):
        for obj in pool_list:
            obj.close()
            obj.quit()

# bin_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe {}".format(" ".join(chromeFlags))


# bin = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222"
