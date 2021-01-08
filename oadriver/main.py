#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/4 下午4:26
# @File    : main.py

import sys, os
p = os.path.dirname(os.path.dirname((os.path.abspath('__file__'))))
if p not in sys.path:
    sys.path.append(p)
from oadriver.Tapd.webdriver import TapDriver
from oadriver.mail.send import send_mail
from oadriver.Tapd.draw import graph_save_png

if __name__ == '__main__':
    default = ['xiaoqiang@codoon.com']
    version = sys.argv[1]
    receivers = default + sys.argv[2:]
    tapdriver = TapDriver()
    general_bugs = tapdriver.bugs_general_stat(version)
    regression_bugs = tapdriver.bugs_regression_stat(version)
    bug_requrie = tapdriver.bugs_touch_require(version)
    df1 = general_bugs.get_symbol_result()
    df2 = regression_bugs.get_symbol_result()
    df3 = bug_requrie.get_dict_result()
    pic1 = graph_save_png(df1.values[-1][1:].tolist(), df1.columns[1:], '%s_bugs_general' % version)
    pic2 = graph_save_png(df2.values[-1][1:-1].tolist(), df2.columns[1:-1], '%s_bugs_regression' % version)
    send_mail(version, df1, df2, df3, pic1, pic2, receivers)