# -*- coding: utf-8 -*-

from pysankey import sankey
from pysankey.tests.test_customer_goods import TestCustomerGood


class TestReadmeCustomerGood(TestCustomerGood):
    def test_no_fail_readme(self):
        # This is not working yet...
        weight = self.data["revenue"].values[1:].astype(float)
        sankey(
            left=self.data["customer"].values[1:],
            right=self.data["good"].values[1:],
            rightWeight=weight,
            leftWeight=weight,
            aspect=20,
            fontsize=10,
            figureName=self.figure_name,
        )
