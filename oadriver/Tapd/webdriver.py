#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 下午6:00
# @File    : oadriver.py
from oadriver.remote.webdriver import Webdriver
import os, json
from datetime import datetime
from oadriver.Tapd.webelement import WebElement as TapdElement


def _get_create_date():
    return datetime.now().strftime("%Y-%m-%d")


def _load_log_conf():
    current_path = os.path.abspath(os.path.dirname(__file__))
    # os.chdir(current_path + '/conf')
    with open(current_path + "/conf/log_parm.json", "r") as f:
        return json.load(f)


def _load_bug_trace_conf():
    current_path = os.path.abspath(os.path.dirname(__file__))
    # os.chdir(current_path + '/conf')
    with open(current_path + "/conf/bug_trace.json", "r") as f:
        return json.load(f)


class TapDriver(Webdriver):
    _tapd_element_cls = TapdElement

    def __init__(self):
        log_parmas = _load_log_conf()
        self._login_url, self._username, self._password = log_parmas['login_url'], log_parmas['username'], log_parmas[
            'password']
        self._tapd = Webdriver(self._login_url, self._username, self._password)

    def create_tapd_element(self, response, features='html.parser'):
        """Creates a web element with the specified `element_id`."""
        return self._tapd_element_cls(response, features)

    def bugs_regression_stat(self, version):
        bug_regress_url = _load_bug_trace_conf()['bug_regression_url']
        req_body = str(_load_bug_trace_conf()['bug_reg_body']) % (_get_create_date(), version)
        return self.create_tapd_element(self._tapd.post(bug_regress_url, eval(req_body)))

    def bugs_general_stat(self, version):
        bug_general_url = _load_bug_trace_conf()['bug_general_url']
        req_body = str(_load_bug_trace_conf()['bug_gen_body']) % (_get_create_date(), version)
        return self.create_tapd_element(self._tapd.post(bug_general_url, eval(req_body)))

    def bugs_24hour_handle(self, version):
        bug_general_url = _load_bug_trace_conf()['bug_handle_url']
        req_body = str(_load_bug_trace_conf()['bug_handle_body']) % (_get_create_date(), _get_create_date(), version)
        return self.create_tapd_element(self._tapd.post(bug_general_url, eval(req_body)))

    def bugs_touch_require(self, version):
        bug_general_url = _load_bug_trace_conf()['bug_general_url']
        req_body = str(_load_bug_trace_conf()['bug_requrie_body']) % (_get_create_date(), version)
        return self.create_tapd_element(self._tapd.post(bug_general_url, eval(req_body)))
