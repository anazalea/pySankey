# -*- coding: utf-8 -*-

import pandas as pd
from pysankey.tests.generic_test import GenericTest


class TestCustomerGood(GenericTest):

    """ Permit to test sankey with the data in customers-goods.csv """

    def setUp(self):
        self.figure_name = "customer-good"
        self.data = pd.read_csv('pysankey/customers-goods.csv', sep=',',
                                names=['id', 'customer', 'good', 'revenue'])
        self.colorDict = {  # Color are random and ugly
            "customer": '#171b1b', "John": '#371b1b', "Mike": '#571b1b',
            "Betty": '#771b1b', "Ben": '#971b1b', "good": '#a71b1b',
            "fruit": '#c71b1b', "meat": '#fd1b1b', "drinks": '#e71b1b',
            "bread": '#f71b1b'
        }
