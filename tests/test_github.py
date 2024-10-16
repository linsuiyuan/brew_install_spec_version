"""测试 github 模块"""
from github import fetch_rb_history_url
from github import fetch_rb_version_list


def test_fetch_rb_history():
    url = "https://github.com/Homebrew/homebrew-cask/blob/HEAD/Casks/p/popclip.rb"
    history_url = fetch_rb_history_url(url)
    print(history_url)


def test_fetch_rb_version_list():
    url = "https://github.com/Homebrew/homebrew-cask/commits/a44d1b7babca5293d5c1d5a930c99d1ba7d9de60" \
          "/Casks/p/popclip.rb"
    commit_list = fetch_rb_version_list(url)
    for c in commit_list:
        print(c)
