# -*- coding: utf-8 -*-

import pandas as pd

from pysankey.tests.generic_test import GenericTest


class TestCustomerGood(GenericTest):

    """ Permit to test sankey with the data in customers-goods.csv """

    def setUp(self):
        self.figure_name = "customer-good"
        self.data = pd.read_csv(
            "pysankey/customers-goods.csv",
            sep=",",
            names=["id", "customer", "good", "revenue"],
        )
