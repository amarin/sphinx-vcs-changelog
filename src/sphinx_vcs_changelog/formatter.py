# -*- coding: utf-8 -*-
"""Commit message formatter"""
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
from abc import abstractmethod
from datetime import datetime

import six
from docutils import nodes

from sphinx_vcs_changelog.decorator import use_option


@use_option('detailed-message-pre', bool)
@use_option('hide_author', bool)
@use_option('hide_date', bool)
@use_option('hide_details', bool)
class CommitFormatter(object):
    """Format commit message into docutils nodes"""
    options = {}
    option_spec = {}

    def format_commit_message(self, commit):
        """Format commit message & detailed representation"""
        date_str = datetime.fromtimestamp(commit.authored_date)
        if '\n' in commit.message:
            message, detailed_message = commit.message.split('\n', 1)
        else:
            message = commit.message
            detailed_message = None

        item = nodes.list_item()
        # choose detailed message style by detailed-message-strong option
        item += nodes.inline(text=message)

        if not self.options.get('hide_author'):
            item += [
                nodes.inline(text=" by "),
                nodes.emphasis(text=six.text_type(commit.author))
            ]
        if not self.options.get('hide_date'):
            item += [
                nodes.inline(text=" at "),
                nodes.emphasis(text=str(date_str))
            ]
        if detailed_message and not self.options.get('hide_details'):
            detailed_message = detailed_message.strip()
            if self.options.get('detailed-message-pre', False):
                item.append(
                    nodes.literal_block(text=detailed_message))
            else:
                item.append(nodes.paragraph(text=detailed_message))
        return item

    @abstractmethod
    def option(self, option_name, default=None):
        """Shorthand method to get option value"""

    @abstractmethod
    def option_configured(self, option_name):
        """Check if option is set to any value

        :rtype: bool
        """
