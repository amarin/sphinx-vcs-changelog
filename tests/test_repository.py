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
import re
from os import path

from docutils import nodes


def test_no_repository_raises(temp_dir):
    from sphinx_vcs_changelog.exceptions import RepositoryNotFound
    from sphinx_vcs_changelog.factory import directive_factory

    expect_exception_class = RepositoryNotFound
    not_a_vcs_path = path.join(temp_dir, 'test.rst')

    try:
        directive = directive_factory(not_a_vcs_path)
        directive.run()
    except expect_exception_class:
        pass
    else:
        raise NotImplementedError("Expects %s" % expect_exception_class)


def test_no_path_raises(temp_dir):
    from sphinx_vcs_changelog.exceptions import InvalidPath
    from sphinx_vcs_changelog.factory import directive_factory

    expect_exception_class = InvalidPath
    not_a_vcs_path = path.join(temp_dir, 'test_rst', 'example.rst')
    try:
        directive = directive_factory(not_a_vcs_path)
        directive.run()
    except expect_exception_class:
        pass
    else:
        raise NotImplementedError("Expects %s" % expect_exception_class)


def test_no_commits(test_object_of_class):
    from sphinx_vcs_changelog.changelog import ChangelogWriter
    from sphinx_vcs_changelog.exceptions import NoCommits

    assert isinstance(test_object_of_class, ChangelogWriter)
    expecting_exception_classes = (NoCommits, )

    try:
        test_object_of_class.run()
    except expecting_exception_classes:
        pass
    else:
        raise AssertionError(
            "Expected any of %s", ', '.join(
                (x.__name__ for x in expecting_exception_classes)
            )
        )


def test_100_filter_matched(test_object_of_class):
    instance = test_object_of_class
    from sphinx_vcs_changelog.changelog import ChangelogWriter
    from sphinx_vcs_changelog.constants import OPTION_MATCH

    assert isinstance(instance, ChangelogWriter)

    message_to_match = 'ref: commit #1'
    message_regex = '^[a-z]{3}:.+#\\d+$'
    assert re.match(message_regex, message_to_match) is not None

    instance.repo.index.commit('initial')
    instance.repo.index.commit('next initial')
    instance.repo.index.commit(message_to_match)
    instance.repo.index.commit('another one matched')

    assert instance.commits_count == 4

    instance.options.update({
        OPTION_MATCH: message_regex
    })

    assert instance.commits_count == 1
    assert {x.message for x in instance.commits_list} == {message_to_match}


def test_100_filter_since(test_object_of_class):
    instance = test_object_of_class
    from sphinx_vcs_changelog.changelog import ChangelogWriter
    from sphinx_vcs_changelog.constants import OPTION_SINCE

    assert isinstance(instance, ChangelogWriter)

    instance.repo.index.commit('initial')
    total_commits = 1

    message_template = 'ref: commit #%d'
    look_for_commit_number = 4
    look_for_commit_message = message_template % look_for_commit_number
    look_for_hexsha = None

    commits_after_requested = []

    assert instance.commits_count == total_commits

    for _num in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        msg = message_template % _num
        commit = instance.repo.index.commit(msg)
        total_commits += 1

        if look_for_hexsha is not None:
            commits_after_requested.append(msg)

        if msg == look_for_commit_message:
            look_for_hexsha = commit.hexsha

    assert instance.commits_count == total_commits

    instance.options.update({
        OPTION_SINCE: look_for_commit_message
    })

    assert instance.commits_count == len(commits_after_requested)
    assert set(
        [x.message for x in instance.commits_list]
    ) == set(commits_after_requested)

    del instance.options[OPTION_SINCE]
    assert instance.commits_count == 10
    instance.options.update({
        OPTION_SINCE: look_for_hexsha
    })
    assert instance.commits_count == len(commits_after_requested)
    assert set(
        [x.message for x in instance.commits_list]
    ) == set(commits_after_requested)


def test_first_commit_produces_one_item(test_object_of_class):
    from sphinx_vcs_changelog.changelog import ChangelogWriter
    assert isinstance(test_object_of_class, ChangelogWriter)
    test_object_of_class.repo.index.commit('initial')
    res = test_object_of_class.run()
    assert 1 == len(res)
    assert isinstance(res[0], nodes.bullet_list)

def test_commit_template_parts(test_object_of_class):
    from sphinx_vcs_changelog.changelog import ChangelogWriter
    assert isinstance(test_object_of_class, ChangelogWriter)
    test_object_of_class.repo.index.commit('initial')
    res = test_object_of_class.run()
    assert 1 == len(res)
    assert isinstance(res[0], nodes.bullet_list)

