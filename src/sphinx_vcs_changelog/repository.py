# -*- coding: utf-8 -*-
"""Base"""
from abc import abstractmethod
from itertools import filterfalse

import six
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from git import Repo

from sphinx_vcs_changelog.constants import OPTION_MATCH
from sphinx_vcs_changelog.constants import OPTION_MAX_RESULTS_COUNT
from sphinx_vcs_changelog.constants import OPTION_REPO_DIR
from sphinx_vcs_changelog.constants import OPTION_SINCE
from sphinx_vcs_changelog.decorator import use_option
from sphinx_vcs_changelog.filters import CommitsFilter
from sphinx_vcs_changelog.filters import NOTSET
from sphinx_vcs_changelog.filters.added_since import AddedSince
from sphinx_vcs_changelog.filters.matched_regexp import MatchedRegexp
from sphinx_vcs_changelog.filters.results_count import ResultsCount


@use_option(OPTION_REPO_DIR, six.text_type)
@use_option(OPTION_SINCE, directives.nonnegative_int)
@use_option(OPTION_MATCH, six.text_type)
@use_option(OPTION_MAX_RESULTS_COUNT, directives.nonnegative_int)
class Repository(Directive):
    """Base class for changelog directive

    Provides access method to VCS repository definition,
    commits filtering and options definitions
    """

    filters = [
        AddedSince,
        MatchedRegexp,
        ResultsCount,
    ]

    def __init__(self, *args, **kwargs):
        super(Repository, self).__init__(*args, **kwargs)
        self.debug = None
        self.info = None
        self.warning = None
        self.error = None
        self.critical = None

        self._filtered = None
        self.prepare()

    def prepare(self):
        """Separated initialisation.
        Called from __init__ during work process
        as well as directly in tests.

        Dont inline into __init__ because of testing behaviour"""
        self.debug = self.state.document.reporter.debug
        self.info = self.state.document.reporter.info
        self.warning = self.state.document.reporter.warning
        self.error = self.state.document.reporter.error
        self.critical = self.state.document.reporter.severe

    def using_repo(self):
        """Find target repository and return Repo object.

        :returns: Repo
        """
        repo_dir = self.options.get(
            OPTION_REPO_DIR,
            self.state.document.settings.env.srcdir
        )
        repo = Repo(repo_dir, search_parent_directories=True)
        return repo

    @property
    def repo(self):
        """Get current repository as property"""
        return self.using_repo()

    def option(self, option_name, default=None):
        """Shorthand method to get options"""
        if option_name not in self.option_spec:
            raise NotImplementedError("No such option %s" % option_name)
        return self.options.get(option_name, default)

    def option_configured(self, option_name):
        """Check if option is set to any value"""
        return not self.options.get(option_name, NOTSET) == NOTSET

    @property
    def commits(self):
        """Iterator over repository commits.

        Filtering commits using current filter set"""
        if self._filtered is None:
            self._filtered = self.using_repo().iter_commits()

        for filter_instance_or_class in self.get_filter_ordering():
            self._apply_filter(filter_instance_or_class)

        return self._filtered

    @property
    def commits_messages(self):
        """Iterator over repository commits messages"""
        self._filtered = None
        for x in self.commits:
            yield x.message

    @property
    def commits_list(self):
        """List of repository commits to render"""
        self._filtered = None
        return list(self.commits)

    @property
    def commits_count(self):
        """Count filtered commits count"""
        return len(self.commits_list)

    def _apply_filter(self, filter_class):
        """Apply additional filter to commits iterator"""
        _instance = self.get_filter_instance(filter_class)
        if not _instance.required:
            return

        self._filtered = filterfalse(_instance.filter_function, self._filtered)

    def get_filter_instance(self, filter_class):
        """Make filter instance by filter_class"""
        assert issubclass(filter_class, CommitsFilter)
        return filter_class(self)

    def get_filter_ordering(self):
        """Return filter functions apply ordering"""
        return self.filters

    def run(self):
        """Choose commits to display & build markup """
        return self.build_markup()

    @abstractmethod
    def build_markup(self):
        """Build markup"""
        raise NotImplementedError("%s.build_markup() to be implemented")
