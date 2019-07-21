# -*- coding: utf-8 -*-
"""Constants to use internally"""

#: directive name
DIRECTIVE_CHANGELOG = 'vcs_changelog'

#: option name to setup repo-path
OPTION_REPO_DIR = 'repo-path'

#: option name to select commits only after specified commit message or sha
OPTION_SINCE = 'added-since'

#: option name to take limited results count
OPTION_MAX_RESULTS_COUNT = 'limit'

#: option name to take commits if message matched regexp only
OPTION_MATCH = 'filter-regex'

#: option name to count commits if message matched regexp only
OPTION_MATCH_COUNT = 'context-regex-count'

#: option name to match regexp groups in commits
OPTION_MATCH_GROUPS = 'context-regex-groups'

#: option to define commit output template
OPTION_ITEM_TEMPLATE = 'item-template'

#: default commit output template is list item containing summary only
DEFAULT_ITEM_TEMPLATE = '- {summary}'

#: NOTSET value
NOTSET = object()

#: NOTSET str representation
NOTSET_STR = 'empty'

#: Known commit keys to use in templates
COMMIT_KEYS = [
    'message',
    'date',
    'author',
]
