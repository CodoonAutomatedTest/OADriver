#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 下午1:49
# @File    : webelement.py
from bs4 import BeautifulSoup


class WebElement(object):

    def __init__(self, resp, features='html.parser'):
        self._response = resp
        self._features = features
        self._soup = self._execute()

    def __repr__(self):
        return '<{0.__module__}.{0.__name__}>'.format(
            type(self), self._response)

    def _execute(self):
        return BeautifulSoup(self._response.text, features=self._features)

    def find_element(self, name=None, attrs=None, recursive=True, text=None,
                     **kwargs):
        if attrs is None:
            attrs = {}
        return self._execute().find(name, attrs, recursive, text,
             **kwargs)

    def find_elements(self, name=None, attrs=None, recursive=True, text=None,
                      **kwargs):
        if attrs is None:
            attrs = {}
        return self._execute().find_all(name, attrs, recursive, text,
             **kwargs)


