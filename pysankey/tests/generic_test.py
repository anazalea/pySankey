# -*- coding: utf-8 -*-

import os
import unittest


class GenericTest(unittest.TestCase):

    """ Generic tests for sankey, figure_name is used the resulting images
    will be removed at the end of the tests. """

    def tearDown(self):
        path = "{}.png".format(self.figure_name)
        # Comment this to check the resulting image
        if os.path.exists(path):
            os.remove(path)
