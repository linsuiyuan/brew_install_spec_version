"""测试 brew 模块"""
import pytest

from brew import brew_info


@pytest.mark.parametrize("app_name,results", [
    ["hehe", 0],
    ["poppler", 1],
    ["doppler", 2],
])
def test_brew_info(app_name, results):
    assert len(brew_info(app_name)) == results
