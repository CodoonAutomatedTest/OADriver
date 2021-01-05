#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 上午11:18
# @File    : oadriver.py
import requests
import os, execjs
from oadriver.remote.webelement import WebElement

_current_path = os.path.abspath(os.path.dirname(__file__))
_root_path = os.path.dirname(_current_path)
_encrypt_js_path = _root_path + '/libs/encrypt.js'


class Webdriver(object):
    # _web_element_cls = WebElement

    @classmethod
    def get_remote_connection_body(cls, username, password):
        sign_js = cls._load_sign_js(cls._get_js(_encrypt_js_path))
        ops = sign_js.call('encrypt', password)
        parmas = {
            'data[Login][ref]': 'https://www.tapd.cn/my_worktable',
            'data[Login][encrypt_key]': ops['key'],
            'data[Login][encrypt_iv]': ops['iv'],
            'data[Login][site]': 'TAPD',
            'data[Login][via]': 'encrypt_password',
            'data[Login][email]': username,
            'data[Login][password]': ops['pass'],
            'data[Login][login]': 'login'
        }
        return parmas

    @classmethod
    def get_remote_connection_headers(cls):
        """
        Get headers for remote request.

        :Args:
         - parsed_url - The parsed url
         - keep_alive (Boolean) - Is this a keep-alive connection (default: False)
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
            'Connection': 'keep-alive'
        }

        return headers

    def __init__(self, remote_server_addr, username, password):
        self._url = remote_server_addr
        self._login(remote_server_addr, username, password)

    def get(self, url, body=None):
        response = self._conn.get(url=url, data=body, headers=self.get_remote_connection_headers())
        if response.status_code == 200:
            return response
        else:
            raise Exception('invalid http request')

    def post(self, url, body=None):
        response = self._conn.post(url=url, data=body, headers=self.get_remote_connection_headers())
        if response.status_code == 200:
            return response
        else:
            raise Exception('invalid http request')

    # def create_web_element(self, response, features='html.parser'):
    #     """Creates a web element with the specified `element_id`."""
    #     return self._web_element_cls(response, features)

    def _login(self, url, username, password):
        headers = self.get_remote_connection_headers()
        body = self.get_remote_connection_body(username, password)
        self._conn = requests.Session()
        resp = self._conn.post(url=url, data=body, headers=headers)
        data = resp.text.encode('utf-8').decode('UTF-8')
        if resp.status_code == 200:
            return  {'status': resp.status_code, 'value': data}
        else:
            raise Exception('login faild! try agin later...')

    def _get_js(path):
        with open(path) as f:
            line = f.readline()
            html_str = ''
            while line:
                html_str = html_str + line
                line = f.readline()
            return html_str

    def _load_sign_js(js_str):
        return execjs.compile(js_str)
