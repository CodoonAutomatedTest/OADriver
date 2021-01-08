#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 下午2:19
# @File    : draw.py

import matplotlib.pyplot as plt


def _make_autopct(values):
    values = list(map(int, values))
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        # 同时显示数值和占比的饼图
        return '{p:.2f}%\n  ({v:d})'.format(p=pct, v=val)
    return my_autopct


def graph_pie_save_png(values, labels, filename):
    colors = ["lightskyblue", "steelblue", "sandybrown", "darkgrey", "coral", "pink", "rosybrown", "lightblue", "plum",
              "lightsalmon", "salmon", "mediumaquamarine", "mediumseagreen"]
    plt.pie(x=values, labels=labels, autopct=_make_autopct(values), colors=colors)
    plt.axis('off')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
    plt.savefig(filename + ".png")
    plt.close()
    return filename + ".png"


def graph_bar_save_png(dataframe, filename):
    dataframe.plot(kind='bar', rot=0)
    for i in range(0, 2):
        plt.text(i - 0.14, dataframe.get("0-1天")[i], '%.0f' % dataframe.get("0-1天")[i], ha='center', va='bottom')
        plt.text(i + 0.12, dataframe.get(">1天")[i], '%.0f' % dataframe.get(">1天")[i], ha='center', va='bottom')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
    plt.savefig(filename + ".png")
    plt.close()
    return filename + ".png"