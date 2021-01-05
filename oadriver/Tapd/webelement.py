#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 下午1:49
# @File    : webelement.py
from oadriver.remote.webelement import WebElement as RemoteWebElement
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _make_autopct(values):
    values = list(map(int, values))
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        # 同时显示数值和占比的饼图
        return '{p:.2f}%\n  ({v:d})'.format(p=pct, v=val)
    return my_autopct


class WebElement(RemoteWebElement):

    def __init__(self, resp, features='html.parser'):
        super().__init__(resp,features)

    def get_symbol_result(self):
        context = self._soup.find('table', {'class': 'bug_stat_table'})
        colums = [i.text.strip() for i in context.find_all('th')]
        cells = [i.text.strip() for i in context.find_all('td')]
        context = np.array(cells).reshape(int(len(cells) / len(colums)), len(colums))
        new_context = np.delete(context, 0, axis=1)
        return pd.DataFrame(data=new_context, columns=colums[1:], index=context[:,0])

    def graph_save_png(values, labels, filename):
        colors = ["lightskyblue", "steelblue", "sandybrown", "darkgrey", "coral", "pink", "rosybrown", "lightblue",
                  "plum",
                  "lightsalmon", "salmon", "mediumaquamarine", "mediumseagreen"]
        plt.pie(x=values, labels=labels, autopct=_make_autopct(values), colors=colors)
        plt.axis('off')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
        plt.savefig(filename + ".png")
        return filename
