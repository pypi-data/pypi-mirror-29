# -*- coding:utf-8 -*-
# Created by qinwei on 2017/12/19
#
import atexit
import logging
import os
import socket
from time import time


class SocketUtils:
    @classmethod
    def find_random_port(cls):
        """return a random free port"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    @classmethod
    def find_free_port(cls, base_port, socket_path):
        """start base_port to lookup a free port"""
        while base_port < 60000:
            if cls.is_open(ip="127.0.0.1", port=base_port):
                base_port += 1
            else:
                try:
                    cls.__check_socket("{}/{}".format(socket_path, base_port))
                    return base_port
                except FileExistsError as e:
                    base_port += 1

    @classmethod
    def __check_socket(cls, socket_file):
        """ use a file to check deny multi process open same port """
        if os.path.exists(socket_file) and time() - os.stat(socket_file).st_mtime < 10:
            # file exits and last access less then 10s
            raise FileExistsError("socket exists")

        with open(socket_file, mode="w") as file:
            file.write(str(os.getpid()))
        atexit.register(cls.__remove_file, socket_file)

    @classmethod
    def __remove_file(cls, socket_file):
        try:
            print("DELETE {}".format(socket_file))
            os.remove(socket_file)
        except Exception as e:
            logging.error(e)

    @staticmethod
    def is_open(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            # 利用shutdown()函数使socket双向数据传输变为单向数据传输。shutdown()需要一个单独的参数，
            # 该参数表示了如何关闭socket。具体为：0表示禁止将来读；1表示禁止将来写；2表示禁止将来读和写。
            s.close()
            return True
        except:
            return False
