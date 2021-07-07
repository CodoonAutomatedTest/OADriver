#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/31 下午5:24
# @File    : send.py

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import os


def _create_general_message(version, table1):  # image1, table1, image2, table2, table3
    table_context = """<h3>一、缺陷平台分布统计</h3><p><img src="cid:image1"></p><table border="1"><caption>V%s缺陷平台分布情况</caption><tr><th>状态</th>""" % version
    for colum in table1.columns:
        table_context += '<th>' + colum + '</th>'
    table_context += '</tr><tr>'
    for index, row in table1.iterrows():
        table_context += '<td>' + index + '</td>'
        for item in row:
            table_context += '<td>' + item + '</td>'
        table_context += '</tr>'
    table_context += '</table>'
    return table_context


def _create_regression_message(version, table1):  # image1, table1, image2, table2, table3
    table_context = """<h3>二、缺陷修复成功率统计</h3><p><img src="cid:image2"></p><table border="1"><caption>V%s修复成功率</caption><tr><th>操作系统</th>""" % version
    for colum in table1.columns:
        table_context += '<th>' + colum + '</th>'
    table_context += '</tr><tr>'
    for index, row in table1.iterrows():
        table_context += '<td>' + index + '</td>'
        for item in row:
            table_context += '<td>' + item + '</td>'
        table_context += '</tr>'
    table_context += '</table>'
    return table_context


def _create_requrie_message(version, table1, non_and, non_ios, non_api, non_h5, non_hard):  # image1, table1, image2, table2, table3
    table_context = """<h3>五、缺陷关联需求情况统计</h3><table border="1"><caption>V%s关联需求统计</caption><tr>""" % version
    temp_context = ''
    for colum in table1[-1].keys():
        if colum == 'href':
            continue
        table_context += '<th>' + colum + '</th>'
        if colum == 'android':
            temp_context += '<td>' + non_and + '</td>'
        elif colum == 'H5':
            temp_context += '<td>' + non_h5 + '</td>'
        elif colum == 'ios':
            temp_context += '<td>' + non_ios + '</td>'
        elif colum == 'api':
            temp_context += '<td>' + non_api + '</td>'
        elif colum == '硬件':
            temp_context += '<td>' + non_hard + '</td>'
        elif colum == '小计':
            total = int(non_and) + int(non_h5) + int(non_ios) + int(non_api) + int(non_hard)
            temp_context += '<td>' + str(total) + '</td>'
    table_context += '</tr><tr>'
    for cells in table1:
        cells_list = list(cells.values())
        table_context += '<td><a href=' + cells_list[1] + '>' + cells_list[0] + '</a></td>'
        for cell in cells_list[2:]:
            table_context += '<td>' + cell + '</td>'
        table_context += '</tr>'
    table_context += '<td>未关联需求的缺陷</td>' + temp_context
    table_context += '</table>'
    return table_context


def _create_24hours_message(version, df1, df2, links):
    unhandled_sum = sum(df2.get('>1天').values)
    unhandled_new = df2.get('>1天').values[0]
    unhandled_process = df2.get('>1天').values[1]
    total_sum = int(df1.loc[['总计'], "小计"].values[0])
    rate = (1 - unhandled_sum/total_sum) * 100
    table_context = """<h3>三、24小时缺陷处理率</h3><p>%s共计发现bug数：%s个，bug保持新和接受/处理状态超过一天的数量共计：%s个。(其中状态新为<a href=%s>%s个</a>, 状态接受/处理为<a href=%s>%s个</a>)</p><p>缺陷24小时处理率为1-%s/%s=%.01f%%</p><p><img 
    src="cid:image3"></p>""" % (version, total_sum, unhandled_sum, links[0], unhandled_new, links[1], unhandled_process, unhandled_sum, total_sum, rate)
    return table_context


def _create_daily_chg_message(version, table1):  # image1, table1, image2, table2, table3
    table_context = """<h3>四、缺陷每日变化趋势</h3><p><img src="cid:image4"></p><table border="1"><caption>V%s缺陷每日变化趋势</caption><tr><th>日期</th>""" % version
    for colum in table1.columns:
        table_context += '<th>' + colum + '</th>'
    table_context += '</tr><tr>'
    for index, row in table1.iterrows():
        table_context += '<td>' + index + '</td>'
        for item in row:
            table_context += '<td>' + item + '</td>'
        table_context += '</tr>'
    table_context += '</table>'
    return table_context


def make_mail_message(version, df1, df2, df3, non_and, non_ios, non_api, non_h5, non_hard, df4, df5, links):
    mail_msg = """<p>Hi, all~</p><h1>V%s缺陷统计情况如下</h1>""" % version
    context1 = _create_general_message(version, df1)
    context2 = _create_regression_message(version, df2)
    context3 = _create_requrie_message(version, df3, non_and, non_ios, non_api, non_h5, non_hard)
    context4 = _create_24hours_message(version, df1, df4, links)
    context5 = _create_daily_chg_message(version, df5)
    mail_msg = mail_msg + context1 + context2 + context4 + context5 + context3
    return mail_msg


def send_mail(version, df1, df2, df3, non_and, non_ios, non_api, non_h5, non_hard, df4, df5, links, pic1, pic2, pic3, pic4, receivers):
    # 设置收发邮件信息
    sender = 'xiaoqiang@codoon.com'
    # 企业邮箱 SMTP 服务
    mail_host = "smtp.exmail.qq.com"  # 设置服务器
    mail_user = "xiaoqiang@codoon.com"  # 用户名
    mail_pass = "WFUB52E8ePCi9k6d"  # 口令
    # ===========配置相关-=============
    message = MIMEMultipart('related')
    # message['From'] = Header("TAPD版本统计", 'utf-8')  # 设置邮件发件人
    # message['TO'] = Header("测试团队", 'utf-8')  # 设置邮件收件人
    message['From'] = _format_addr(u'TAPD版本统计 <%s>' % sender)  # 设置邮件发件人
    message['to'] = _list_format_addr(receivers)  # 设置邮件收件人
    if is_number(version):
        title = "非主版本需求%s" % version
    else:
        title = "V%s" % version
    message['Subject'] = Header('%s缺陷统计' % title)  # 设置邮件标题
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    # 邮件正文
    mail_msg = make_mail_message(version, df1, df2, df3, non_and, non_ios, non_api, non_h5, non_hard, df4, df5, links)
    msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    current_path = os.path.abspath(os.path.dirname(__file__))
    root_path = os.path.dirname(current_path)
    os.chdir(root_path)
    # 指定图片为当前目录
    fp = open(pic1, 'rb')
    msgImage1 = MIMEImage(fp.read())
    fp.close()
    # 定义图片 ID，在 HTML 文本中引用
    msgImage1.add_header('Content-ID', '<image1>')
    message.attach(msgImage1)
    #
    # 指定图片为当前目录
    fp = open(pic2, 'rb')
    msgImage2 = MIMEImage(fp.read())
    fp.close()
    # 定义图片 ID，在 HTML 文本中引用
    msgImage2.add_header('Content-ID', '<image2>')
    message.attach(msgImage2)
    fp = open(pic3, 'rb')
    msgImage3 = MIMEImage(fp.read())
    fp.close()
    # 定义图片 ID，在 HTML 文本中引用
    msgImage3.add_header('Content-ID', '<image3>')
    message.attach(msgImage3)
    # 指定图片为当前目录
    fp = open(pic4, 'rb')
    msgImage4 = MIMEImage(fp.read())
    fp.close()
    # 定义图片 ID，在 HTML 文本中引用
    msgImage4.add_header('Content-ID', '<image4>')
    message.attach(msgImage4)
    try:
        email_client = smtplib.SMTP_SSL(mail_host, port=465)
        email_client.login(mail_user, mail_pass)
        email_client.sendmail(sender, receivers, message.as_string())
        print("已发送统计报告邮件")
    except smtplib.SMTPException:
        raise Exception("Error: 无法发送邮件")


def _format_addr(s):
    addr = parseaddr(s)
    return formataddr(addr)


def _list_format_addr(li):
    return ','.join(li)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
