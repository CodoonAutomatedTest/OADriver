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
from oadriver.Tapd.draw import graph_pie_save_png, graph_bar_save_png, graph_bar_chg_state_as_png

if __name__ == '__main__':
    default = ['qa@codoon.com']
    version = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    receivers = default + sys.argv[4:]
    tapdriver = TapDriver()
    general_bugs = tapdriver.bugs_general_stat(version)
    regression_bugs = tapdriver.bugs_regression_stat(version)
    bug_requrie = tapdriver.bugs_touch_require(version)
    android_non_requrie = tapdriver.bugs_non_touch_require(version, "android")
    ios_non_requrie = tapdriver.bugs_non_touch_require(version, "ios")
    api_non_requrie = tapdriver.bugs_non_touch_require(version, "api")
    h5_non_requrie = tapdriver.bugs_non_touch_require(version, "H5")
    hard_non_requrie = tapdriver.bugs_non_touch_require(version, "硬件")
    handle_24hour_bugs = tapdriver.bugs_24hour_handle(version)
    df1 = general_bugs.get_symbol_result()
    df2 = regression_bugs.get_symbol_result()
    df3 = bug_requrie.get_dict_result()
    non_and = android_non_requrie.get_dict_result3()
    non_ios = ios_non_requrie.get_dict_result3()
    non_api = api_non_requrie.get_dict_result3()
    non_h5 = h5_non_requrie.get_dict_result3()
    non_hard = hard_non_requrie.get_dict_result3()
    df4 = (handle_24hour_bugs.get_symbol_result()).astype(int)
    df4, links = handle_24hour_bugs.get_dict_result2()
    df4 = df4.astype(int)
    chg_status = tapdriver.bugs_chg_status(version, start_date, end_date)
    df5 = chg_status.get_dict_result4()
    pic1 = graph_pie_save_png(df1.values[-1][1:].tolist(), df1.columns[1:], '%s_bugs_general' % version)
    pic2 = graph_pie_save_png(df2.values[-1][1:-1].tolist(), df2.columns[1:-1], '%s_bugs_regression' % version)
    pic3 = graph_bar_save_png(df4, '%s_bugs_24hours_handler' % version)
    pic4 = graph_bar_chg_state_as_png(df5, '%s_bugs_chg_state' % version, version)
    send_mail(version, df1, df2, df3, non_and, non_ios, non_api, non_h5, non_hard, df4, df5, links, pic1, pic2, pic3, pic4, receivers)