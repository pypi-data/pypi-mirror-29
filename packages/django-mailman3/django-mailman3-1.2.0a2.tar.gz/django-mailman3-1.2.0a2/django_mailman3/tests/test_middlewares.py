# -*- coding: utf-8 -*-
#
# Copyright (C) 2017-2018 by the Free Software Foundation, Inc.
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


from mock import Mock
from django.conf import settings
from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from django_mailman3.middleware import PaginationMiddleware, TimezoneMiddleware


class TestPaginatorMiddleware(TestCase):

    def setUp(self):
        self.get_response = Mock()
        self.middleware = PaginationMiddleware(self.get_response)
        self.request = Mock()

    def test_request_with_page_value(self):
        data = {'page': 100}
        self.request.REQUEST = data
        self.middleware(self.request)
        self.assertEqual(self.request.page, 100)
        self.get_response.assert_called_once()

    def test_request_without_page_value(self):
        self.middleware(self.request)
        self.assertEqual(self.request.page, 1)


class TestTimezoneMiddleware(TestCase):

    def setUp(self):
        self.get_response = Mock()
        self.middleware = TimezoneMiddleware(self.get_response)
        self.request = Mock()

    def tearDown(self):
        timezone.deactivate()

    def test_non_logged_in_user(self):
        self.request.user.is_authenticated = lambda: False
        self.middleware(self.request)
        # If the user is not logged in, his timezone is the default timezone.
        self.assertEqual(settings.TIME_ZONE,
                         timezone.get_current_timezone_name())
        self.get_response.assert_called_once()

    def test_logged_in_user_without_mailman_profile(self):

        class MockUser:
            @property
            def mailman_profile(self):
                raise ObjectDoesNotExist

            def is_authenticated(self):
                return True

        self.request.user = MockUser()
        # If the mailman profile does not exist for the user, it still does not
        # have a personalized timezone.
        self.middleware(self.request)
        self.assertEqual(settings.TIME_ZONE,
                         timezone.get_current_timezone_name())
        self.get_response.assert_called_once()

    def test_logged_in_user_with_mailman_profile(self):
        self.request.user.is_authenticated = lambda: True
        self.request.user.mailman_profile = Mock(timezone='US/Central')
        # self.assertTrue(self.request.user.mailman_profile.called)
        # If the user has a timezone set in their profile, it should be set as
        # current timezone.
        self.middleware(self.request)
        self.assertEqual('US/Central',
                         timezone.get_current_timezone_name())
        self.get_response.assert_called_once()
