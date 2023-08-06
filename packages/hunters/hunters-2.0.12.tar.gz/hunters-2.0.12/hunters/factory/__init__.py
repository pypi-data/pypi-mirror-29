# -*- coding:utf-8 -*-
# Created by qinwei on 2017/11/29
#
import abc

from hunters.config import DEFAULT_BROWSER_CONFIG


class Factory:
    """实例工厂, 负责创建实例, 并且也负责销毁, 谁创建谁知道怎么销毁"""

    def __init__(self, browser_config=DEFAULT_BROWSER_CONFIG):
        self._config = browser_config

    @abc.abstractmethod
    def new_instance(self):
        """
        创建新的实例
        """

    @abc.abstractmethod
    def destroy(self, obj):
        """
        Factory让你决定如何创建和如何销毁,
        :param obj:
        :return:
        """

    @abc.abstractmethod
    def destroy_all(self, pool_list=None):
        """
         完全销毁所有实例
        :param pool_list: all resource pool data which is the `new_instance` method create
        :return:
        """

    def config(self):
        """
        return the config for use create instance if has
        :return:
        """
        return self._config
