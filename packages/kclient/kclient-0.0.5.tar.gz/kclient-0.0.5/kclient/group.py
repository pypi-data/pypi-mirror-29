# -*- coding: utf-8 -*-
"""
    kclient.subscribe
    ~~~~~~~~~~

    Python wrapper for k-client Group API.
"""
from .client import Client
from .enums import Groups


class Group(Client):
    def info(self, group=Groups.KEYAKIZAKA):
        """

        :return:
        """
        param = {
            "group": group.value
        }
        return self._post('/group/info', param)