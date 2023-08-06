#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/8 18:17
# @Author  : chenjw
# @Site    : 
# @File    : httpSimple.py
# @Software: PyCharm Community Edition
# @Desc    :  do what

from requests.auth import HTTPBasicAuth
import base64
import requests
from ccommon import jsonParse
from bs4 import BeautifulSoup


class HttpSimple():
    def __init__(self, url):
        self.url = url
        self.data = None
        self.headers = None
        self.status_code = 200
        self.basicAuth = None
        self.method = 'get'
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
            if method.lower() in ['get', 'post']:
                self.method = method.lower()
        return self

    def run(self):
        if self.method == 'get':
            self.rsp = requests.get(url=self.url, data=self.data, headers=self.headers,auth=self.basicAuth)
        else:
            self.rsp = requests.post(url=self.url, data=self.data, headers=self.headers,auth=self.basicAuth)
        self.checkStatus()
        return self

    def checkStatus(self):
        if self.rsp.status_code != self.status_code:
            raise Exception('[HttpSimple] call url(%s) by method(%s) but status_code is %s' % (
                self.url, self.method, self.rsp.status_code))

    def retJson(self):
        return jsonParse.JsonParse(self.rsp.json())

    def retText(self):
        return self.rsp.text

    def retSoup(self):
        return BeautifulSoup(self.rsp.text, 'html.parser')


if __name__ == '__main__':
    pass
