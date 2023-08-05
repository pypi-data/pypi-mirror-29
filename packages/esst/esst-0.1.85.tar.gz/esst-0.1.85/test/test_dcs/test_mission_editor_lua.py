# coding=utf-8
"""
Tests for esst.dcs.mission_editor_lua
"""
import string
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from esst.dcs import mission_editor_lua

TEMPLATE = Path('./test/test_files/MissionEditor.lua').read_text(encoding='utf8')


def test_injection():
    Path('./MissionEditor').mkdir()
    template_file = Path('./MissionEditor/MissionEditor.lua')
    template_file.write_text(TEMPLATE, encoding='utf8')
    assert mission_editor_lua.INJECT_TEMPLATE not in template_file.read_text(encoding='utf8')
    assert mission_editor_lua.inject_mission_editor_code('.')
    assert Path('./MissionEditor/MissionEditor.lua_backup_unknown').exists()
    content = template_file.read_text(encoding='utf8')
    assert mission_editor_lua.INJECT_TEMPLATE in content
    assert mission_editor_lua.inject_mission_editor_code('.')
    assert content == template_file.read_text(encoding='utf8')


def test_dcs_does_not_exist():
    with pytest.raises(FileNotFoundError):
        mission_editor_lua.inject_mission_editor_code('./some/dir')


def test_mission_editor_lua_does_not_exist():
    with pytest.raises(FileNotFoundError):
        mission_editor_lua.inject_mission_editor_code('.')


@given(text=st.text(min_size=400, max_size=600, alphabet=string.printable))
@settings(max_examples=20)
def test_wrong_content(text):
    Path('./MissionEditor').mkdir(exist_ok=True)
    template_file = Path('./MissionEditor/MissionEditor.lua')
    template_file.write_text(text, encoding='utf8')
    assert mission_editor_lua.INJECT_TEMPLATE not in template_file.read_text(encoding='utf8')
    assert not mission_editor_lua.inject_mission_editor_code('.')
    assert Path('./MissionEditor/MissionEditor.lua_backup_unknown').exists()
    assert mission_editor_lua.INJECT_TEMPLATE not in template_file.read_text(encoding='utf8')
