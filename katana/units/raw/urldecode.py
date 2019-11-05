#!/usr/bin/env python3
from typing import Any
import urllib.request
import binascii
import magic

from katana.unit import NotApplicable, PrintableDataUnit
from katana.manager import Manager
from katana.target import Target
import katana.util
import regex as re

URL_DATA = re.compile(rb"%[0-9A-Fa-f]{1,2}", re.IGNORECASE | re.MULTILINE | re.DOTALL)


class Unit(PrintableDataUnit):

    # Moderate priority
    PRIORITY = 25

    def __init__(self, manager: katana.manager.Manager, target: katana.target.Target):
        super(Unit, self).__init__(manager, target)

        if URL_DATA.search(target.raw) is None:
            raise NotApplicable("No URL encoded parts")

    def evaluate(self, case):

        try:
            # Attempt to urldecode the data
            new_result = urllib.request.unquote(self.target.upstream.decode("utf-8"))
        except (UnicodeDecodeError, binascii.Error):
            # If this fails, it's probably not something we can deal with...
            return

        # We only want to work with this if it something new.
        if new_result.encode("utf-8") != self.target.raw:
            self.manager.register_data(self, new_result)
