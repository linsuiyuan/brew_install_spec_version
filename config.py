"""配置模块"""
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
assert GITHUB_TOKEN is not None


if __name__ == '__main__':
    print(GITHUB_TOKEN)
