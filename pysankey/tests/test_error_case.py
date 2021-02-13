# -*- coding: utf-8 -*-

from pysankey import LabelMismatch, NullsInFrame, sankey
from pysankey.tests.generic_test import TestFruit


class TestErrorCase(TestFruit):

    """ Test sankey's error case. """

    def test_bad_color_labels(self):
        """ sankey raise a value error when there is not enough color info"""
        bad_color_dict = {"apple": "#f71b1b", "orange": "#f78c1b"}
        with self.assertRaises(ValueError) as value_error:
            sankey(self.data["true"], self.data["predicted"], colorDict=bad_color_dict)
        self.assertIn(": lime, blueberry, banana, kiwi", str(value_error.exception))

    def test_label_mismatch(self):
        """ sankey raises a LabelMismatch when data doesn't match the labels"""
        with self.assertRaises(LabelMismatch):
            sankey(
                self.data["true"],
                self.data["predicted"],
                leftLabels=["banana", "orange", "blueberry", "apple", "lime"],
                rightLabels=["orange", "banana", "blueberry", "apple"],
            )

    def test_nulls_in_frame(self):
        """ sankey raises a NullsInFrame when left or right data is null"""
        with self.assertRaises(NullsInFrame):
            sankey([None], self.data["predicted"])
