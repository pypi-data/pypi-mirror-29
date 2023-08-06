# -*- coding: utf-8 -*-
#
# Copyright (C) 2017-2018 by the Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.


import time

from django.test import TestCase
from django_mailman3.lib.cache import CacheProxy


class TestCacheProxy(TestCase):

    def setUp(self):
        self.cache = CacheProxy()

    def test_cache(self):
        # First we set a new value.
        self.cache.set('foo', 'bar')
        self.assertEqual(self.cache.get('foo'), 'bar')
        # Now we set a timed cache.
        self.cache.set('key', 'value', timeout=2)
        time.sleep(2)
        self.assertIsNone(self.cache.get('key'))
        # Set an existing key.
        value = self.cache.get_or_set('foo', 'value')
        # We should get 'bar' as output as it is already set.
        self.assertEqual(value, 'bar')
        # Set a non-existent key using a callable value.
        value = self.cache.get_or_set('random-key', lambda: 'random-value')
        self.assertEqual(value, 'random-value')
        self.assertEqual(self.cache.get('random-key'), 'random-value')
        # Set a non-existent key with a timeout.
        value = self.cache.get_or_set('yes', lambda: 'no', timeout=2)
        time.sleep(2)
        self.assertIsNone(self.cache.get('yes'))
