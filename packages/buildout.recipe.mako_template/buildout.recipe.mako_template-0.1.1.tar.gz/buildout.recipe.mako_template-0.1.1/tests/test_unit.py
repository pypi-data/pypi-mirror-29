#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit Tests for `buildout.recipe.mako_template` package."""
import os
import pytest
from zc.buildout import UserError
from buildout.recipe.mako_template.recipe import _parse_files_option


def test_content_parse_files_option():
    data = """
        base/mytemplate.mako.make:/bin/Makefile:true
        base/mytemplate2.mako.make:mytemplate2.make
        base/mytemplate3.mako.make : /mytemplate3.make :
    """
    files = [
        ('base/mytemplate.mako.make', '/bin/Makefile', True),
        ('base/mytemplate2.mako.make', os.path.join(os.getcwd(), 'mytemplate2.make'), False),
        ('base/mytemplate3.mako.make', '/mytemplate3.make', False),
    ]
    assert _parse_files_option(data) == files


def test_malformed_content_parse_files_option():
    data = """
        base/mytemplate3.mako.make : /mytemplate3.make
        base/mytemplate.mako.make    /bin/Makefile
    """
    msg = (
        "Malformed file option 'base/mytemplate.mako.make    /bin/Makefile'\n"
        "allowed format is 'source:target[:is_executable(true or false)[:collision_allowed]]'"
    )
    with pytest.raises(UserError) as exp:
        _parse_files_option(data)
    assert str(exp.value) == msg


def test_templates_collision():
    data = """
        base/mytemplate.mako.make : /mytemplate3.make
        base/mytemplate.mako.make : /bin/Makefile
    """
    with pytest.raises(UserError) as exp:
        assert _parse_files_option(data)
    assert str(exp.value) == "Template collision is detected at 'base/mytemplate.mako.make : /bin/Makefile'"


def test_targets_collision():
    data = """
        base/mytemplate1.mako.make : /bin/Makefile
        base/mytemplate2.mako.make : /bin/Makefile
    """
    with pytest.raises(UserError) as exp:
        assert _parse_files_option(data)
    assert str(exp.value) == "Target collision is detected at 'base/mytemplate2.mako.make : /bin/Makefile'"


def test_allow_collision():
    data = """
        base/mytemplate1.mako.make : /bin/Makefile1
        base/mytemplate2.mako.make : /bin/Makefile2
        base/mytemplate1.mako.make : /bin/Makefile3 ::collision_allowed
        base/mytemplate3.mako.make : /bin/Makefile2 ::collision_allowed

    """
    files = [
        ('base/mytemplate1.mako.make', '/bin/Makefile1', False),
        ('base/mytemplate2.mako.make', '/bin/Makefile2', False),
        ('base/mytemplate1.mako.make', '/bin/Makefile3', False),
        ('base/mytemplate3.mako.make', '/bin/Makefile2', False),
    ]
    assert _parse_files_option(data) == files
