# -*- coding: utf-8 -*-
"""
    kclient.client
    ~~~~~~~~~~~~

    Python wrapper for k-client API.
"""
import os
import requests
import logging
import shutil
from .helper import detect_filename

from requests.exceptions import RequestException


class Client(object):
    ROOT_URL = 'https://client-k.hot.sonydna.com'
    requests = None

    def __init__(self, **kwargs):
        options = ['username', 'token', 'version', 'user-agent']
        for option in options:
            if option in kwargs:
                setattr(self, option, kwargs[option])
            else:
                setattr(self, option, None)
        if self.requests is None:
            self.requests = requests

    def _headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'User-Agent': getattr(self, 'user-agent'),
            'X-API-Version': getattr(self, 'version'),
        }

    def _body(self):
        return {
            'username': getattr(self, 'username'),
            'token': getattr(self, 'token')
        }

    def _post(self, path, params=None):
        # type: (str, dict) -> object
        """POST request.
        :param path:
        :param params:
        """

        url = self.ROOT_URL + path
        json = params or {}
        json.update(self._body())
        json = dict([(k, v) for (k, v) in json.items() if v is not None])
        try:
            r = self.requests.post(url=url, json=json, headers=self._headers())
            json = r.json()
            if r.status_code == 200 and json['status'] == 'OK':
                return json['result']
            else:
                logging.warning("api error. %s" % json)
                return None
        except RequestException as e:
            logging.error(e)
            return None

    def download(self, url, out=None):
        """

        :param url:
        :param out:
        :return:
        """
        if out is None:
            out = detect_filename(url)
        if os.path.exists(path=out):
            return
        res = self.requests.get(url, stream=True, headers=self._headers())
        with open(out, "wb") as fp:
            logging.debug("Downlonad:" + out)
            shutil.copyfileobj(res.raw, fp)

    def unread(self):
        return self._post('/sysinfo/unread')
