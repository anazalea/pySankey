import matplotlib.pyplot as plt

from pysankey import sankey
from pysankey.tests.generic_test import TestFruit


class TestSankey(TestFruit):
    def test_right_color(self):
        ax = sankey(self.data["true"], self.data["predicted"], rightColor=True)
        self.assertIsInstance(ax, plt.Axes)
