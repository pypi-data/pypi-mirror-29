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

import unittest

from email import policy, message_from_binary_file, message_from_file
from django_mailman3.lib.scrub import Scrubber
from django_mailman3.tests.utils import get_test_file
from traceback import format_exc


class TestScrubber(unittest.TestCase):

    def _check_html_attachment(self, value, expected):
        """
        Python's mimetype module does not give predictable results:
        https://mail.python.org/pipermail/python-list/2014-February/678963.html
        """
        self.assertEqual(value[0], expected[0])
        self.assertIn(value[1], ["attachment.html", "attachment.htm"])
        self.assertEqual(value[2:4], expected[2:4])

    def test_attachment_1(self):
        with open(get_test_file("attachment-1.txt")) as email_file:
            msg = message_from_file(email_file, policy=policy.SMTP)
        scrubber = Scrubber(msg)
        contents, attachments = scrubber.scrub()
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0], (
                2, 'puntogil.vcf', 'text/x-vcard', "utf-8",
                'begin:vcard\nfn:gil\nn:;gil\nversion:2.1\n'
                'end:vcard\n\n'))
        self.assertEqual(
            contents,
            "This is a test message.\n\n"
            "\n-- \ndevel mailing list\ndevel@lists.fedoraproject.org\n"
            "https://admin.fedoraproject.org/mailman/listinfo/devel\n"
            )

    def test_attachment_2(self):
        with open(get_test_file("attachment-2.txt")) as email_file:
            msg = message_from_file(email_file, policy=policy.SMTP)
        scrubber = Scrubber(msg)
        contents, attachments = scrubber.scrub()
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0], (
                3, 'signature.asc', 'application/pgp-signature', None,
                b'-----BEGIN PGP SIGNATURE-----\nVersion: GnuPG v1.4.12 '
                b'(GNU/Linux)\nComment: Using GnuPG with Mozilla - '
                b'http://www.enigmail.net/\n\niEYEARECAAYFAlBhm3oACgkQhmBj'
                b'z394AnmMnQCcC+6tWcqE1dPQmIdRbLXgKGVp\nEeUAn2OqtaXaXaQV7rx+'
                b'SmOldmSzcFw4\n=OEJv\n-----END PGP SIGNATURE-----\n'))
        self.assertEqual(
            contents,
            "This is a test message\nNon-ascii chars: Hofm\xfchlgasse\n"
            "\n-- \ndevel mailing list\ndevel@lists.fedoraproject.org\n"
            "https://admin.fedoraproject.org/mailman/listinfo/devel\n"
            )

    def test_attachment_3(self):
        with open(get_test_file("attachment-3.txt")) as email_file:
            msg = message_from_file(email_file, policy=policy.SMTP)
        scrubber = Scrubber(msg)
        contents, attachments = scrubber.scrub()
        self.assertEqual(len(attachments), 2)
        # HTML part
        self._check_html_attachment(
            attachments[0],
            (3, "attachment.html", "text/html", "iso-8859-1"))
        self.assertEqual(len(attachments[0][4]), 3114)
        # Image attachment
        self.assertEqual(
            attachments[1][0:4],
            (4, "GeoffreyRoucourt.jpg", "image/jpeg", None))
        self.assertEqual(len(attachments[1][4]), 282180)
        # Scrubbed content
        self.assertEqual(contents, "This is a test message\n\n\n")

    def test_html_email_1(self):
        with open(get_test_file("html-email-1.txt")) as email_file:
            msg = message_from_file(email_file, policy=policy.SMTP)
        scrubber = Scrubber(msg)
        contents, attachments = scrubber.scrub()
        self.assertEqual(len(attachments), 1)
        # HTML part
        self._check_html_attachment(
            attachments[0],
            (2, "attachment.html", "text/html", "iso-8859-1"))
        self.assertEqual(len(attachments[0][4]), 2688)
        # Scrubbed content
        self.assertEqual(
            contents,
            "This is a test message\n"
            "Non-ASCII chars: r\xe9ponse fran\xe7ais \n\n\n")

    def test_html_only_email(self):
        # This email only has an HTML part, thus the scrubbed content will be
        # empty. It should be an unicode empty string, not str.
        with open(get_test_file("html-email-2.txt")) as email_file:
            msg = message_from_file(email_file, policy=policy.SMTP)
        scrubber = Scrubber(msg)
        contents = scrubber.scrub()[0]
        self.assertTrue(
            isinstance(contents, str),
            "Scrubbed content should always be unicode")

    def _test_non_ascii_payload(self, enc):
        with open(get_test_file("payload-%s.txt" % enc), 'rb') as email_file:
            msg = message_from_binary_file(email_file, policy=policy.SMTP)
            scrubber = Scrubber(msg)
            contents = scrubber.scrub()[0]
            self.assertTrue(isinstance(contents, str))
            self.assertEqual(contents,
                'This message contains non-ascii characters:\n\xe9 \xe8 \xe7 \xe0 \xee \xef \xeb \u20ac\n'  # noqa
            )

    def test_non_ascii_payload_utf8(self):
        """Scrubber must handle non-ascii messages"""
        self._test_non_ascii_payload("utf8")

    def test_non_ascii_payload_iso8859(self):
        """Scrubber must handle non-ascii messages"""
        self._test_non_ascii_payload("iso8859")

    def test_bad_content_type(self):
        """Scrubber must handle unknown content-types"""
        with open(get_test_file("payload-unknown.txt")) as email_file:
            msg = message_from_file(email_file, policy=policy.SMTP)
        scrubber = Scrubber(msg)
        try:
            contents = scrubber.scrub()[0]
        except LookupError as e:
            import traceback
            print(traceback.format_exc())
            self.fail(e)  # codec not found
        self.assertTrue(isinstance(contents, str))

    def test_attachment_4(self):
        with open(get_test_file("attachment-4.txt")) as email_file:
            msg = message_from_file(email_file, policy=policy.SMTP)
        scrubber = Scrubber(msg)
        contents, attachments = scrubber.scrub()
        self.assertEqual(len(attachments), 2)
        # HTML part
        self._check_html_attachment(
            attachments[0],
            (3, "attachment.html", "text/html", "iso-8859-1"))
        self.assertEqual(len(attachments[0][4]), 113)
        # text attachment
        self.assertEqual(
            attachments[1][0:4],
            (4, "todo-déjeuner.txt", "text/plain", "utf-8"))
        self.assertEqual(len(attachments[1][4]), 110)
        # Scrubbed content
        self.assertEqual(
            contents,
            'This is a test, HTML message with '
            'accented letters : \xe9 \xe8 \xe7 \xe0.\nAnd an '
            'attachment with an accented filename\n\n\n\n\n')

    def test_attachment_5(self):
        with open(get_test_file("attachment-5.txt")) as email_file:
            msg = message_from_file(email_file, policy=policy.SMTP)
        scrubber = Scrubber(msg)
        contents, attachments = scrubber.scrub()
        self.assertEqual(len(attachments), 1)
        # text attachment
        self.assertEqual(
            attachments[0][0:4],
            (2, "todo-déjeuner.txt", "text/plain", "utf-8"))
        self.assertEqual(len(attachments[0][4]), 110)
        # Scrubbed content
        self.assertEqual(
            contents,
            'This is a test, HTML message with '
            'accented letters : \xe9 \xe8 \xe7 \xe0.\nAnd an '
            'attachment with an accented filename\n\n\n\n\n\n')

    def test_attachment_name_badly_encoded(self):
        with open(get_test_file("email-bad-filename.txt"), 'rb') as email_file:
            msg = message_from_binary_file(email_file, policy=policy.SMTP)
        scrubber = Scrubber(msg)
        try:
            attachments = scrubber.scrub()[1]
        except UnicodeDecodeError:
            print(format_exc())
            self.fail("Could not decode the filename")
        # The filename has non-ascii characters without the encoding specified,
        # Python will try to decode their name with best guess (ascii) and then
        # replace the characters that don't correspond to an ascii code
        # point. Then, we scrub the filename to allow only alpahun with dash,
        # underscore and dot.
        self.assertEqual(
            attachments,
            [(0, 'non-ascii-u3b5.jpg', 'text/plain', None, 'Dummy content\n')])

    def test_remove_next_part_from_content(self):
        with open(get_test_file("pipermail_nextpart.txt")) as email_file:
            msg = message_from_file(email_file, policy=policy.SMTP)
        scrubber = Scrubber(msg)
        contents = scrubber.scrub()[0]

        self.assertFalse("-------------- next part --------------" in contents)

    def test_name_unicode(self):
        for num in range(1, 6):
            with open(get_test_file("attachment-%d.txt" % num)) as email_file:
                msg = message_from_file(email_file, policy=policy.SMTP)
            scrubber = Scrubber(msg)
            attachments = scrubber.scrub()[1]
            for attachment in attachments:
                name = attachment[1]
                self.assertTrue(isinstance(name, str),
                                "attachment %r must be unicode" % name)
