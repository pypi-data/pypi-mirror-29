# -*- coding: utf-8 -*-
"""
    kclient.article
    ~~~~~~~~~~

    Python wrapper for k-client Article API.
"""
from .enums import Groups
from .client import Client


class Article(Client):
    def count(self, group=Groups.KEYAKIZAKA):
        """
        :return:
        """
        param = {
            "group": group.value
        }
        return self._post('/article/count', param)

    def get(self, contents):
        """
        :param contents: contents id
        :return:
        """
        return self._post('/article', {'article': contents})

    def allhistory(self, group=Groups.KEYAKIZAKA, count=100, fromdate=None, sortorder=0, letter=False):
        """
        :param group:
        :param count:
        :param fromdate:
        :param sortorder: 0: ascending order, 1: descending order
        :param letter: include letter.
        :return:
        """
        param = {
            "count": count,
            "fromdate": fromdate,
            "group": group.value,
            "sortorder": sortorder
        }

        allhistory = self._post('/article/allhistory', param)
        if not letter:
            allhistory['history'] = filter(lambda h: not 'letter' in h['body'], allhistory['history'])
        return allhistory