#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/8 18:17
# @Author  : chenjw
# @Site    : 
# @File    : httpSimple.py
# @Software: PyCharm Community Edition
# @Desc    :  simple http requests,support chain

import base64
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from ccommon import jsonParse


class HttpSimple:
    method_get = 'get'
    method_post = 'post'

    def __init__(self, url):
        self.url = url
        self.status_code = 200
        self.method = HttpSimple.method_get
        self.data = None
        self.headers = None
        self.basicAuth = None
        self.rsp = None

    def addData(self, data):
        self.data = data
        return self

    def addDataSingle(self, key, value):
        if self.data is None:
            self.data = {}
        if isinstance(key, str) is True:
            self.headers[key] = value
        return self

    def addHeaders(self, headers):
        if isinstance(headers, dict) is True:
            self.headers = headers
        return self

    def addHeadersSingle(self, key, value):
        if self.headers is None:
            self.headers = {}
        if isinstance(key, str) is True:
            self.data[key] = value
        return self

    def addAuth(self, auth=None, user=None, pwd=None):
        if auth is not None:
            self.basicAuth = auth
        if isinstance(user, str) is True and isinstance(pwd, str) is True:
            pwd = str(base64.b64encode(bytes('%s:%s' % (user, pwd), 'utf-8')), 'utf-8')
            self.basicAuth = HTTPBasicAuth(user, pwd)
        return self

    def addStatusCode(self, status_code):
        if isinstance(status_code, int) is True:
            self.status_code = status_code
        return self

    def addMethod(self, method):
        if isinstance(method, str) is True:
            if method.lower() in [HttpSimple.method_get, HttpSimple.method_post]:
                self.method = method.lower()
        return self

    def run(self):
        if self.method == HttpSimple.method_get:
            self.rsp = requests.get(url=self.url, data=self.data, headers=self.headers, auth=self.basicAuth)
        else:
            self.rsp = requests.post(url=self.url, data=self.data, headers=self.headers, auth=self.basicAuth)
        self.checkStatus()
        return self

    def checkStatus(self):
        self._checkRsp()
        if self.rsp.status_code != self.status_code:
            raise Exception('[HttpSimple] call url(%s) by method(%s) but status_code is %s' % (
                self.url, self.method, self.rsp.status_code))

    def _checkRsp(self):
        if self.rsp is None:
            raise Exception('[HttpSimple] please call function run() at first')

    def retRspHeaders(self):
        self._checkRsp()
        return self.rsp.headers

    def retReqHeaders(self):
        self._checkRsp()
        return self.rsp.request.headers

    def retJson(self):
        self._checkRsp()
        return jsonParse.JsonParse(self.rsp.json())

    def retText(self):
        self._checkRsp()
        return self.rsp.text

    def retSoup(self):
        self._checkRsp()
        return BeautifulSoup(self.rsp.text, 'html.parser')


if __name__ == '__main__':
    # demo
    HttpSimple('url'). \
        addData({'a': 'a', 'b': 'b'}). \
        addDataSingle('c', 'c'). \
        addHeaders({'cookie': 'aaa'}). \
        addHeadersSingle('host', 'aaa.com'). \
        addMethod(HttpSimple.method_get). \
        run(). \
        retText()
    pass
