#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 下午2:19
# @File    : draw.py

import matplotlib.pyplot as plt
import numpy as np


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


def graph_bar_chg_state_as_png(dataframe, filename, version):
    dataframe = dataframe.astype(int)
    name_list = dataframe.index.tolist()[:-1]
    num_list = dataframe[dataframe.columns[0]].tolist()[:-1]
    num_list1 = dataframe[dataframe.columns[1]].tolist()[:-1]
    num_list2 = dataframe[dataframe.columns[2]].tolist()[:-1]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
    plt.figure(dpi=100,figsize=(10.5, 5.5))
    index = np.arange(len(name_list))
    plt.bar(index-0.2, num_list, 0.2, color='blue', tick_label=name_list, label='创建缺陷总数')
    plt.bar(index, num_list1, 0.2, color="red", label='修复缺陷总数')
    plt.bar(index+0.2, num_list2, 0.2, color="yellow",  label='关闭缺陷总数', tick_label=name_list)
    plt.legend(['创建缺陷总数', '修复缺陷总数', '关闭缺陷总数'], labelspacing=1)
    for a, b in zip(index - 0.2, num_list):  # 柱子上的数字显示
        plt.text(a, b, '%d' % b, ha='center', va='bottom', fontsize=7)
    for a, b in zip(index, num_list1):
        plt.text(a, b, '%d' % b, ha='center', va='bottom', fontsize=7)
    for a, b in zip(index + 0.2, num_list2):
        plt.text(a, b, '%d' % b, ha='center', va='bottom', fontsize=7)
    plt.title('V%s缺陷每日变化趋势' % version)
    # 设置x轴标签位置
    # 设置 x 坐标轴刻度的旋转方向和大小
    # rotation: 旋转方向
    plt.xticks(index, name_list,rotation=90, fontsize=7)
    plt.ylabel('个数')
    plt.legend()

    plt.savefig(filename + ".png")
    plt.close()
    return filename + ".png"