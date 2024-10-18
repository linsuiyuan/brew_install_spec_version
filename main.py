"""入口文件"""
import sys
from pathlib import Path

import config
import brew
from github_client import GithubClient


def get_app_rb_url(app_name):
    """获取 brew 软件 rb文件的url"""
    print(f"从 brew 查询 {app_name} 的信息")

    apps = brew.brew_info(app_name)
    if len(apps) == 0:
        raise Exception(f"没有找到软件：{app_name}")

    for app_type, url in apps:
        print(f"查到 {app_type}: {app_name}")

    # 等于1时，直接返回
    if len(apps) == 1:
        return apps[0]

    # 大于1时，需要选择1个
    tip = f"请选择一个类型：{[t for t, _ in apps]}(首字母): "
    while len(apps) > 1:
        input_ = input(tip)
        for app_type, url in apps:
            if app_type.startswith(input_):
                return app_type, url
        tip = "请输入正确的首字母: "


def get_spec_version(url):
    """获取特定的版本"""
    client = GithubClient(token=config.GITHUB_TOKEN)
    versions = client.fetch_rb_versions(url)

    print("从 Github 查询到的版本如下：")
    for i, (v, _) in enumerate(versions, start=1):
        print(f"{i}: {v}")
    tip = f"请选择一个版本(填版本前的序号): "
    choice = 0
    while not choice:
        input_ = input(tip)
        try:
            choice = int(input_)
        except ValueError:
            tip = f"请输入正常的数字: "
        else:
            if 0 < choice <= len(versions):
                # 拼凑特定版本号的rb文件网址
                version, sha = versions[choice - 1]
                owner, repo_name, file_path = client.parse_github_url(url)
                spec_rb_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{sha}/{file_path}"
                return version, spec_rb_url
            else:
                tip = f"请输入正确的序号: "


def download_and_save_rb(raw_url: str):
    """下载并保存rb文件"""
    client = GithubClient(token=config.GITHUB_TOKEN)
    content = client.download_raw_file(raw_url)
    filename = raw_url.rsplit("/", 1)[-1]
    file = Path(filename)
    file.write_text(content)
    return filename


def main():
    """入口函数"""

    if len(sys.argv) <= 1:
        app_name = input("请输入需要搜索的软件: ")
    else:
        app_name = sys.argv[1]

    try:
        app_type, url = get_app_rb_url(app_name)
    except Exception as ex:
        print(ex)
        exit(1)

    version, raw_url = get_spec_version(url)

    print(f"开始下载版本：{version} 的 rb 文件")
    filename = download_and_save_rb(raw_url)
    print(f"rb 文件({filename}) 下载成功")


main()
