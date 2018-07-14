# -*- coding: utf-8 -*-

import unittest

import pandas as pd
from pysankey import sankey


class TestErrorCase(unittest.TestCase):

    def setUp(self):
        pd.options.display.max_rows = 8
        self.data = pd.read_csv(
            'pysankey/fruits.txt', sep=' ', names=['true', 'predicted']
        )

    def test_bad_color_labels(self):
        """ sankey raise a value error when there is not enough color info"""
        colorDict = {
            'apple':'#f71b1b',
            'orange':'#f78c1b'
        }
        self.assertRaises(ValueError, sankey,
            self.data['true'], self.data['predicted'], aspect=20,
            colorDict=colorDict, fontsize=12, figureName="fruit"
        )
