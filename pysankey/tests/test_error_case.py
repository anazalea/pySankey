# -*- coding: utf-8 -*-

from pysankey import sankey
from pysankey.tests.test_fruit import TestFruit


class TestErrorCase(TestFruit):

    """ Test sankey's error case. """

    def test_bad_color_labels(self):
        """ sankey raise a value error when there is not enough color info"""
        bad_color_dict = {"apple": "#f71b1b", "orange": "#f78c1b"}
        with self.assertRaises(ValueError) as value_error:
            sankey(
                self.data["true"],
                self.data["predicted"],
                aspect=20,
                colorDict=bad_color_dict,
                fontsize=12,
                figureName=self.figure_name,
            )
        self.assertIn(": lime, blueberry, banana, kiwi", str(value_error.exception))
