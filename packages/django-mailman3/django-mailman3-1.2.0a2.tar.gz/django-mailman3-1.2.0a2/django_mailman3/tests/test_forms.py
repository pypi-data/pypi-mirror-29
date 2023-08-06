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


from django.test import TestCase
from django.contrib.auth.models import User
from django_mailman3.forms import UserProfileForm


class TestUserProfileForm(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='bob',
                                        email='bob@example.com')

    def tearDown(self):
        self.user.delete()

    def test_valid_form(self):
        data = dict(username='alice',
                    first_name='Alice',
                    last_name='Wonderland',
                    timezone='UTC')
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = dict(username='alice',
                    first_name='Alice',
                    last_name='',
                    timezone='UTC')
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('This field is required.' in str(form.errors))
        self.assertTrue('last_name' in str(form.errors))

    def test_form_cleans_username(self):
        data = dict(username='bob',
                    first_name='Bob',
                    last_name='User',
                    timezone='UTC')
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue('A user with that username already exists.'
                        in str(form.errors))
