# -*- coding: utf-8 -*-
"""
    kclient.subscribe
    ~~~~~~~~~~

    Python wrapper for k-client Subscribe API.
"""
from .client import Client
from .enums import Groups


class Subscribe(Client):
    def list(self):
        """
        :return:
        """
        return self._post('/subscribe/list')