# -*- coding:utf-8 -*-
# Created by qinwei on 2017/12/7
#
import threading
import uuid
from time import time


class FileUtils:
    @staticmethod
    def create_tmp_file_name(prefix="", suffix=""):
        """
        create a new temp file name
        :param prefix:
        :param suffix:
        :return:
        """
        name = "{}{}-{}".format(int(time()), threading.current_thread().ident, uuid.uuid4().hex[:8])
        file_name = "{prefix}{name}{suffix}".format(prefix=prefix, name=name, suffix=suffix)
        return file_name
