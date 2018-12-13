# -*- coding: utf-8 -*-

import pandas as pd

from pysankey import sankey
from pysankey.tests.test_fruit import TestFruit


class TestReadmeFruit(TestFruit):
    def test_no_fail_readme(self):
        pd.options.display.max_rows = 8
        sankey(
            self.data["true"],
            self.data["predicted"],
            aspect=20,
            colorDict=self.colorDict,
            fontsize=12,
            figureName=self.figure_name,
        )
