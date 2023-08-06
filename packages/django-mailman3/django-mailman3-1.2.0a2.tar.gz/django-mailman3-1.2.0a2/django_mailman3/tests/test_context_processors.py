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


from django.test import TestCase, RequestFactory, override_settings
from django_mailman3.context_processors import common


class TestContextProcessors(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(LOGIN_URL='/login', LOGOUT_URL='/logout',
                       ALLOWED_HOSTS=['example.com'])
    def test_common_with_all_vars(self, *args, **kwargs):
        request = self.factory.get('/', HTTP_HOST='example.com')
        context = common(request)
        self.assertEqual(context['site_name'], 'example.com')
        self.assertEqual(context['LOGIN_URL'], '/login')
        self.assertEqual(context['LOGOUT_URL'], '/logout')
