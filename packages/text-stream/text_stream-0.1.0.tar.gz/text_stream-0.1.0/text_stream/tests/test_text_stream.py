#!/usr/bin/env python3
# Created at Mar 7, 2018, by Qi Zhang
"""
Test data is downloaded from
`github <https://github.com/georgeyumnam/quantum-espresso-codes/blob/master/2-Al/1_SCF/Al.pw.in>_`.
"""

import unittest
from io import StringIO
from pathlib import PurePath

from text_stream import *


class TestText(unittest.TestCase):
    def setUp(self):
        self.file = 'data/Al.pw.in'
        with open(self.file) as f:
            self.text = f.read()

    def test_type(self):
        a = make_text_stream(self.file)
        b = make_text_stream(self.text)
        self.assertTrue(isinstance(a, TextFileStream))
        self.assertTrue(isinstance(b, TextStream))
        self.assertTrue(isinstance(a.infile_path, PurePath))
        self.assertTrue(isinstance(b.stream, StringIO))

    def test_error(self):
        self.assertRaises(FileNotFoundError, TextFileStream, 'data/file_not_exists')
        self.assertRaises(TypeError, make_text_stream, 1)
