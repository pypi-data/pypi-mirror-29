# -*- coding:utf-8 -*-
# Created by qinwei on 2018/2/26
#

# 根据interval秒数重复执行的定时器
# @setInterval(3, daemon=False)
# def show():
#    print("heelo")
#
# stop = show() # running ...
# print("ll")
# stop.set() # stopping ...
#
import threading


def setInterval(interval, daemon=False):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():  # executed in another thread
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = daemon  # stop if the program exits
            t.start()
            return stopped

        return wrapper

    return decorator
