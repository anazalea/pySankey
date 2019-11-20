# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from pysankey import sankey
from pysankey.tests.generic_test import TestFruit, TestCustomerGood


class TestReadmeFruit(TestFruit):

    """ Test use case from README with the data in fruit.txt"""

    def test_no_fail_readme(self):
        ax = sankey(
            self.data["true"],
            self.data["predicted"],
            aspect=20,
            colorDict=self.colorDict,
            fontsize=12
        )
        self.assertIsInstance(ax, plt.Axes)


class TestReadmeCustomerGood(TestCustomerGood):

    """ Test use case from README with the data in customer-goods.csv"""

    def test_no_fail_readme(self):
        weight = self.data["revenue"].values[1:].astype(float)
        ax = sankey(
            left=self.data["customer"].values[1:],
            right=self.data["good"].values[1:],
            rightWeight=weight,
            leftWeight=weight,
            aspect=20,
            fontsize=10
        )
        self.assertIsInstance(ax, plt.Axes)
