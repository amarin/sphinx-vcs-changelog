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
from datetime import datetime

from docutils.frontend import OptionParser
from docutils.io import StringInput
from git import Commit

from sphinx_vcs_changelog.constants import DEFAULT_ITEM_TEMPLATE
from sphinx_vcs_changelog.constants import OPTION_ITEM_TEMPLATE
from sphinx_vcs_changelog.repository import Repository


class ChangelogWriter(Repository):
    """Base class for simple linear changelog's"""
    default_changelog_template = "{commits}"

    known_commit_properties = [
        'summary',
        'message',
        'name_rev',
        'author'
    ]

    def get_template(self):
        """Prepare changelog template"""
        if self.content:
            content_text = '\n'.join((
                x
                for x in self.content
            ))
            return content_text

        return self.default_changelog_template

    def get_item_template(self):
        """Get used item template"""
        return self.option(OPTION_ITEM_TEMPLATE, DEFAULT_ITEM_TEMPLATE)

    def prepare_rst(self):
        """Make internal ReStructuredText changelog"""
        template = self.get_template()
        self.info("Using template:\n%s" % template)
        context = {}
        for context_updater_class in self.context_processors:
            context_updater = context_updater_class(self)

            if not context_updater.required:
                continue

            for x in self.commits:
                context_updater.collect_commit_info(x)

            context.update(context_updater.context)

        context.update(
            commits='\n'.join((
                self.format_commit_message(x) for x in self.commits
            ))
        )
        return template.format(**context)

    def build_markup(self):
        """Build markup"""
        from docutils.readers import Reader

        internal_rst = self.prepare_rst()
        internal_rst_fh = StringInput(source=internal_rst)
        reader = Reader(parser_name='rst')

        option_parser = OptionParser()
        settings = option_parser.get_default_values()
        settings.update(
            dict(
                tab_width=3,
                pep_references=False,
                rfc_references=False
            ),
            option_parser
        )
        document = reader.read(internal_rst_fh, reader.parser, settings)
        return document.children

    @staticmethod
    def get_commit_dict(commit):
        """Return commit as dict to use in string format
        :param commit: Commit instance
        :type commit: Commit

        :rtype: dict
        """
        assert isinstance(commit, Commit)

        if '\n' in commit.message:
            summary, detailed_message = commit.message.split('\n', 1)
        else:
            summary = commit.message
            detailed_message = None

        return dict(
            summary=summary,
            detail=detailed_message,
            message=commit.message,
            name_rev=commit.name_rev,
            author=commit.author,
            date=datetime.fromtimestamp(commit.authored_date),
        )

    def format_commit_message(self, commit):
        """Format commit message & detailed representation"""
        template = self.get_item_template()
        format_args = self.get_commit_dict(commit)
        return template.format(**format_args)
