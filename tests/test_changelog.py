# -*- coding: utf-8 -*-
import random
import re

from sphinx_vcs_changelog.changelog import ChangelogWriter
from sphinx_vcs_changelog.constants import OPTION_MATCH
from sphinx_vcs_changelog.constants import OPTION_MAX_RESULTS_COUNT


# class TestWithRepository(ChangelogTestCase):
#
##
#     def test_single_commit_message_and_user_display(self):
#         self.repo.index.commit('my root commit')
#         nodes = self.changelog.run()
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         item = list_markup.bullet_list.list_item
#         children = list(item.childGenerator())
#         assert_equal(5, len(children))
#         assert_equal('my root commit', children[0].text)
#         assert_equal('Test User', children[2].text)
#
#     def test_single_commit_message_and_user_display_with_non_ascii_chars(
#     self):
#         self._set_username('þéßþ  Úßéë')
#         self.repo.index.commit('my root commit')
#         nodes = self.changelog.run()
#         list_markup = BeautifulSoup(six.text_type(nodes[0]), features='xml')
#         item = list_markup.bullet_list.list_item
#         children = list(item.childGenerator())
#         assert_equal(5, len(children))
#         assert_equal('my root commit', children[0].text)
#         assert_equal(u'þéßþ  Úßéë', children[2].text)
#
#     def test_single_commit_time_display(self):
#         before = datetime.now().replace(microsecond=0)
#         self.repo.index.commit('my root commit')
#         nodes = self.changelog.run()
#         after = datetime.now()
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         item = list_markup.bullet_list.list_item
#         children = list(item.childGenerator())
#         timestamp = datetime.strptime(children[4].text, '%Y-%m-%d %H:%M:%S')
#         assert_less_equal(before, timestamp)
#         assert_greater(after, timestamp)
#
#     def test_single_commit_default_detail_setting(self):
#         self.repo.index.commit(
#             'my root commit\n\nadditional information\nmore info'
#         )
#         nodes = self.changelog.run()
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         item = list_markup.bullet_list.list_item
#         children = list(item.childGenerator())
#         assert_equal(6, len(children))
#         assert_equal('my root commit', children[0].text)
#         assert_equal('Test User', children[2].text)
#         assert_equal(
#             str(children[5]),
#             '<paragraph>additional information\nmore info</paragraph>'
#         )
#
#     def test_single_commit_preformmated_detail_lines(self):
#         self.repo.index.commit(
#             'my root commit\n\nadditional information\nmore info'
#         )
#         self.changelog.options.update({'detailed-message-pre': True})
#         nodes = self.changelog.run()
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         item = list_markup.bullet_list.list_item
#         children = list(item.childGenerator())
#         assert_equal(6, len(children))
#         assert_equal(
#             str(children[5]),
#             '<literal_block xml:space="preserve">additional information\n'
#             'more info</literal_block>'
#         )
#
#     def test_more_than_ten_commits(self):
#         for n in range(15):
#             self.repo.index.commit('commit #{0}'.format(n))
#         nodes = self.changelog.run()
#         assert_equal(1, len(nodes))
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         assert_equal(1, len(list_markup.findAll('bullet_list')))
#         bullet_list = list_markup.bullet_list
#         assert_equal(10, len(bullet_list.findAll('list_item')))
#         for n, child in zip(range(15, 5), bullet_list.childGenerator()):
#             assert_in('commit #{0}'.format(n), child.text)
#         assert_not_in('commit #4', bullet_list.text)
#
#     def test_specifying_number_of_commits(self):
#         for n in range(15):
#             self.repo.index.commit('commit #{0}'.format(n))
#         self.changelog.options.update({'revisions': 5})
#         nodes = self.changelog.run()
#         assert_equal(1, len(nodes))
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         assert_equal(1, len(list_markup.findAll('bullet_list')))
#         bullet_list = list_markup.bullet_list
#         assert_equal(5, len(bullet_list.findAll('list_item')))
#         for n, child in zip(range(15, 10), bullet_list.childGenerator()):
#             assert_in('commit #{0}'.format(n), child.text)
#         assert_not_in('commit #9', bullet_list.text)
#
#     def test_specifying_a_rev_list(self):
#         self.repo.index.commit('before tag')
#         commit = self.repo.index.commit('at tag')
#         self.repo.index.commit('after tag')
#         self.repo.index.commit('last commit')
#         self.repo.create_tag('testtag', commit)
#
#         self.changelog.options.update({'rev-list': 'testtag..'})
#         nodes = self.changelog.run()
#
#         assert_equal(1, len(nodes))
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         assert_equal(1, len(list_markup.findAll('bullet_list')))
#
#         bullet_list = list_markup.bullet_list
#         assert_equal(2, len(bullet_list.findAll('list_item')))
#
#         children = list(bullet_list.childGenerator())
#         first_element = children[0]
#         second_element = children[1]
#         assert_in('last commit', first_element.text)
#         assert_in('after tag', second_element.text)
#
#     def test_warning_given_if_rev_list_and_revisions_both_given(self):
#         self.repo.index.commit('a commit')
#         self.changelog.options.update({'rev-list': 'HEAD', 'revisions': 12})
#         nodes = self.changelog.run()
#         assert_equal(
#             1, self.changelog.state.document.reporter.warning.call_count
#         )
#
#     def test_line_number_displayed_in_multiple_option_warning(self):
#         self.repo.index.commit('a commit')
#         self.changelog.options.update({'rev-list': 'HEAD', 'revisions': 12})
#         nodes = self.changelog.run()
#         document_reporter = self.changelog.state.document.reporter
#         assert_equal(
#             [call(ANY, line=self.changelog.lineno)],
#             document_reporter.warning.call_args_list
#         )
#
#     def test_name_filter(self):
#         self.repo.index.commit('initial')
#         for file_name in ['abc.txt', 'bcd.txt', 'abc.other', 'atxt']:
#             full_path = os.path.join(self.repo.working_tree_dir, file_name)
#             f = open(full_path, 'w+')
#             f.close()
#             self.repo.index.add([full_path])
#             self.repo.index.commit('commit with file {}'.format(file_name))
#         self.repo.index.commit('commit without file')
#
#         self.changelog.options.update({'filename_filter': 'a.*txt'})
#         nodes = self.changelog.run()
#         assert_equal(1, len(nodes))
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         assert_equal(1, len(list_markup.findAll('bullet_list')))
#
#         bullet_list = list_markup.bullet_list
#         assert_equal(2, len(bullet_list.findAll('list_item')), nodes)
#
#         next_file = os.path.join(self.repo.working_tree_dir, 'atxt')
#         f = open(next_file, 'w+')
#         f.close()
#         self.repo.index.add([next_file])
#         self.repo.index.commit('show me')
#
#         nodes = self.changelog.run()
#         assert_equal(1, len(nodes), nodes)
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         assert_equal(1, len(list_markup.findAll('bullet_list')))
#
#         bullet_list = list_markup.bullet_list
#         assert_equal(2, len(bullet_list.findAll('list_item')), nodes)
#
#     def test_single_commit_hide_details(self):
#         self.repo.index.commit(
#             'Another commit\n\nToo much information'
#         )
#         self.changelog.options.update({'hide_details': True})
#         nodes = self.changelog.run()
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         item = list_markup.bullet_list.list_item
#         children = list(item.childGenerator())
#         assert_equal(5, len(children))
#         assert_equal('Another commit', children[0].text)
#         assert_equal('Test User', children[2].text)
#
#     def test_single_commit_message_hide_author(self):
#         self.repo.index.commit('Yet another commit')
#         self.changelog.options.update({'hide_author': True})
#         nodes = self.changelog.run()
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         item = list_markup.bullet_list.list_item
#         children = list(item.childGenerator())
#         print(children)
#         assert_equal(3, len(children))
#         assert_equal('Yet another commit', children[0].text)
#         assert_not_in(' by Test User', children[1].text)
#         assert_in(' at ', children[1].text)
#
#     def test_single_commit_message_hide_date(self):
#         self.repo.index.commit('Yet yet another commit')
#         self.changelog.options.update({'hide_date': True})
#         nodes = self.changelog.run()
#         list_markup = BeautifulSoup(str(nodes[0]), features='xml')
#         item = list_markup.bullet_list.list_item
#         children = list(item.childGenerator())
#         print(children)
#         assert_equal(3, len(children))
#         assert_equal('Yet yet another commit', children[0].text)
#         assert_not_in(' at ', children[1].text)
#         assert_in(' by ', children[1].text)
#
#
# class TestWithOtherRepository(TestWithRepository):
#     """
#     The destination repository is not in the same repository as the rst files.
#     """
#
#     def setup(self):
#         super(TestWithOtherRepository, self).setup()
#         self.changelog.state.document.settings.env.srcdir = os.getcwd()
#         self.changelog.options.update({'repo-dir': self.root})


def test_100_grouped_group_extraction(test_object_of_class):
    instance = test_object_of_class
    assert isinstance(instance, ChangelogWriter)
    # assert isinstance(instance.debug, int)

    prefix_1 = 'ref:'
    prefix_2 = 'doc:'

    group_1_template = prefix_1 + ' commit #%d'
    group_2_template = prefix_2 + ' commit #%d'
    group_n_template = 'just commit #%d'
    message_regex = '^([a-z]{3}:).+\\#\\d+$'
    for x in range(0, 20):
        template = random.choice([
            group_1_template, group_2_template, group_n_template
        ])
        msg = template % x
        if not template == group_n_template:
            assert re.match(message_regex, msg)
        instance.repo.index.commit(msg)

    instance.options.update({
        OPTION_MATCH: message_regex
    })

    groups = instance.unique_groups
    assert groups == {prefix_1, prefix_2}


def test_100_filter_count(test_object_of_class):
    instance = test_object_of_class
    assert isinstance(instance, ChangelogWriter)

    instance.repo.index.commit('initial')
    instance.options.update({
        OPTION_MAX_RESULTS_COUNT: 5
    })

    for _num in range(0, 9):
        instance.repo.index.commit('ref: commit #%d' % _num)

    instance.apply_filters()
    assert instance.commits_count == 5


