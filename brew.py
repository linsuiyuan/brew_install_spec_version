"""brew 相关操作"""
import re
import subprocess


def brew_info(name, app_type=None):
    """
    读取 brew 软件的 info
    :param name: 软件的名称
    :param app_type: 软件的类型（formula 和 cask）, 若为 None 则表示两者都获取
    :return:
    """

    # 为None时给app_type是集合，那么后面的in判断，不管是判断在集合中还是在字符串中，那么
    if app_type is None:
        app_type = {"cask", "formula"}

    apps = []

    if "cask" in app_type:
        result = subprocess.run(['brew', 'info', '--cask', name], capture_output=True, text=True)
        if result.stdout:
            github_url = re.search(r'https:.*\.rb', result.stdout).group()
            apps.append(("cask", github_url))

    if "formula" in app_type:
        result = subprocess.run(['brew', 'info', '--formula', name], capture_output=True, text=True)
        if result.stdout:
            github_url = re.search(r'https:.*\.rb', result.stdout).group()
            apps.append(("formula", github_url))

    return apps


