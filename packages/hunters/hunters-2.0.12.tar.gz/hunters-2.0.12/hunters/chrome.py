# -*- coding:utf-8 -*-
# Created by qinwei on 2017/11/29
#
import atexit
import os
import platform
import subprocess
import threading
from time import sleep

import pychrome
import requests

from hunters.config import DEFAULT_BROWSER_CONFIG
from hunters.factory import Factory


def default_chrome_bin():
    if platform.system().lower() == "windows":
        return "chrome.exe"
    return "chrome"


def find_chrome_bin(bin_path):
    """
    find chrome bin location from
    the priority is
    env[CHROME_BIN] > bin_path > default_chrome_bin()
    :param bin_path:
    :return:
    """
    return os.getenv("CHROME_BIN", bin_path or default_chrome_bin())


def parse_chrome_option(browser_config, debugging_port=9222, debugging_address="127.0.0.1"):
    """
    parse browser_config to chrome config
    :param browser_config:
    :param debugging_address:9222 default
    :param debugging_port: 127.0.0.1 default
    :return: list
    """
    chrome_flag = [
        # '--headless',
        # '--disable-gpu',
        '--hide-scrollbars',
        '--disable-infobars',
        # '--start-fullscreen',
        '--start-maximized',
        # '--no-sandbox',
        '--window-size={},{}'.format(browser_config.width, browser_config.height),
        '--disable-client-side-phishing-detection',
        '--disable-background-networking',
        '--disable-web-security',
        '--allow-running-insecure-content',
        '--enable-experimental-web-platform-features',

        # r'--load-extension=""',
        # r'--disable-extensions-except=""'
    ]

    if debugging_address:
        chrome_flag.append("--remote-debugging-address={}".format(debugging_address))

    if debugging_port:
        chrome_flag.insert(0, "--remote-debugging-port={}".format(debugging_port))
        chrome_flag.append("--user-data-dir=/data/appdatas/chrome/{}".format(debugging_port))

    if browser_config.headless:
        chrome_flag.insert(0, "--headless")

    if browser_config.user_agent:
        chrome_flag.append("--user-agent=\"{}\"".format(browser_config.user_agent))

    if browser_config.disk_cache_size is not None and browser_config.disk_cache_size > 0:
        chrome_flag.append("--disk-cache-size={}".format(browser_config.disk_cache_size))

    if not browser_config.gpu:
        chrome_flag.insert(2, "--disable-gpu")

    chrome_flag += browser_config.extra_options  #: append extra options by user custom

    return chrome_flag


def open_chrome(port=9222, address="127.0.0.1", browser_config=DEFAULT_BROWSER_CONFIG):
    chrome_flags = parse_chrome_option(debugging_port=port, debugging_address=address, browser_config=browser_config)
    chrome_bin = find_chrome_bin(browser_config.execute_bin)
    chrome_flags.insert(0, chrome_bin)
    item = None
    try:
        item = subprocess.Popen(args=chrome_flags)  #: use list not string to FIX `File name too long`
    except FileNotFoundError as e:
        raise FileNotFoundError("can't found chrome bin, set env CHROME_BIN or use BrowserConfig to config before run")

    def close_subprocess():
        """ 主进程退出的时候自动退出这个Chrome进程 """
        item.kill()

    atexit.register(close_subprocess)
    MAX = 5
    count = 0
    while True:
        try:
            result = requests.get("http://{}:{}/json".format(address, port), timeout=5)
            print("[Hunters] check chrome open {}:{}".format(address, port))
            if result.ok:
                break
        except Exception as e:
            # wait for chrome openning
            sleep(1)
            pass

        count += 1
        if count > MAX:
            raise RuntimeError("Could not connect to chrome http://{}:{} ".format(address, port))

    return item


class ChromeDevToolFactory(Factory):
    """ open multi chrome instance, and bind multi debugging-port"""

    def __init__(self, browser_config, port=9222, address="127.0.0.1"):
        super().__init__(browser_config=browser_config)
        self._config = browser_config
        self._remote_browser_pool = []
        self._browser_process = []
        self._mutex = threading.Lock()
        self._tab_browser = {}
        self._address = address
        self._port = port

    def new_instance(self):
        with self._mutex:
            b_process = open_chrome(port=self._port, address=self._address,
                                    browser_config=self.config())
            self._browser_process.append(b_process)
            browser_ = pychrome.Browser(url="http://{}:{}".format(self._address, self._port))
            self._remote_browser_pool.append(browser_)
            self._port += 1

            tab_ = browser_.list_tab()[0]
            if hasattr(tab_, "start"):
                tab_.start()
            self._tab_browser[tab_.id] = {"browser": browser_, "process": b_process, "tab": tab_}
            return tab_  # return tab_ as a resource

    def destroy(self, obj):
        data_map = self._tab_browser.pop(obj.id)
        obj.stop()
        self.close_process(data_map)

    @classmethod
    def close_process(cls, data_map):
        if data_map:
            data_map.get("process").kill()
            del data_map

    def destroy_all(self, pool_list=None):
        for tab_, item in self._tab_browser.items():
            self.close_process(item)


class ChromeTabDevToolFactory(Factory):
    """ open only a Chrome, use multi tab as resource, when use new_instance
    this factory just open a chrome, and return a new Chrome Tab
    """

    def __init__(self, browser_config, port=9222, address="127.0.0.1"):
        super().__init__(browser_config=browser_config)
        self._address = address
        self._port = port
        self._browser_process = None
        self._init_chrome(browser_config)
        self._browser = pychrome.Browser(url="http://{}:{}".format(self._address, self._port))

    def _init_chrome(self, browser_config):
        if len(browser_config.manual_url) == 0:
            self._browser_process = open_chrome(port=self._port, address=self._address,
                                                browser_config=browser_config)
        else:
            addrs = browser_config.manual_url.split(":")
            self._address = addrs[0]
            self._port = addrs[1]

    def new_instance(self):
        """return a new chrome tab as resource """
        tab = self._browser.new_tab("about:blank")
        if hasattr(tab, "start"):  # [FIX] pychrome 0.2.0 start manual
            tab.start()
        return tab

    def destroy_all(self, pool_list=None):
        try:
            self._browser_process.kill()
        except Exception as e:
            # silent
            print(e)

    def destroy(self, obj):
        obj.stop()
        self._browser.close_tab(obj.id)
