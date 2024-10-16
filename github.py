"""github网站相关"""
import json
import re

import requests
from lxml import etree


def fetch_rb_history_url(url):
    """
    获取 rb 文件的历史提交
    :param url: rb文件的 url
    :return: 提交历史 url
    """

    resp = requests.get(url)
    resp.raise_for_status()

    html_tree = etree.HTML(resp.text)
    title = html_tree.xpath('//title/text()')[0]

    oid = re.search(r"rb at (\w+) · ", title).group(1)
    history_url = url.replace("blob/HEAD", f"commits/{oid}")
    return history_url


def fetch_rb_version_list(hitstory_url):
    """
    获取 rb 版本列表
    :param hitstory_url: 提交历史 url
    :return: 返回包含 oid 和 version 的元组
    """
    resp = requests.get(hitstory_url)
    resp.raise_for_status()

    html_tree = etree.HTML(resp.text)

    data_target = html_tree.xpath('//script[@data-target="react-app.embeddedData"]/text()')[0]
    commit_group = json.loads(data_target)['payload']['commitGroups']
    # 注意 commitGroups 里面的提交按日期分组，同一天里可能有多个提交
    # 版本一般包含在 shortMessage 字段里
    commit_list = [(c['oid'], c['shortMessage'])
                   for commit in commit_group
                   for c in commit["commits"]
                   # 过滤版本形式的
                   if re.search(r"\d+(\.\d+)+", c['shortMessage'])]
    return commit_list
