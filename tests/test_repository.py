# -*- coding: utf-8 -*-
"""Test repository-related cases"""
#
#  Copyright 2018-2019 (C) Aleksey Marin <asmadews@gmail.com>
#  #
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  #
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  #
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from os import path

from sphinx_vcs_changelog.factory import directive_factory


def test_no_repository_raises(temp_dir):
    from sphinx_vcs_changelog.exceptions import RepositoryNotFound
    expect_exception_class = RepositoryNotFound
    not_a_vcs_path = path.join(temp_dir, 'test.rst')
    try:
        directive = directive_factory(not_a_vcs_path)
        res = directive.run()
    except expect_exception_class:
        pass
    else:
        raise NotImplementedError("Expects %s" % expect_exception_class)


def test_no_path_raises(temp_dir):
    from sphinx_vcs_changelog.exceptions import InvalidPath
    expect_exception_class = InvalidPath
    not_a_vcs_path = path.join(temp_dir, 'test_rst', 'example.rst')
    try:
        directive = directive_factory(not_a_vcs_path)
        res = directive.run()
    except expect_exception_class:
        pass
    else:
        raise NotImplementedError("Expects %s" % expect_exception_class)

