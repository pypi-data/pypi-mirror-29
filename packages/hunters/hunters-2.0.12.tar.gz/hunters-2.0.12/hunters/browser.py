# -*- coding:utf-8 -*-
# Created by qinwei on 2017/8/7

##############################################################################
import base64
import codecs
import logging
import os
import queue
import threading
import weakref
from base64 import b64decode
from http.cookiejar import split_header_words
from parser import ParserError
from time import sleep, time
from urllib import parse

import pychrome
import requests
from requests import Response
from requests.exceptions import TooManyRedirects, SSLError
from requests.structures import CaseInsensitiveDict

from hunters.benchmark import BenchMark
from hunters.config import DEFAULT_BROWSER_CONFIG
from hunters.constant import Regex
from hunters.util.file_util import FileUtils
from hunters.util.socket_util import SocketUtils
from hunters.utils import StringUtil, ResponseUtils, remove_xml_encoding, dom

logger = logging.getLogger("hunters.browser")


class Browser(object):
    """ Define Browser uniform Abstract API """

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def get(self, url, **kwargs):
        """

        :param url:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def post(self, url, data, json, **kwargs):
        """

        :param url:
        :param data:
        :param json:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def head(self, url, **kwargs):
        raise NotImplementedError

    def screenshot_as_png(self, filename, full_page=False):
        """

        :param filename:
        :param full_page:
        :return:
        """
        raise NotImplementedError

    def window_size(self, width, height):
        """
        resize window size

        :param width:
        :param height:
        :return:
        """
        raise NotImplementedError

    def scroll_by(self, x, y):
        """

        :param x:
        :param y:
        :return:
        """
        raise NotImplementedError

    def wait(self, num):
        """

        :param num:
        :return:
        """
        raise NotImplementedError

    def execute_js(self, js_str):
        """

        :param js_str:
        :return:
        """
        raise NotImplementedError

    def cookies(self, urls):
        """
        Cookie相关操作接口

        :param urls: 传递一个host或者url列表来获取对应的cookie, 具体由子类实现
        :return: 返回cookies (dict或list)
        """
        raise NotImplementedError

    def close(self):
        """ 关闭当前窗口, 通常如果是Selenium实现的, 可能关闭的是浏览器 """
        raise NotImplementedError

    def quit(self):
        """ 完全关闭进程, 通常如果是Selenium, 关闭浏览器和webdriver """
        raise NotImplementedError

    def browser_config(self):
        raise NotImplementedError

    def set_block_urls(self, urls):
        """
        block url to load

        :param urls: list, ["*.png", ".jpeg"]
        :return:
        """
        raise NotImplementedError

    def limit_page_size(self, per_size, total_size):
        """
        limit page size

        :param per_size:
        :param total_size:
        :return:
        """
        raise NotImplementedError

    def disable_image(self, bool_):
        """

        :param bool_:
        :return:
        """
        raise NotImplementedError

    @staticmethod
    def parse_url(url):
        """
        ParseResult(scheme='https', netloc='fex.bdstatic.com', path='/hunter/alog/dp.csp.min.js', params='', query='v=140804', fragment='')

        :param url:
        :return:
        """
        return parse.urlparse(url)

    @staticmethod
    def get_host(url):
        return parse.urlparse(url).netloc


class MiniBrowser(Browser):
    """
    文本型/单请求/微浏览器实现,
    基于requests,
    requests, Cookie自动保持, URL跳转自动跟随, 自动解析文本decode, 都是浏览器必有特性
    decode比较弱, 自己重新实现了一个, 更能准确判断gbk和utf8
    """

    def __init__(self, browser_config=DEFAULT_BROWSER_CONFIG):
        # self.session.mount("data:", DataAdapter) TOTO
        self._browser_config = browser_config

    @property
    def session(self):
        # XXX 解决同一个session长期复用会导致内存一致涨的问题
        session = requests.session()
        session.headers['User-Agent'] = self._browser_config.user_agent
        session.max_redirects = self._browser_config.max_redirects
        return session

    @property
    def cookie_store(self):
        return self.browser_config().cookie_store

    def browser_config(self):
        return self._browser_config

    def head(self, url, **kwargs):
        try:
            kwargs.setdefault("timeout", 2)  # head 请求如果2秒没啥返回, 说明拒绝head或者访问失败了
            assert url.startswith("http"), "HEAD only support http or https"
            return Tab(self, self.session.head(url, **kwargs))
        except Exception as e:
            logger.error("url[%s], msg[%s]" % (url, e))
            r = Response()
            r.headers = {}
            r.url = url
            r.status_code = 503  #: 服务无法访问
            return r

    def cookies_str(self, host):
        cookies_dict = self.cookies(host)
        result = ""

        for (k, v) in cookies_dict.items():
            result += "%s=%s; " % (StringUtil.replace_blank(k), StringUtil.replace_blank(v))

        return result

    def cookies(self, host):
        """从会话中拿出cookie"""
        return self.cookie_store.get(host) or {}

    def _mrg_cookies(self, host, cookies):
        """
        合并cookies
        :param cookies: list[tuple] or dict or "A=1; B=3"
        :return:
        """
        last_cookies = self.cookies(host)
        if isinstance(cookies, dict):
            last_cookies.update(cookies)
        else:
            if isinstance(cookies, str):
                #: split word ["A=1"] ==> [[(A, 1)]]
                cookies = split_header_words([cookies])[0]

            for item in cookies:
                last_cookies.update({item[0]: item[1]})

        self.cookie_store.set(host, last_cookies)
        return last_cookies

    def _set_header_cookie(self, host, **kwargs):

        headers = kwargs.get("headers", {})
        user_cookie = headers.get("Cookie")  #: 用户自己配置Cookie的情况下, 合并
        if user_cookie:
            self._mrg_cookies(host, user_cookie)
        headers.update({'Cookie': self.cookies_str(host)})
        kwargs.setdefault("headers", headers)
        return kwargs

    def _check_cookies(self, host, response, cookie_dict=None):
        if "Set-Cookie" in response.headers:
            self._mrg_cookies(host, cookie_dict)  #: 合并到会话级别, cookies中

    def get(self, url, **kwargs):
        b = BenchMark(__name__)
        try:
            # extract_cookies_to_jar(self.session.cookies, req, urllib3.HTTPResponse())
            host = self.get_host(url)
            kwargs = self._set_header_cookie(host, **kwargs)
            kwargs.setdefault("stream", True)  #: lazyLoad , 避免读取大文件
            with self.session as session:
                try:
                    r = session.get(url, **kwargs)
                except SSLError as err:  # 这里可能会报Https鉴权错误
                    kwargs.setdefault("verify", False)
                    r = session.get(url, **kwargs)
                    setattr(r, "SSLError", True)  # 配置一个标记说明存在鉴权, 让后续者鉴定错误
                    logger.warning("SSLError, url[%s], err[%s]", url, err)

                self._check_cookies(host, r, session.cookies.items())

                self._check_body_size(response=r)

            return Tab(self, self.__detect_encoding(r))

        except TooManyRedirects as err:
            r = ResponseUtils.too_many_redirects_response(err)
            r.ori_url = url
            logging.warning("TooManyRedirects:[{}]".format(url))
            return Tab(self, r)
        except Exception as e:
            #: 如果是requests都无法访问, 说明连接不可用.
            r = ResponseUtils.exception_response(e)
            # connection error just warning and return a exception response
            logger.warning("connect url:[{}] ,error[{}]".format(url, e))
            r.ori_url = url
            return Tab(self, r)
        finally:
            b.mark("OK")

    def _check_body_size(self, response):
        """ 检测内容是否超标 """
        max_body_size = self.browser_config().max_body_size
        ResponseUtils.handle_chunked_body(response=response, max_size=max_body_size)
        if ResponseUtils.is_body_over_size(response=response, max_size=max_body_size):
            logger.debug("over size limit:{} > {}".format(response.url, max_body_size))
            response.close()

    def post(self, url, data=None, json=None, **kwargs):
        host = self.get_host(url)
        self._set_header_cookie(host, **kwargs)
        with self.session as session:
            r = self.session.post(url, data, json, **kwargs)
            self._check_cookies(host, r, session.cookies.items())
        return Tab(self, self.__detect_encoding(r))

    def screenshot_as_png(self, filename, full_page=False):
        raise NotImplementedError("IGNORE screenshot_as_png for textBrowser")

    def window_size(self, width, height):
        raise NotImplementedError("IGNORE window_size for textBrowser")

    def scroll_by(self, x, y):
        raise NotImplementedError("IGNORE scroll_by for textBrowser")

    def wait(self, num):
        raise NotImplementedError("IGNORE scroll_by for textBrowser")

    def execute_js(self, js_str):
        raise NotImplementedError("IGNORE execute_js for textBrowser")

    @staticmethod
    def __detect_encoding(response):
        """ 尝试检测页面编码 """
        #: 'text/html; charset=GB2312'
        #: 'application/json'
        content_type = response.headers.get("Content-Type", "error/no-content-type")
        if not Regex.RE_TYPE_PLAIN.search(content_type):
            #: 必须是文本类型才能检测, 二进制的忽略
            return response

        before_encoding = response.encoding  #: 'ISO-8859-1'
        detect_encoding = None

        #: 有的网站不按常理出牌, 返回content-type是charset=gbk,但是内容meta是utf8,比如QQ某个网站
        #: 但是调试发现浏览器有优先级, 如果返回头返回了编码, 以返回头为准, 否则看页面的meta[charset]值
        #: FIX 优先级UTF8-BOM最高
        match = Regex.RE_CONTENT_TYPE_CHARSET.search(content_type)
        if response.content is not None and response.content[0:3] == codecs.BOM_UTF8:
            detect_encoding = "UTF-8"
        elif match:
            detect_encoding = match.group(1)
        elif Regex.RE_TYPE_HTML.search(content_type):
            match = Regex.RE_MATA_CHARSET.search(response.text)
            if match:
                detect_encoding = match.group(1)  # 解决乱码问题

        #: 如果都没有编码信息, 就探测编码
        if detect_encoding is None and before_encoding in (
                None, 'ISO-8859-1'):  #: 'ISO-8859-1' 编码特别不准. 至少GBK, UTF-8也兼容他
            detect_encoding = response.apparent_encoding  #: 检测编码

        if detect_encoding is None:
            detect_encoding = "UTF-8"
        #: GB18030 (7W字) > GBK (2W字) > BIG5(繁体) > GB2312 (6K字)
        #: 如果检测出使用GB2312 , 有超出范围的罕见字符会有乱码, 改成兼容性更强的GBK
        if detect_encoding.upper() == "GB2312":
            detect_encoding = "GBK"

        response.encoding = detect_encoding
        logging.debug("DETECT ENCODING, url[%s], encoding[%s], before[%s]", response.url, response.encoding,
                      before_encoding)
        return response


##################################### ViewBrowser ##################################################

class BaseChrome(Browser):
    """ Chrome implement , base on DevTools Protocol, use DevTools(Remote-Debugging) directly, no WebDriver  """

    def __init__(self, factory):
        """
        :param factory:  devtool factory
        """
        self._browser_config = factory.config()
        self._minibrowser = MiniBrowser(self._browser_config)
        self.local_store = self._browser_config.local_store
        self._last_done = True
        self._query_done = queue.Queue(1)
        self._factory = factory
        self._response_received_queue = queue.Queue()
        self._listen_count = False
        self.api = factory.new_instance()
        self._max_total_size = self.browser_config().max_body_size * 5
        self._init()

    def _init(self):

        self.Page.enable()
        self.DOM.enable()
        self.Network.enable()
        try:
            # This method is EXPERIMENTAL
            self.api.Page.setDownloadBehavior(behavior="allow", downloadPath=self.local_store)

            if self.browser_config().max_body_size > 0:
                self.api.Network.setDataSizeLimitsForTest(maxTotalSize=self._max_total_size,
                                                          maxResourceSize=self.browser_config().max_body_size)

            def response(**kwargs):
                if self._listen_count > 0:
                    self._response_received_queue.put(kwargs)
                    self._listen_count -= 1
                else:
                    logger.debug("ignore {}", kwargs)

            self.api.Network.responseReceived = response

        except Exception as e:
            logger.warning(str(e))

        self.Page.loadEventFired = self.__event_page_load

    def browser_config(self):
        return self._browser_config

    @property
    def text(self):
        data = self.DOM.getDocument()
        node_id = data.get("root").get("nodeId")
        result_dict = self.DOM.getOuterHTML(nodeId=node_id)
        return result_dict.get("outerHTML")

    def get(self, url, **kwargs):
        """
        Because Connect to Chrome base on WebSocket, so when we send "Page.navigate" command to browser,
        we should be listening `PageLoadedFired` Event to known whether the all page load done

        :param url:
        :param kwargs:
        :return: Response
        """
        b = BenchMark("chrome-get")
        while not self._last_done:
            # block to wait for last query done
            sleep(0.01)

        self._last_done = False

        # 某些网站卡在https验证部分都没有发请求
        _timeout = kwargs.get("timeout", 3)
        _headers = kwargs.get("headers", {})
        _referer = _headers.get("Referer")
        _cookies = _headers.get("Cookies")
        # TODO cookie headers
        response = self._minibrowser.get(url, **kwargs)
        if "error" not in response.headers.get("content-type"):
            try:
                # for open or query timeout
                self.Page.navigate(url=url, referer=_referer, _timeout=_timeout)

                # for page load timeout
                self._query_done.get(block=True, timeout=_timeout)
                response.status_code = 200

            except (queue.Empty, pychrome.exceptions.TimeoutException) as e:
                # force browser stop
                self._last_done = True
                response.status_code = -5404
                response.reason = "timeout"
                logger.info("STOP LOADING [{}]".format(url))
                self.api.Page.stopLoading()

        response.url = self.url or url  # current page
        b.ok()
        tab = Tab(weakref.ref(self)(), weakref.ref(response)())
        setattr(tab, "headless", True)
        return tab

    @property
    def url(self):
        url = self.execute_js("location.href")
        if url.startswith("chrome-error"):
            return None
        return url

    def wait(self, num):
        sleep(num)
        return self

    def post(self, url, data, json, **kwargs):
        raise NotImplemented("Not Support POST method")

    def close(self):
        return self

    def scroll_by(self, x, y):
        """ scroll the scroll bar, to trigger some async page load"""
        return self.execute_js("window.scrollBy({}, {})".format(x, y))

    def head(self, url, **kwargs):
        return self._minibrowser.head(url, **kwargs)

    def execute_js(self, js_str):
        """
        :param js_str: js expression
        :return: the js expression return (maybe u should specify "return document.title"
        """
        b = BenchMark("execute_js")
        try:
            result = self.api.Runtime.evaluate(expression=js_str)
            return result.get("result").get("value", None)
        finally:
            b.ok()

    def screenshot_as_png(self, filename=None, full_page=False):
        """
        screen_shot current page

        :param filename: filename (string) to  write to
        :param full_page:
        :return: return bytes when no filename specify
        """
        b = BenchMark("screenshot_as_png")
        if full_page:
            self._resize_to_model_height("html")
        try:
            result = self.api.Page.captureScreenshot(format="png", fromSurface=True, fullPage=True)
            base64 = result.get('data', "")
            image_bytes_ = b64decode(base64)

            if filename:
                filename = os.path.join(self._browser_config.local_store, filename)
                if filename.startswith(self._browser_config.local_store) and "../" not in filename:
                    with open(filename, "wb+") as f:
                        f.write(image_bytes_)
                else:
                    raise PermissionError("deny to write outside %s" % self.local_store)

            return image_bytes_
        finally:
            self.api.Emulation.clearDeviceMetricsOverride()  # reset window size
            b.mark("ok")

    def _resize_to_model_height(self, selector):
        """

        :param selector: CSS Selector
        :return:
        """
        data = self.api.DOM.getDocument()
        node_id = data.get("root").get("nodeId")
        result = self.api.DOM.querySelector(selector=selector, nodeId=node_id)
        # result = {'model': {'content': [0, 0, 1280, 0, 1280, 5527, 0, 5527],
        # 'padding': [0, 0, 1280, 0, 1280, 5527, 0, 5527],
        # 'border': [0, 0, 1280, 0, 1280, 5527, 0, 5527],
        # 'margin': [0, 0, 1280, 0, 1280, 5527, 0, 5527],
        # 'width': 1280, 'height': 5527}}
        if "nodeId" in result:
            result = self.api.DOM.getBoxModel(nodeId=result.get("nodeId"))
            model = result.get("model")
            self.window_size(self.browser_config().width, model.get("height") + 100)

    def window_size(self, width, height):
        """ change current page size by Chrome Emulation """
        self.api.Emulation.setDeviceMetricsOverride(width=width, height=height, deviceScaleFactor=1,
                                                    screenWidth=width, screenHeight=height,
                                                    mobile=False, fitWindow=False)
        self.api.Emulation.setVisibleSize(width=width, height=height)
        self.api.Emulation.setPageScaleFactor(pageScaleFactor=1)
        return self

    def disable_image(self, bool_):
        """

        :NOTE: If use  Tab pool return a tab as a resource,
        remember to reset all behavior to protect Resource Pollution when user change the tab behavior.
        Because the pool return a blocked tab in the next time, maybe not expected
        """
        if bool_:
            # block by some url suffix
            self.set_block_urls(urls=[
                ".jpg", ".png", ".ico", ".gif", ".jpeg", "img="
                , "=png", "=jpg", "=jpeg", "=gif"])
        else:
            self.set_block_urls(urls=[])

    def limit_page_size(self, per_size, total_size):
        """
        Be careful to reset all behavior if necessary

        :param per_size: bytes
        :param total_size: bytes
        :return:
        """
        if per_size > 0 and total_size > 0:
            self.api.Network.setDataSizeLimitsForTest(maxTotalSize=total_size, maxResourceSize=per_size)

    def set_block_urls(self, urls):
        self.api.Network.setBlockedURLs(urls=urls)
        return self

    def quit(self):
        """ Close Chrome , Stop WebSocket """
        self.api.Browser.close()  # some chrome version not this method
        self.api.stop()

    def cookies(self, urls):
        """
        :param urls: url list , or domain list
        :return: cookies [{name: "", value:"", url:"", domain:"" ...}]
        """
        result = self.Network.getCookies(urls=urls)
        return result.get("cookies")

    def get_all_cookies(self):
        """ return a list for all cookie """
        result = self.Network.getAllCookies()
        return result.get("cookies")

    def delete_cookies(self, name, **kwargs):
        """
        :param name: cookie name
        :param kwargs:  (like string url, domain, path)
        :return:
        """
        kwargs.setdefault("name", name)
        self.api.Network.delete_cookies(**kwargs)
        return self

    def set_cookies(self, cookies):
        """
        :param cookies: [{name:"key", value:"value", url:"option", "domain": "option" }]
        :return:
        """
        self.api.Network.setCookies(cookies=cookies)
        return self

    def __event_page_load(self, **kwargs):
        """
        Page Loader Event Listener,
        emit when Chrome Page Load (all ajax, and DOM change done)

        :param kwargs:
        :return:
        """
        self._last_done = True
        self._query_done.put(time())

    def __getattr__(self, item):
        """
        Proxy Chrome DevTools Method , When Attribute is uppercase start ,
        such as self.Page.enable() bind to self.api
        """
        if item[0].isupper():
            return getattr(self.api, item)

        raise AttributeError(item)

    def listen_response(self, max_count=100):
        self._listen_count = max_count

    def list_response(self):
        """

        :return:
        """
        result = []
        # not use yield and iter because we should remove all response in
        try:
            # get all item in queue, to clear it
            while True:
                # just wait a little time
                # chrome will load new Network by js or setTimeout/setInterval
                # discard it
                item = self._response_received_queue.get(timeout=0.5)
                result.append(ChromeResponse(weakref.ref(self)(), item))

        except queue.Empty as e:
            pass

        return result


class ChromeResponse(Response):
    def __init__(self, chrome, received):
        super().__init__()
        self.request_id = received.get("requestId")
        self._response = received.get("response")
        self.headers = CaseInsensitiveDict(data=self._response.get("headers"))
        self._type = received.get("type")
        self.url = self._response.get("url")
        self.status_code = self._response.get("status")
        self.reason = self._response.get("statusText")
        self._browser = chrome

    @property
    def type(self):
        return self._type.lower()

    @property
    def text(self):
        #  {"body":"",  "base64Encoded": True/False }
        return self.content.decode()

    @property
    def content(self):
        try:
            result = self._browser.Network.getResponseBody(requestId=self.request_id)
            if result.get("base64Encoded"):
                return base64.b64decode(result.get("body"))
            return bytes(result.get("body"), encoding="utf-8")
        except Exception as e:
            print(e)
            return None


class Chrome(BaseChrome):
    """
    Multi Chrome Process
    Every Chrome Instance is create a new Chrome Process and return a Tab
    """
    factory = None

    def __init__(self, browser_config):
        if Chrome.factory is None:
            from hunters.chrome import ChromeDevToolFactory
            free_port = SocketUtils.find_free_port(base_port=9222, socket_path=browser_config.local_store)
            Chrome.factory = ChromeDevToolFactory(port=free_port, browser_config=browser_config)

        super().__init__(factory=Chrome.factory)


class ChromeTab(BaseChrome):
    """
    One Chrome Process, open Multi Tab
    """

    # Share the factory for all ChromeTab Instance,
    # In order to use a single Chrome Browser,
    # In this case, every ChromeTab instance is bind to a Chrome Tab
    factory = None

    def __init__(self, browser_config):
        if ChromeTab.factory is None:
            from hunters.chrome import ChromeTabDevToolFactory
            free_port = SocketUtils.find_free_port(base_port=9222, socket_path=browser_config.local_store)
            ChromeTab.factory = ChromeTabDevToolFactory(port=free_port,
                                                        browser_config=browser_config)
        else:
            logger.warning("ChromeTab.factory has already set before. the Tab type will only use one Chrome Instance")

        super().__init__(factory=ChromeTab.factory)


class ViewBrowser(ChromeTab):
    """The View Browser is extend by ChromeTab
    Every New ViewBrowser Instance will create a new Tab in backend Chrome
    The browserConfig will share in all Tab
    """

    def __init__(self, browser_config):
        super().__init__(browser_config=browser_config)


###########################################################
class Tab(Browser):
    """
    Tab是网页标签, 比较特殊的东西, 不知道取什么名字, 就叫tab(标签)类似浏览器标签
    有浏览器的特性(可以继续发起请求), 也有结果的特性(从页面获取值)
    Proxy Browser/Response Method
    Friendly TO IDE code autocomplete,
    some method not use __getattr__
    """

    def __init__(self, browser, response):
        self._browser = browser
        self._response = response
        self.local_store = browser.browser_config().local_store
        self._thread_local = threading.local()
        # self.__dict__.update(response.__dict__)  #: 拷贝结果集的属性到tab
        self._dom = None

    def dom(self):
        # 解析结构化结构, DOM(方便CSS方式选择)
        # 这里会牺牲一定性能来保证API的简洁
        if self._dom is None and Regex.RE_TYPE_HTML.search(self.headers.get("Content-Type")):
            text = self.text or ""
            if "" == text.strip():
                text = "<html></html>"
            try:
                self._dom = dom(remove_xml_encoding(text))  # cssselect
            except ParserError as e:
                logger.error("DOMError, url[%s], msg[%s], content:[%s]", self.url, e, text)
                self._dom = dom("<html></html>")

        if self._dom is None:
            logger.warning("DOM NONE! %s %s", self.url, self.text)
            self._dom = dom("<html></html>")
        return self._dom

    @property
    def text(self):
        if hasattr(self, "headless"):
            return self._browser.text
        return self._response.text

    @property
    def title(self):
        if "html" in self.headers.get("content-type", ""):
            #: 只有当前访问页面是HTML的类型才尝试获取 title
            els = self.dom().cssselect('title')
            return els[0].text if els and len(els) > 0 else ""
        return ""

    def user_dir(self, path):
        return os.path.join(self.local_store, path)

    def tmp_file(self, prefix="", suffix="", dirname=None, new=True):
        """
        create a new tmp file in user_dir
        such as in browser local store


        :param mode: open mode "w+b"
        :param prefix: tmp file prefix name
        :param suffix: tmp file suffix , such as ".png"
        :param dirname:
        :param new: [True] create a new temp file in  every call, otherwise bind to thread local
                    if False , it will return a file bind to current thread, different thread will hold
                    the different file. To avoiding multi thread write a same file
        :return: A temp open file

        :NOTE: CLOSE file will not Remove the temp File
        """
        if new:
            tmp_name = self.__temp_file(prefix=prefix, suffix=suffix, dirname=dirname)
            return self.user_dir(tmp_name)

        if not hasattr(self._thread_local, "tmp_file"):
            tmp_name = self.__temp_file(prefix=prefix, suffix=suffix, dirname=dirname)
            self._thread_local["tmp_file"] = self.user_dir(tmp_name)

        return self._thread_local.get("tmp_file")

    @staticmethod
    def __temp_file(prefix="", suffix="", dirname=""):
        tmp_name = FileUtils.create_tmp_file_name(prefix=prefix, suffix=suffix)
        if dirname is not None:
            tmp_name = "{}/{}".format(dirname, tmp_name)
        return tmp_name

    def scroll_by(self, x, y):
        self._browser.scroll_by(x, y)

    def execute_js(self, js_str):
        self._browser.execute_js(js_str)

    def get(self, url, **kwargs):
        self._browser.get(url, **kwargs)

    def window_size(self, width, height):
        self._browser.window_size(width, height)

    def close(self):
        self._browser.close()

    def screenshot_as_png(self, filename, full_page=False):
        self._browser.screenshot_as_png(filename, full_page)

    def quit(self):
        self._browser.quit()

    def wait(self, num):
        self._browser.wait(num)

    def __str__(self):
        return "<Tab[{}],[{}]>".format(self.url, self.status_code)

    @property
    def content(self):
        return self._response.content

    def json(self):
        return self._response.json()

    @property
    def encoding(self):
        return self._response.encoding

    @encoding.setter
    def encoding(self, charset):
        self._response.encoding = charset

    def __getattr__(self, item):
        if hasattr(self._browser, item):
            return getattr(self._browser, item)
        return getattr(self._response, item)
