# -*- coding: utf-8 -*-

from pysankey import sankey
from pysankey.tests.test_customer_goods import TestCustomerGood


class TestReadmeCustomerGood(TestCustomerGood):

    def test_no_fail_readme(self):
        # This is not working yet...
        sankey(left=self.data['customer'], right=self.data['good'],
               rightWeight=self.data['revenue'], aspect=20,
               fontsize=20, figureName=self.figure_name)
