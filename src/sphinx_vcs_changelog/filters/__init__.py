# -*- coding: utf-8 -*-
"""Define useful filters to repository commits"""
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


from abc import ABC
from abc import abstractmethod

from docutils.parsers.rst import Directive

from sphinx_vcs_changelog.constants import NOTSET


class CommitsFilter(object):
    """Base filter class"""

    def __init__(self, directive):
        super(CommitsFilter, self).__init__()
        assert isinstance(directive, Directive)
        self.directive = directive

    @property
    def required(self):
        """This filter is not required. Inheritors should overwrite it"""
        return False

    def exclude(self, commit):
        """Negated filter_value to use in itertools.filterfalse()"""
        return not self.pass_to_render(commit)

    @property
    def filter_function(self):
        """Return function to filter via current instance method"""
        filter_instance = self
        return lambda x: filter_instance.exclude(x)

    @abstractmethod
    def pass_to_render(self, commit):
        """Filter function itself.

        Should return True if current commit suitable chosen to be shown
        by current filter"""
        return True


class OptionFilter(CommitsFilter, ABC):
    """Filter based on option presence and value"""
    option = None

    # initial value to compare with
    compare = None

    def __init__(self, directive):
        """Init filter, using specified option name and value

        Option value stored internally in value for internal use """
        super(OptionFilter, self).__init__(directive)
        self.compare = self.__class__.compare

        from sphinx_vcs_changelog.repository import Repository
        assert isinstance(self.directive, Repository)
        self.value = self.directive.option(self.option, NOTSET)

    @property
    def required(self):
        """Check if this filter suitable.

        Return False if no option value set
        """
        return self.value != NOTSET
