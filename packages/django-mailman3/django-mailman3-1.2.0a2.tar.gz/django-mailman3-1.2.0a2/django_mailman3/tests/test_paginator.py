# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2018 by the Free Software Foundation, Inc.
#
# This file is part of Django-Mailman.
#
# Django-Mailman is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Django-Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Django-Mailman.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aurelien Bompard <abompard@fedoraproject.org>
#


from django.template import Context
from django.test import RequestFactory, SimpleTestCase

from django_mailman3.lib.paginator import paginate, MailmanPaginator
from django_mailman3.templatetags.pagination import (
    add_to_query_string, paginator)
from django_mailman3.tests.utils import TestCase, FakeMMPage


class TestMailmanPaginator(TestCase):

    def setUp(self):
        super(TestMailmanPaginator, self)._pre_setup()
        # Create a user pagination based on just list of numbers instead of
        # list of users. This is a mocked page and thus doesn't really care.
        self.mailman_client.get_user_page.return_value = FakeMMPage(
            count=5, entries=list(range(100)))
        self.user_pages = MailmanPaginator(
            function=self.mailman_client.get_user_page, per_page=5)

    def test_get_page_one(self):
        user_page_1 = self.user_pages.page(1)
        self.assertIsNotNone(user_page_1)
        # The number of entries in this list should be 5.
        self.assertEqual(len(list(user_page_1)), 5)

    def test_get_count(self):
        # Total number of elements in this paginator class should be 100
        self.assertEqual(self.user_pages.count, 100)


class PaginateTestCase(SimpleTestCase):

    def test_page_range_ellipsis(self):
        objects = list(range(1000))
        self.assertEqual(
            paginate(objects, 1, 20).paginator.page_range_ellipsis,
            [1, 2, 3, 4, '...', 50])
        self.assertEqual(
            paginate(objects, 2, 20).paginator.page_range_ellipsis,
            [1, 2, 3, 4, 5, '...', 50])
        self.assertEqual(
            paginate(objects, 3, 20).paginator.page_range_ellipsis,
            [1, 2, 3, 4, 5, 6, '...', 50])
        self.assertEqual(
            paginate(objects, 4, 20).paginator.page_range_ellipsis,
            [1, 2, 3, 4, 5, 6, 7, '...', 50])
        self.assertEqual(
            paginate(objects, 5, 20).paginator.page_range_ellipsis,
            [1, 2, 3, 4, 5, 6, 7, 8, '...', 50])
        self.assertEqual(
            paginate(objects, 6, 20).paginator.page_range_ellipsis,
            [1, 2, 3, 4, 5, 6, 7, 8, 9, '...', 50])
        self.assertEqual(
            paginate(objects, 7, 20).paginator.page_range_ellipsis,
            [1, '...', 4, 5, 6, 7, 8, 9, 10, '...', 50])
        self.assertEqual(
            paginate(objects, 8, 20).paginator.page_range_ellipsis,
            [1, '...', 5, 6, 7, 8, 9, 10, 11, '...', 50])
        self.assertEqual(
            paginate(objects, 9, 20).paginator.page_range_ellipsis,
            [1, '...', 6, 7, 8, 9, 10, 11, 12, '...', 50])
        self.assertEqual(
            paginate(objects, 10, 20).paginator.page_range_ellipsis,
            [1, '...', 7, 8, 9, 10, 11, 12, 13, '...', 50])
        self.assertEqual(
            paginate(objects, 30, 20).paginator.page_range_ellipsis,
            [1, '...', 27, 28, 29, 30, 31, 32, 33, '...', 50])
        self.assertEqual(
            paginate(objects, 40, 20).paginator.page_range_ellipsis,
            [1, '...', 37, 38, 39, 40, 41, 42, 43, '...', 50])
        self.assertEqual(
            paginate(objects, 41, 20).paginator.page_range_ellipsis,
            [1, '...', 38, 39, 40, 41, 42, 43, 44, '...', 50])
        self.assertEqual(
            paginate(objects, 42, 20).paginator.page_range_ellipsis,
            [1, '...', 39, 40, 41, 42, 43, 44, 45, '...', 50])
        self.assertEqual(
            paginate(objects, 43, 20).paginator.page_range_ellipsis,
            [1, '...', 40, 41, 42, 43, 44, 45, 46, '...', 50])
        self.assertEqual(
            paginate(objects, 44, 20).paginator.page_range_ellipsis,
            [1, '...', 41, 42, 43, 44, 45, 46, 47, '...', 50])
        self.assertEqual(
            paginate(objects, 45, 20).paginator.page_range_ellipsis,
            [1, '...', 42, 43, 44, 45, 46, 47, 48, 49, 50])
        self.assertEqual(
            paginate(objects, 46, 20).paginator.page_range_ellipsis,
            [1, '...', 43, 44, 45, 46, 47, 48, 49, 50])
        self.assertEqual(
            paginate(objects, 47, 20).paginator.page_range_ellipsis,
            [1, '...', 44, 45, 46, 47, 48, 49, 50])
        self.assertEqual(
            paginate(objects, 48, 20).paginator.page_range_ellipsis,
            [1, '...', 45, 46, 47, 48, 49, 50])
        self.assertEqual(
            paginate(objects, 49, 20).paginator.page_range_ellipsis,
            [1, '...', 46, 47, 48, 49, 50])
        self.assertEqual(
            paginate(objects, 50, 20).paginator.page_range_ellipsis,
            [1, '...', 47, 48, 49, 50])

    def test_default_page(self):
        self.assertEqual(paginate(list(range(100)), None).number, 1)

    def test_last_page(self):
        self.assertEqual(paginate(list(range(100)), 1000).number, 10)

    def test_page_str(self):
        try:
            self.assertEqual(paginate(list(range(1000)), "2").number, 2)
        except TypeError as e:
            self.fail(e)

    def test_page_not_an_int(self):
        self.assertEqual(paginate(list(range(100)), "dummy").number, 1)

    def test_add_to_query_string(self):
        request = RequestFactory().get("/url", {"key1": "value1"})
        result = add_to_query_string(
            {"request": request}, "key2", "value2", key3="value3")
        self.assertEqual(
            set(result.split("&amp;")),
            set(["key1=value1", "key2=value2", "key3=value3"]))

    def test_paginator_tag(self):
        objects = paginate(list(range(100)), 1, 20)
        context = Context({'title': 'My Title'})
        updated_context = paginator(context, objects)
        self.assertEqual(updated_context['label_previous'], 'Previous')
        self.assertEqual(updated_context['label_next'], 'Next')
        self.assertEqual(updated_context['page'], objects)
        self.assertEqual(updated_context['per_page_options'],
                         [10, 25, 50, 100, 200])
        dated_pages_ctxt = paginator(context, objects, bydate=True)
        self.assertEqual(dated_pages_ctxt['label_previous'], 'Newer')
        self.assertEqual(dated_pages_ctxt['label_next'], 'Older')
