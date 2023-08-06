# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018 by the Free Software Foundation, Inc.
#
# This file is part of Django-Mailman.
#
# Django-Mailman3 is a free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Django-Mailman3 is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Django-Mailman.  If not, see <http://www.gnu.org/licenses/>.

import os
import re

from enum import Enum
from mimetypes import guess_all_extensions
from email.errors import HeaderParseError
from email.header import make_header, decode_header
from email.message import EmailMessage

# Path characters for common platforms
PRE = re.compile(r'[/\\:]')
# All other characters to strip out of Content-Disposition: filenames
# (essentially anything that isn't an alphanum, dot, dash, or underscore).
SRE = re.compile(r'[^-\w.]')
# Regexp to strip out leading dots
DRE = re.compile(r'^\.*')

NEXT_PART = re.compile(r'--------------[ ]next[ ]part[ ]--------------\n')


class Sanitize(Enum):
    """
    Enum to denote whether the HTML message should be scrubbed.
    """
    SANITIZE_HTML = 1


def oneline(header_string):
    """Inspired by mailman.utilities.string.oneline"""
    try:
        h = make_header(decode_header(header_string))
        ustr = str(h)
        return ''.join(ustr.splitlines())
    except (LookupError, UnicodeError, ValueError, HeaderParseError):
        # possibly charset problem. return with undecoded string in one line.
        return ''.join(header_string.splitlines())


class Scrubber():
    """
    Given an EmailMessage, extract all the attachments including text/html
    parts and return the text.
    """

    sanitize = Sanitize.SANITIZE_HTML

    def __init__(self, msg):
        assert isinstance(msg, EmailMessage)
        self.msg = msg

    def scrub(self):
        """Given a EmailMessage, extracts the text from the body and all the
        attachments.

        Returns a tuple (result, attachments), in which attachments is a list
        of all the attachments and result is unicode text of the message body.

        """
        attachments = self._get_all_attachments()
        text = self._get_text()
        return (text, attachments)

    def _get_all_attachments(self):
        attachments = []
        # We iterate over all the attachments using the new iter_attachments
        # API in EmailMessage. This returns all immediate children parts that
        # are not candidate body parts.
        for part_num, part in enumerate(self.msg.walk()):
            ctype = part.get_content_type()
            # Messages will *always* return a value for get_content_type, even
            # if message doesn't have one. If there is no content_type defined,
            # text/plain is returned for most message. In case of
            # multipart/digest, it is message/rfc822.
            if ctype == 'text/plain':
                if part.is_attachment():
                    attachments.append(self._parse_attachment(part, part_num))
                    part.set_content('')
            elif (ctype == 'text/html' and self.sanitize ==
                  Sanitize.SANITIZE_HTML):
                attachments.append(self._parse_attachment(part, part_num))
                part.set_content('')
            elif ctype == 'message/rfc822':
                attachments.append(self._parse_attachment(part, part_num))
                part.set_content('')
            elif part.get_payload() and not part.is_multipart():
                attachments.append(self._parse_attachment(part, part_num))
        return attachments

    def _get_charset(self, msg, default='ascii', guess='False'):
        """
        Returns the charset of a EmailMessage part.

        If there is no charset defined, try to guess by decoding with certain
        common types.

        :param msg: The EmailMessage message to return charset for.
        :type msg: EmailMessage
        :param default: The charset to be assumed as default if none is defined
        :type default: str
        :param guess: Boolean defining whether we should try to guess the
                      charset.
        :type guess: Bool
        """
        if msg.get_content_charset():
            return msg.get_content_charset()
        if msg.get_charset():
            return msg.get_charset()
        charset = default
        if not guess:
            # Do not try to guess the charset and just return the default.
            return charset
        text = msg.get_payload(decode=True)
        for encoding in ['ascii', 'utf8', 'iso8859-15']:
            try:
                text.decode(encoding)
            except UnicodeDecodeError:
                continue
            else:
                charset = encoding
                break
        return charset

    def _parse_attachment(self, part, part_num, filter_html=True):
        """
        Decode the attachment.

        :param part: Attachment to be parsed.
        :type part: EmailMessage
        :param part_num: An attachment numerical identifier
        :type part_num: int
        :filter_html: Whether filter HTML content from the text of attachment.
        :type filter_html: Bool
        """
        ctype = part.get_content_type()
        # Get the charset of the message, if not set, try to guess it's value.
        # When guess is True, it will never return None.
        charset = self._get_charset(part, default=None, guess=False)
        payload = part.get_content()
        # get_content can give either bytes or str, based on whether it was
        # able to decode the payload. If it is str, return it as it is,
        # otherwise, try to decode it using the guessed charset.
        if not isinstance(payload, str):
            decodedpayload = part.get_payload(decode=True)
        else:
            # It is also a str, just return it as it is.
            decodedpayload = payload
        filename = self._get_attachment_filename(part, ctype)
        if ctype == 'message/rfc822':
            decodedpayload = str(decodedpayload)
        return (part_num, filename, ctype, charset, decodedpayload)

    def _guess_all_extensions(self, ctype):
        """
        Given the attachment's content-type, try to guess its file extension.
        """
        # mimetypes maps multiple extensions to the same type, e.g. .doc, .dot,
        # and .wiz are all mapped to application/msword.  This sucks for
        # finding the best reverse mapping.  If the extension is one of the
        # giving mappings, we'll trust that, otherwise we'll just guess. :/
        all_exts = guess_all_extensions(ctype, strict=False)
        return all_exts and all_exts[0]

    def _get_attachment_filename(self, part, ctype):
        # Try to get the filename using the default `get_filename()`
        # API.
        try:
            filename = oneline(part.get_filename(''))
        except (TypeError, UnicodeDecodeError):
            # Workaround for https://bugs.launchpad.net/mailman/+bug/1060951
            # (accented filenames).
            # In Python3 get_filename decodes the filename with
            # `errors=replace` which means, that if there are non-ascii
            # characters in the filename, they are replaced with '?'.
            filename = 'attachment.bin'

        filename, fext = os.path.splitext(filename)
        ext = fext or self._guess_all_extensions(ctype)
        # Now that we have a guessed extension and if it returned no values,
        # let's cook up some extensions depending on the content type.
        if not ext:
            if ctype == 'message/rfc822':
                ext = '.txt'
            else:
                ext = '.bin'
        # Remove anything other than alphanum, dot, dash or underscore.
        ext = SRE.sub('', ext)
        if not filename:
            # Use attachment as default filename if there is none.
            filebase = 'attachment'
        else:
            # Sanitize the filename given in the message headers.
            parts = PRE.split(filename)
            filename = parts[-1]
            # Strip off the leading dots.
            filename = DRE.sub('', filename)
            # Allow only alphanumerics, dash, underscore, and dot
            # i18n filenames are not supported yet,
            # see https://bugs.launchpad.net/bugs/1060951
            filename = SRE.sub('', filename)
            # If the filename's extension doesn't match the type we guessed,
            # which one should we go with?  For now, let's go with the one we
            # guessed so attachments can't lie about their type.  Also, if the
            # filename /has/ no extension, then tack on the one we guessed.
            # The extension was removed from the name above.
            filebase = filename
        return filebase + ext

    def _get_text_one_part(self, msg):
        """
        Returns decoded payload for a non-multipart message.
        """
        # MAS: TypeError exception can occur if payload is None. This
        # was observed with a message that contained an attached
        # message/delivery-status part. Because of the special parsing
        # of this type, this resulted in a text/plain sub-part with a
        # null body. See bug 1430236.
        charset = self._get_charset(msg, guess=True)
        payload = msg.get_payload(decode=True)
        try:
            result = payload.decode(charset)
        except (UnicodeDecodeError, LookupError, ValueError, AssertionError):
            result = payload.decode('utf-8', 'replace')
        next_part_match = NEXT_PART.search(result)
        if next_part_match:
            result = result[0:next_part_match.start(0)]
        return result

    def _get_text(self):
        if self.msg.is_multipart():
            # We now want to concatenate all the parts which have been scrubbed
            # to text/plain, into a single text/plain payload.  We need to make
            # sure all the characters in the concatenated string are in the
            # same encoding, so we'll use the 'replace' key in the coercion
            # call.
            # BAW: Martin's original patch suggested we might want to try
            # generalizing to utf-8, and that's probably a good idea
            # (eventually).
            text = []
            for part in self.msg.walk():
                # Walk through the message and collect all the plaintext parts
                # and leave all the multiparts.
                if part.is_multipart():
                    continue
                ctype = part.get_content_type()
                # Ignore anything other text/plain and text/html
                if ctype != 'text/plain' and (
                        ctype != 'text/html' or self.sanitize != 2):
                    continue
                part_content = self._get_text_one_part(part)
                if isinstance(part_content, str):
                    if not part_content.endswith('\n'):
                        part_content += '\n'
                text.append(part_content)
            return '\n'.join(text)
        else:
            return self._get_text_one_part(self.msg)
