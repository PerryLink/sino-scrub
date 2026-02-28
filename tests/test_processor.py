"""核心处理器测试"""

import pytest
from pathlib import Path
from sino_scrub.processor import TextScrubber


def test_basic_replacement():
    """测试基础替换功能"""
    scrubber = TextScrubber(categories=['translation'])
    text = "系统正在处死进程"
    result, _ = scrubber.scrub(text)
    assert "终止" in result
    assert "处死" not in result


def test_cultural_taboo():
    """测试文化禁忌词替换"""
    scrubber = TextScrubber(categories=['cultural'])
    text = "祝您全家升天"
    result, _ = scrubber.scrub(text)
    assert "幸福" in result
    assert "升天" not in result


def test_track_changes():
    """测试变更追踪"""
    scrubber = TextScrubber(categories=['translation'])
    text = "系统正在处死进程"
    result, changes = scrubber.scrub(text, track_changes=True)

    assert changes is not None
    assert len(changes) > 0
    assert changes[0]['keyword'] == '处死'
    assert changes[0]['replacement'] == '终止'


def test_multiple_categories():
    """测试加载多个类别"""
    scrubber = TextScrubber(categories=['translation', 'cultural'])
    text = "系统处死进程后祝您升天"
    result, _ = scrubber.scrub(text)
    assert "终止" in result
    assert "幸福" in result


def test_case_insensitive():
    """测试大小写不敏感"""
    scrubber = TextScrubber(categories=['translation'])
    text = "系统正在处死进程"
    result, _ = scrubber.scrub(text)
    assert "终止" in result
