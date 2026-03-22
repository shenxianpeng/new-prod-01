"""
pytest 测试 — pipeline.py 核心函数

测试覆盖（见测试计划）：
  test_load_config_valid              — 正常解析 people.yml
  test_load_config_twitter_disabled   — enabled:false 时 twitter_enabled=False
  test_load_processed_ids_new         — 文件不存在时返回空集合
  test_load_processed_ids_existing    — 加载已有 ID 列表
  test_load_processed_ids_malformed   — 格式损坏时返回空集合（不崩溃）
  test_parse_llm_output_valid         — 正常 TITLE:/SUMMARY: 解析
  test_parse_llm_output_fallback      — 格式不符时返回原文 fallback
  test_parse_llm_output_partial       — 只有 SUMMARY 时正常处理
  test_render_html_with_entries       — 有内容时渲染正确 HTML
  test_render_html_empty              — 无内容时渲染空状态 HTML
"""

import json
import sys
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

# 把 src/ 加入 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pipeline import (
    TweetEntry,
    load_config,
    load_processed_ids,
    parse_llm_output,
    render_html,
    save_processed_ids,
)


# ---------------------------------------------------------------------------
# load_config
# ---------------------------------------------------------------------------

def test_load_config_valid(tmp_path):
    """正常 YAML 解析出正确的 Person 列表。"""
    config = {
        "people": [
            {
                "id": "sam_altman",
                "name": "Sam Altman",
                "twitter_handle": "sama",
                "sources": [{"type": "twitter", "enabled": True}],
            }
        ]
    }
    p = tmp_path / "people.yml"
    p.write_text(yaml.dump(config), encoding="utf-8")

    people = load_config(p)

    assert len(people) == 1
    assert people[0].id == "sam_altman"
    assert people[0].name == "Sam Altman"
    assert people[0].twitter_handle == "sama"
    assert people[0].twitter_enabled is True


def test_load_config_twitter_disabled(tmp_path):
    """enabled: false 时 twitter_enabled 应为 False。"""
    config = {
        "people": [
            {
                "id": "test_person",
                "name": "Test",
                "twitter_handle": "test",
                "sources": [{"type": "twitter", "enabled": False}],
            }
        ]
    }
    p = tmp_path / "people.yml"
    p.write_text(yaml.dump(config), encoding="utf-8")

    people = load_config(p)
    assert people[0].twitter_enabled is False


def test_load_config_empty_people(tmp_path):
    """people 列表为空时返回空列表，不崩溃。"""
    p = tmp_path / "people.yml"
    p.write_text(yaml.dump({"people": []}), encoding="utf-8")

    assert load_config(p) == []


# ---------------------------------------------------------------------------
# load_processed_ids / save_processed_ids
# ---------------------------------------------------------------------------

def test_load_processed_ids_new(tmp_path):
    """文件不存在时返回空集合。"""
    ids = load_processed_ids(tmp_path / "nonexistent.json")
    assert ids == set()


def test_load_processed_ids_existing(tmp_path):
    """正常加载已有 ID 列表。"""
    p = tmp_path / "processed_ids.json"
    p.write_text(json.dumps({"ids": ["123", "456"]}))

    ids = load_processed_ids(p)
    assert ids == {"123", "456"}


def test_load_processed_ids_malformed(tmp_path):
    """JSON 格式损坏时返回空集合，不抛出异常。"""
    p = tmp_path / "processed_ids.json"
    p.write_text("this is not valid json {{{{")

    ids = load_processed_ids(p)
    assert ids == set()


def test_save_and_reload_processed_ids(tmp_path):
    """save + load 往返一致。"""
    p = tmp_path / "processed_ids.json"
    original = {"aaa", "bbb", "ccc"}

    save_processed_ids(original, p)
    reloaded = load_processed_ids(p)

    assert reloaded == original


# ---------------------------------------------------------------------------
# parse_llm_output
# ---------------------------------------------------------------------------

def test_parse_llm_output_valid():
    """正常格式：提取 TITLE 和 SUMMARY。"""
    text = "TITLE: 关于 AGI 时间线的思考\nSUMMARY: Altman 认为 AGI 比预期更近。"
    result = parse_llm_output(text, original="The original tweet")

    assert result["title"] == "关于 AGI 时间线的思考"
    assert result["summary"] == "Altman 认为 AGI 比预期更近。"


def test_parse_llm_output_fallback():
    """格式完全不符时，返回原文 fallback（不跳过条目）。"""
    text = "Here is my translation: 这是翻译内容，但没有遵守格式。"
    original = "The original tweet text"

    result = parse_llm_output(text, original)

    assert result["title"] == "（原文）"
    assert result["summary"] == original


def test_parse_llm_output_partial_summary_only():
    """只有 SUMMARY 没有 TITLE 时，title 填充占位符。"""
    text = "SUMMARY: 这是摘要内容。"
    result = parse_llm_output(text, original="original")

    assert result["summary"] == "这是摘要内容。"
    assert result["title"] == "（无标题）"


def test_parse_llm_output_extra_prefix():
    """LLM 在 TITLE: 前加了多余的前缀行，仍能正确提取。"""
    text = textwrap.dedent("""\
        好的，这是翻译：
        TITLE: 核心标题
        SUMMARY: 核心摘要内容。
    """)
    result = parse_llm_output(text, original="original")

    assert result["title"] == "核心标题"
    assert result["summary"] == "核心摘要内容。"


# ---------------------------------------------------------------------------
# render_html
# ---------------------------------------------------------------------------

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def test_render_html_with_entries():
    """有内容时，HTML 包含条目的 person_name 和 summary。"""
    entries = [
        TweetEntry(
            tweet_id="1",
            person_id="sam_altman",
            person_name="Sam Altman",
            original_text="Original tweet",
            tweet_url="https://twitter.com/sama/status/1",
            created_at="2026-03-22 09:00",
            title="关于 AGI 的思考",
            summary="这是中文摘要。",
        )
    ]

    html = render_html(entries, today="2026-03-22", templates_dir=TEMPLATES_DIR)

    assert "Sam Altman" in html
    assert "这是中文摘要。" in html
    assert "Original tweet" in html
    assert "https://twitter.com/sama/status/1" in html
    assert "今日无新内容" not in html


def test_render_html_empty():
    """无内容时，HTML 包含空状态提示，不包含条目结构。"""
    html = render_html([], today="2026-03-22", templates_dir=TEMPLATES_DIR)

    assert "今日无新内容" in html
    assert "Sam Altman" not in html
