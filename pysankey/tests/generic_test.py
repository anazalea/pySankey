# -*- coding: utf-8 -*-

import os
import unittest

import pandas as pd


class GenericTest(unittest.TestCase):

    """ Generic tests for sankey

    If figure_name is used, the resulting images
    will be removed at the end of the tests. """

    @classmethod
    def setUpClass(cls):
        cls.figure_name = ''
        cls.data = ''
        cls.colorDict = ''

    def tearDown(self):
        path = "{}.png".format(self.figure_name)
        # Comment this to check the resulting image
        if os.path.exists(path):
            os.remove(path)


class TestFruit(GenericTest):

    """ Base test to test with the data in fruit.txt """

    def setUp(self):
        self.figure_name = "fruit"
        self.data = pd.read_csv(
            "pysankey/fruits.txt", sep=" ", names=["true", "predicted"]
        )
        self.colorDict = {
            "apple": "#f71b1b",
            "blueberry": "#1b7ef7",
            "banana": "#f3f71b",
            "lime": "#12e23f",
            "orange": "#f78c1b",
            "kiwi": "#9BD937",
        }

class TestCustomerGood(GenericTest):

    """ Base test to test with the data in customers-goods.csv """

    def setUp(self):
        self.figure_name = "customer-good"
        self.data = pd.read_csv(
            "pysankey/customers-goods.csv",
            sep=",",
            names=["id", "customer", "good", "revenue"],
        )
