# -*- coding: utf-8 -*-
from os import path

from sphinx_vcs_changelog.factory import directive_factory
from tests.constants import TESTUSER

__docformat__ = 'reStructuredText'

import pytest


@pytest.fixture
def temp_dir():
    """Make temporary path for testing"""
    from shutil import rmtree
    from tempfile import mkdtemp
    root = mkdtemp()
    assert path.exists(root)
    yield root
    rmtree(root)


@pytest.fixture
def repo(temp_dir):
    """Make test repo in temporary path"""
    assert path.exists(temp_dir)
    from git import Repo
    _repo = Repo.init(temp_dir, mkdir=True)
    config_writer = _repo.config_writer()
    config_writer.set_value('user', 'name', TESTUSER)
    config_writer.release()
    return _repo


@pytest.fixture
def test_object_of_class(repo):
    yield directive_factory(path.join(repo.git_dir, 'changelog.rst'))
