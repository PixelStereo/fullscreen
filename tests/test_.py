#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os, sys
from time import sleep

sys.path.append(os.path.abspath("./../"))

from svp import new_display, new_player

player = new_player('a player')
display = new_display('a display')
preview = new_display('another display')

class TestAll(unittest.TestCase):

    def test_display(self):
        player = new_player
        self.assertEqual(debug, 3)

    def test_player(self):
        uni = u"22"
        uni = checkType(uni)
        self.assertEqual(isinstance(uni, int), True)
        uni = u"22.22"
        uni = checkType(uni)
        self.assertEqual(isinstance(uni, float), True)
        uni = u"twenty-two-22"
        uni = checkType(uni)

if __name__ == "__main__":
    unittest.main()
