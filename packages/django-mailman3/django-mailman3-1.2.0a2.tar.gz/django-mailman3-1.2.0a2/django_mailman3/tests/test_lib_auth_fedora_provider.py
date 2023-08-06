# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 by the Free Software Foundation, Inc.
#
# This file is part of Django-Mailman3.
#
# HyperKitty is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# HyperKitty is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Django-Mailman3.  If not, see <http://www.gnu.org/licenses/>.

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from django.test import TestCase, RequestFactory
from mock import Mock, patch
from openid.consumer import consumer


from django_mailman3.lib.auth.fedora.provider import (
    FedoraProvider, FedoraAccount)


class TestFedoraAccount(TestCase):
    """
    Test FedoraAccount social account.
    """

    def setUp(self):
        self.account = FedoraAccount('')

    def test_self_brand(self):
        self.assertEqual(self.account.get_brand(),
                         {'id': 'fedora', 'name': 'Fedora'})


class TestFedoraProvider(TestCase):
    """
    Test FedoraProvider openid authentication.
    """

    @patch('allauth.socialaccount.providers.openid.views._openid_consumer')
    def setUp(self, consumer_mock):
        self.factory = RequestFactory()
        client = Mock()
        complete = Mock()
        consumer_mock.return_value = client
        client.complete = complete
        self.complete_response = Mock()
        complete.return_value = self.complete_response
        self.complete_response.status = consumer.SUCCESS
        self.complete_response.identity_url = 'http://bob.id.fedoraproject.org'

    def test_get_login_url(self):
        req = self.factory.get('/')
        login_url = FedoraProvider(req).get_login_url(req)
        self.assertEqual(login_url, reverse('fedora_login'))
        login_url = FedoraProvider(req).get_login_url(req, query1='value1')
        new_url = reverse('fedora_login') + '?query1=value1'
        self.assertEqual(login_url, new_url)

    def test_extract_username(self):
        req = self.factory.get('/')
        username = FedoraProvider(req).extract_username(self.complete_response)
        self.assertEqual(username, 'bob')

    def test_extract_commmon_fields(self):
        # This this test we patch super(FedoraProvider, provider) so that it's
        # complicated extract_common_fields method is not called. It is too
        # complicated to try to find the return value and built a mock that
        # satisfies the request. The only relevant output from this we need is
        # a dictionary which is then extended by our FedoraProvider class.
        mock_parent = Mock()
        mock_parent.extract_common_fields.return_value = {}
        # To patch the superclass, we patch the super() builtin.
        with patch('builtins.super') as super_mock:
            super_mock.return_value = mock_parent
            req = self.factory.get('/')
            provider = FedoraProvider(req)
            res = provider.extract_common_fields(self.complete_response)
        self.assertEqual(res, {'username': 'bob'})

    def test_extract_email_addresses(self):
        with patch('django_mailman3.lib.auth.fedora.provider'
                   '.get_email_from_response') as email_mock:
            email_mock.return_value = 'testuser@example.com'
            req = self.factory.get('/')
            emails = FedoraProvider(req).extract_email_addresses(
                self.complete_response)
        self.assertEqual(len(emails), 2)
        self.assertEqual(sorted([x.email for x in emails]),
                         ['bob@fedoraproject.org', 'testuser@example.com'])
