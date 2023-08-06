#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Acceptance Tests for `buildout.recipe.mako_template` package."""

import os
import zc.buildout.testing


def test_simple_usecase(buildout_dir):
    zc.buildout.buildout.main(["-NU", "install", 'simple-test'])
    with open("simple-test-template.out") as f:
        out = f.read()
    assert out == 'Hello, test!\n'
    assert os.access("bash_script.out", os.X_OK)


def test_ineritance(buildout_dir):
    zc.buildout.buildout.main(["-NU", "install", 'inerit-test'])
    with open("inerit-test-template.out") as f:
        out = f.read()
    assert out == 'Hi! This is base0 template!\n    inheriting block\ninheriting body\nAnd this is it, base0 template ends here...\n'


def test_buildout_parts_are_accessible_in_tempate(buildout_dir):
    zc.buildout.buildout.main(["-NU", "install", 'buildout_parts_are_accessible_in_tempate'])
    with open("buildout_parts_are_accessible_in_tempate.out") as f:
        out = f.read()
    assert out == 'test can see zc.recipe.egg\n'


def test_directories_option_for_lookup(buildout_dir):
    zc.buildout.buildout.main(["-NU", "install", 'inerit-test-template-directories-lookup'])
    with open("inerit-test-template-directories-lookup.out") as f:
        out = f.read()
    assert out == 'Hi! This is base0 template!\n    inheriting block\ninheriting body\nAnd this is it, base0 template ends here...\n'
