# -*- coding: utf-8 -*-

import os
import unittest

import pandas as pd
from pysankey import sankey


class TestCustomerGoods(unittest.TestCase):

    def test_no_fail_readme(self):
        colorDict = {  # Color are random and ugly
            "customer": '#171b1b',
            "John": '#371b1b',
            "Mike": '#571b1b',
            "Betty": '#771b1b',
            "Ben": '#971b1b',
            "good": '#a71b1b',
            "fruit": '#c71b1b',
            "meat": '#fd1b1b',
            "drinks": '#e71b1b',
            "bread": '#f71b1b'
        }
        data = pd.read_csv(
            'pysankey/customers-goods.csv', sep=',',
            names=['id', 'customer', 'good', 'revenue']
        )
        # This is not working yet...
        sankey(
            left=data['customer'], right=data['good'],
            rightWeight=data['revenue'], aspect=20, colorDict=colorDict,
            fontsize=20, figureName="customer-good"
        )
        # Comment this to check the result
        if os.path.exists("customer-good.png"):
            os.remove("customer-good.png")
