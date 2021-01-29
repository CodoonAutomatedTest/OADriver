#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 下午1:49
# @File    : webelement.py
from oadriver.remote.webelement import WebElement as RemoteWebElement
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


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

    def get_string_html(self):
        return self._soup.prettify()

    def get_symbol_result(self):
        contexts = self._soup.find('table', {'class': 'bug_stat_table'})
        colums = [i.text.strip() for i in contexts.find_all('th')]
        cells = [i.text.strip() for i in contexts.find_all('td')]
        context = np.array(cells).reshape(int(len(cells) / len(colums)), len(colums))
        new_context = np.delete(context, 0, axis=1)
        return pd.DataFrame(data=new_context, columns=colums[1:], index=context[:,0])

    def get_dict_result(self):
        pages = self._soup.find('table', {'class': 'bug_stat_table'})
        colums = [i.text.strip() for i in pages.find_all('th')]
        cells = [i.text.strip() for i in pages.find_all('td')]
        context = np.array(cells).reshape(int(len(cells) / len(colums)), len(colums))
        new_context = np.delete(context, 0, axis=1)
        all_links = pages.find_all('a', attrs={"href":re.compile('BugStoryRelation_relative_id')})
        pattern = re.compile(r".*\[BugStoryRelation_relative_id\]=(\d+)")
        id_list = []
        for link in all_links:
            id_list.append(pattern.findall(link['href'])[0])
        final_values = []
        new_list = sorted(set(id_list), key=id_list.index)
        for index in range(len(context[:,0])-1):
            items = {u'需求名称': context[:, 0][index], 'href': 'https://www.tapd.cn/20041161/prong/stories/view/%s' % new_list[index]}
            for ite in range(len(colums[1:])):
                items[colums[1:][ite]] = new_context[index][ite]
            final_values.append(items)
        return final_values

    def get_dict_result2(self):
        pages = self._soup.find('table', {'class': 'bug_stat_table'})
        colums = [i.text.strip() for i in pages.find_all('th')]
        cells = [i.text.strip() for i in pages.find_all('td')]
        context = np.array(cells).reshape(int(len(cells) / len(colums)), len(colums))
        new_context = np.delete(context, 0, axis=1)
        df = pd.DataFrame(data=new_context, columns=colums[1:], index=context[:, 0])
        all_links = pages.find_all('a')
        des_links = [all_links[1]['href'], all_links[3]['href']]
        return df,des_links
