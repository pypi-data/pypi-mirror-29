# -*- coding: utf-8 -*-
# Copyright (C) 2012-2018 by the Free Software Foundation, Inc.
#
# This file is part of Django-Mailman.
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
# Django-Mailman.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aurelien Bompard <abompard@fedoraproject.org>
#

from allauth.account.models import EmailAddress
from allauth.socialaccount import providers
from allauth.socialaccount.providers.openid.provider import (
    OpenIDAccount, OpenIDProvider)
from allauth.socialaccount.providers.openid.utils import (
    get_email_from_response)
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from django.utils.http import urlencode
from urllib.parse import urlparse


def extract_username(url):
    return urlparse(url).netloc.split('.')[0]


class FedoraAccount(OpenIDAccount):

    def get_brand(self):
        return dict(id='fedora', name='Fedora')

    def to_str(self):
        return extract_username(self.account.uid)


class FedoraProvider(OpenIDProvider):
    id = 'fedora'
    name = 'Fedora'
    account_class = FedoraAccount
    endpoint = 'https://id.fedoraproject.org'
    login_view = 'fedora_login'

    def get_login_url(self, request, **kwargs):
        url = reverse(self.login_view)
        if kwargs:
            url += '?' + urlencode(kwargs)
        return url

    def extract_username(self, data):
        """
        https://fedoraproject.org/wiki/OpenID
        For fedoraproject.org, the identity_url looks like:

        https://username.id.fedoraproject.org
        """
        return extract_username(data.identity_url)

    def extract_common_fields(self, data):
        fields = super(FedoraProvider, self).extract_common_fields(data)
        fields['username'] = self.extract_username(data)
        return fields

    def extract_email_addresses(self, data):
        """
        For example:

        [EmailAddress(email='john@doe.org',
                      verified=True,
                      primary=True)]
        """
        ret = []
        primary_email = get_email_from_response(data)
        if primary_email:
            # It would be added by cleanup_email_addresses(), but we add it
            # here to mark it as verified.
            ret.append(EmailAddress(
                email=primary_email, verified=True, primary=True))
        # Add the email alias provided by the Fedora project.
        ret.append(EmailAddress(
            email='%s@fedoraproject.org' % self.extract_username(data),
            verified=True, primary=False))
        return ret


providers.registry.register(FedoraProvider)
