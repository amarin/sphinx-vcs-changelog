# -*- coding: utf-8 -*-
"""Simple linear changelog"""
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
from sphinx_vcs_changelog.formatter import CommitFormatter
from sphinx_vcs_changelog.repository import Repository
from docutils import nodes


class ChangelogWriter(Repository, CommitFormatter):
    """Base class for simple linear changelog's"""

    def build_markup(self):
        """Build markup"""
        list_node = nodes.bullet_list()
        for commit in self.commits:
            item = self.format_commit_message(commit)
            list_node.append(item)
        return [list_node]
