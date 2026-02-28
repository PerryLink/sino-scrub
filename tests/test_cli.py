"""CLI 测试"""

import pytest
from typer.testing import CliRunner
from sino_scrub.cli import app

runner = CliRunner()


def test_basic_text_input():
    """测试直接文本输入"""
    result = runner.invoke(app, ["系统正在处死进程"])
    assert result.exit_code == 0
    assert "终止" in result.stdout


def test_diff_mode():
    """测试 diff 模式"""
    result = runner.invoke(app, ["系统正在处死进程", "--diff"])
    assert result.exit_code == 0


def test_debug_mode():
    """测试 debug 模式"""
    result = runner.invoke(app, ["系统正在处死进程", "--debug"])
    assert result.exit_code == 0
    assert "Debug Information" in result.stdout


def test_category_filter():
    """测试类别过滤"""
    result = runner.invoke(app, ["系统处死进程", "-c", "translation"])
    assert result.exit_code == 0
