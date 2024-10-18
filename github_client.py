"""github网站相关"""
import re

from github import Auth
from github import Github


class GithubClient:
    """Github客户类，实现对接Github功能"""

    def __init__(self, token):
        auth = Auth.Token(token)
        self.client = Github(auth=auth)

    def fetch_rb_versions(self, url):
        """
        获取 rb 文件的版本列表
        :param url: rb文件的 url
        :return: 带有版本号和sha值的元组列表
        """

        owner, repo_name, path = self.parse_github_url(url)
        repo = self.client.get_repo(f"{owner}/{repo_name}")

        commits = repo.get_commits(path=path)
        versions = []
        for c in commits:
            message = c.commit.message
            # 有多行时，除了第一行，其他的表示提交的描述
            message = message.split("\n")[0]
            # 过滤有匹配版本形式的提交
            if not re.search(r'\d+(\.\d+)+$', message):
                continue

            versions.append((message, c.sha))
        return versions

    def download_raw_file(self, url):
        """
        下载 GitHub 的原始文件
        :param url: 文件网址
        :return:
        """
        owner, repo_name, path = self.parse_github_url(url)
        sha = re.search(rf"{owner}/{repo_name}/(\w+)", url).group(1)
        repo = self.client.get_repo(f"{owner}/{repo_name}")
        return repo.get_contents(path=path, ref=sha)\
            .decoded_content.decode()

    @classmethod
    def parse_github_url(cls, url: str):
        """
        解析 Github url，取得 拥有者、仓库名和文件路径等
        :param url:
        :return: 返回 拥有者、仓库名、文件路径
        """

        """
        为了匹配一般形式和资源形式的 github url，所以下面的正则稍微繁杂了一点
        """

        # 提取拥有者和仓库名称
        repo_match = re.search(r'github.*\.com/([^/]+)/([^/]+)/', url)
        if not repo_match:
            raise Exception("请输入正确的 Github 网址")

        owner = repo_match.group(1)
        repo_name = repo_match.group(2)

        # 提取路径
        file_match = re.search(rf'{owner}/{repo_name}/(blob/)?[^/]+/(.*)', url)
        if file_match:
            file_path = file_match.group(2)
        else:
            file_path = None
        return owner, repo_name, file_path
