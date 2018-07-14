# -*- coding: utf-8 -*-

import os
import unittest

import pandas as pd
from pysankey import sankey


class TestFruit(unittest.TestCase):

    def test_no_fail_readme(self):
        pd.options.display.max_rows = 8
        data = pd.read_csv(
            'pysankey/fruits.txt', sep=' ', names=['true', 'predicted']
        )
        colorDict = {
            'apple':'#f71b1b',
            'blueberry':'#1b7ef7',
            'banana':'#f3f71b',
            'lime':'#12e23f',
            'orange':'#f78c1b'
        }
        sankey(
            data['true'], data['predicted'], aspect=20, colorDict=colorDict,
            fontsize=12, figureName="fruit"
        )
        # Comment this to check the result
        os.remove("fruit.png")
