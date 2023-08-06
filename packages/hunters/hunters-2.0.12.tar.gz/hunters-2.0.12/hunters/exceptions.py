# -*- coding:utf-8 -*-
# Created by qinwei on 2017/9/11
import logging

from urllib3.exceptions import ReadTimeoutError

logger = logging.getLogger("hunters.exception")


class OverLimitErr(Exception):
    """ Add Url Over limit """


class SpiderExceptionListener(object):
    """
    总的Exception控制器
    """

    def __init__(self):
        self._exception_handler = []
        self.init_exception()

    def init_exception(self):
        def show_exception(ex, input_param, position):
            msg = "{}, {}, {}".format(ex, input_param, position)
            if isinstance(ex, ReadTimeoutError):
                logger.warning("{} {}".format("ReadTimeoutError", msg))
            else:
                logger.exception(msg)

        self.add_listener(show_exception)

    def add_listener(self, ex):
        """ add a exception listener


        :param ex: def handler(ex, input_param, position)
        :return:
        """
        if not callable(ex):
            raise ValueError("{} not callable")
        self._exception_handler.append(ex)

    def handle_exception(self, ex, input_params, pos):
        for handler in self._exception_handler:
            handler(ex, input_params, pos)


spider_exception_listener = SpiderExceptionListener()
