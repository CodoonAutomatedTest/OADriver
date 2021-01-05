#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/31 下午5:24
# @File    : send.py

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
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


def _create_requrie_message(version, table1):  # image1, table1, image2, table2, table3
    table_context = """<h3>三、缺陷关联需求情况统计</h3><table border="1"><caption>V%s关联需求统计</caption><tr><th>需求名称</th>""" % version
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


def make_mail_message(version, df1, df2, df3):
    mail_msg = """<p>Hi, all~</p><h1>V%s缺陷统计情况如下</h1>""" % version
    context1 = _create_general_message(version, df1)
    context2 = _create_regression_message(version, df2)
    context3 = _create_requrie_message(version, df3)
    mail_msg = mail_msg + context1 + context2 + context3
    return mail_msg


def send_mail(version, df1, df2, df3, pic1, pic2):
    # 设置收发邮件信息
    sender = 'xiaoqiang@codoon.com'
    receivers = ['xiaoqiang@codoon.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 企业邮箱 SMTP 服务
    mail_host = "smtp.exmail.qq.com"  # 设置服务器
    mail_user = "xiaoqiang@codoon.com"  # 用户名
    mail_pass = "WFUB52E8ePCi9k6d"  # 口令
    # ===========配置相关-=============
    message = MIMEMultipart('related')
    message['From'] = Header("TAPD版本统计", 'utf-8')  # 设置邮件发件人
    message['TO'] = Header("测试团队", 'utf-8')  # 设置邮件收件人
    message['Subject'] = 'V%s缺陷统计' % version  # 设置邮件标题
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    # 邮件正文
    mail_msg = make_mail_message(version, df1, df2, df3)
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
    try:
        email_client = smtplib.SMTP_SSL(mail_host, port=465)
        email_client.login(mail_user, mail_pass)
        email_client.sendmail(sender, receivers, message.as_string())
        print("已发送统计报告邮件")
    except smtplib.SMTPException:
        raise Exception("Error: 无法发送邮件")