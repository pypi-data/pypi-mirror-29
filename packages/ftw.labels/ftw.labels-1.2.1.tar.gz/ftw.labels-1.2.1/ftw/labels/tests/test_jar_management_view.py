from ftw.builder import Builder
from ftw.builder import create
from ftw.labels.config import COLORS
from ftw.labels.interfaces import ILabelJar
from ftw.labels.testing import LABELS_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import statusmessages
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest2 import TestCase


class TestLabelsJar(TestCase):
    layer = LABELS_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])

    @browsing
    def test_create_label(self, browser):
        root = create(Builder('label root'))

        browser.login().open(root,
                             view='labels-jar/create',
                             data={'title': 'Question',
                                   'color': 'purple'})

        self.assertEqual(
            [{'label_id': 'question',
              'title': 'Question',
              'color': 'purple'}],
            ILabelJar(root).list())

    @browsing
    def test_create_label_is_protected(self, browser):
        root = create(Builder('label root'))
        browser.login(create(Builder('user').with_roles('Reader')))

        with browser.expect_unauthorized():
            browser.open(root,
                         view='labels-jar/create',
                         data={'title': 'Question',
                               'color': 'purple'})

    @browsing
    def test_create_label_requires_label_arguments(self, browser):
        root = create(Builder('label root'))

        browser.login().open(root, view='labels-jar/create')

        statusmessages.assert_message(u"Please choose a title.")

    @browsing
    def test_create_label_without_color_add_random_existing_color(self, browser):
        root = create(Builder('label root'))
        browser.login()
        for i in range(0, len(COLORS)):
            browser.open(root,
                         view='labels-jar/create',
                         data={'title': 'Question'})

        selected_colors = [
            label.get('color') for label in ILabelJar(root).list()]
        self.assertEquals(len(COLORS), len(list(set(selected_colors))))

    @browsing
    def test_update_label(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red')))

        browser.login().open(root,
                             view='labels-jar/update',
                             data={'label_id': 'question',
                                   'title': 'Questions and inquiries',
                                   'color': 'green'})

        self.assertItemsEqual(
            [{'label_id': 'question',
              'title': 'Questions and inquiries',
              'color': 'green'},

             {'label_id': 'bug',
              'title': 'Bug',
              'color': 'red'}],
            ILabelJar(root).list())

    @browsing
    def test_update_label_requires_label_id(self, browser):
        root = create(Builder('label root'))

        with browser.expect_http_error(reason='Bad Request'):
            browser.login().open(root, view='labels-jar/update')

    @browsing
    def test_partial_update_label(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red')))

        browser.login().open(root,
                             view='labels-jar/update',
                             data={'label_id': 'question',
                                   'title': 'Questions and inquiries'})

        self.assertItemsEqual(
            [{'label_id': 'question',
              'title': 'Questions and inquiries',
              'color': 'purple'},

             {'label_id': 'bug',
              'title': 'Bug',
              'color': 'red'}],
            ILabelJar(root).list())

    @browsing
    def test_remove_label(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red')))

        browser.login().open(root,
                             view='labels-jar/remove',
                             data={'label_id': 'question'})

        self.assertEqual(
            [{'label_id': 'bug',
              'title': 'Bug',
              'color': 'red'}],
            ILabelJar(root).list())

    @browsing
    def test_remove_label_requires_label_id(self, browser):
        root = create(Builder('label root'))

        with browser.expect_http_error(reason='Bad Request'):
            browser.login().open(root, view='labels-jar/remove')

    @browsing
    def test_edit_label_form_change_title(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Feature', 'blue')))

        browser.login().open(root,
                             view='labels-jar/edit_label?label_id=feature')

        browser.fill({'title': 'Features and inquiries'}).submit()

        self.assertEqual(
            [{'label_id': 'feature',
              'title': 'Features and inquiries',
              'color': 'blue'}],
            ILabelJar(root).list())

    @browsing
    def test_edit_label_form_change_color(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Feature', 'blue')))

        browser.login().open(root,
                             view='labels-jar/edit_label?label_id=feature')

        browser.fill({'color': 'green'}).submit()

        self.assertEqual(
            [{'label_id': 'feature',
              'title': 'Feature',
              'color': 'green'}],
            ILabelJar(root).list())

    @browsing
    def test_edit_label_form_delete_label(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Feature', 'blue')))

        browser.login().open(root,
                             view='labels-jar/edit_label?label_id=feature')

        browser.find('Delete label').click()

        self.assertEqual([], ILabelJar(root).list())
