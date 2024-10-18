"""测试 github 模块"""
import pytest
from dotenv import load_dotenv

from github_client import GithubClient

load_dotenv()
import config  # noqa


@pytest.fixture(scope="module")
def client():
    """共用Github 客户端"""
    client = GithubClient(token=config.GITHUB_TOKEN)
    yield client


def test_fetch_rb_versions(client):
    url = "https://github.com/Homebrew/homebrew-cask/blob/HEAD/Casks/p/popclip.rb"
    history_url = client.fetch_rb_versions(url)
    for c in history_url:
        print(c)


def test_download_raw_file(client):
    url = "https://raw.githubusercontent.com/Homebrew/homebrew-cask/c6048eadd1aac13d3659b3e522d0a272faaf1617" \
          "/Casks/p/popclip.rb"
    content = client.download_raw_file(url)
    print(content)


def test_parse_github_url():
    # 一般形式的 github url
    url = "https://github.com/Homebrew/homebrew-cask/blob/HEAD/Casks/p/popclip.rb"
    result = GithubClient.parse_github_url(url)
    assert result == ('Homebrew', 'homebrew-cask', 'Casks/p/popclip.rb')

    # 原始文件形式的 github url
    url = "https://raw.githubusercontent.com/Homebrew/homebrew-cask/c6048eadd1aac13d3659b3e522d0a272faaf1617" \
          "/Casks/p/popclip.rb"
    result = GithubClient.parse_github_url(url)
    assert result == ('Homebrew', 'homebrew-cask', 'Casks/p/popclip.rb')
