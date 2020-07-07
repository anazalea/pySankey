# pySankey

Uses matplotlib to create simple <a href="https://en.wikipedia.org/wiki/Sankey_diagram">
Sankey diagrams</a> flowing only from left to right.

[![PyPI version](https://badge.fury.io/py/pySankeyBeta.svg)](https://badge.fury.io/py/pySankeyBeta)
[![Build Status](https://travis-ci.org/Pierre-Sassoulas/pySankey.svg?branch=master)](https://travis-ci.org/Pierre-Sassoulas/pySankey)
[![Coverage Status](https://coveralls.io/repos/github/Pierre-Sassoulas/pySankey/badge.svg?branch=master)](https://coveralls.io/github/Pierre-Sassoulas/pySankey?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Example

With fruits.txt :

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>true</th>
      <th>predicted</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>blueberry</td>
      <td>orange</td>
    </tr>
    <tr>
      <th>1</th>
      <td>lime</td>
      <td>orange</td>
    </tr>
    <tr>
      <th>2</th>
      <td>blueberry</td>
      <td>lime</td>
    </tr>
    <tr>
      <th>3</th>
      <td>apple</td>
      <td>orange</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>996</th>
      <td>lime</td>
      <td>orange</td>
    </tr>
    <tr>
      <th>997</th>
      <td>blueberry</td>
      <td>orange</td>
    </tr>
    <tr>
      <th>998</th>
      <td>orange</td>
      <td>banana</td>
    </tr>
    <tr>
      <th>999</th>
      <td>apple</td>
      <td>lime</td>
    </tr>
  </tbody>
</table>
<p>1000 rows × 2 columns</p>
</div>

You can generate a sankey's diagram with this code:

```python
import pandas as pd
from pysankey import sankey

df = pd.read_csv(
    'pysankey/fruits.txt', sep=' ', names=['true', 'predicted']
)
colorDict = {
    'apple':'#f71b1b',
    'blueberry':'#1b7ef7',
    'banana':'#f3f71b',
    'lime':'#12e23f',
    'orange':'#f78c1b',
    'kiwi':'#9BD937'
}

ax = sankey(
    df['true'], df['predicted'], aspect=20, colorDict=colorDict,
    leftLabels=['banana','orange','blueberry','apple','lime'],
    rightLabels=['orange','banana','blueberry','apple','lime','kiwi'],
    fontsize=12
)
plt.show() # to display
plt.savefig('fruit.png', bbox_inches='tight') # to save
```

![Fruity Alchemy](pysankey/fruit.png)

You could also use weight:

```
,customer,good,revenue
0,John,fruit,5.5
1,Mike,meat,11.0
2,Betty,drinks,7.0
3,Ben,fruit,4.0
4,Betty,bread,2.0
5,John,bread,2.5
6,John,drinks,8.0
7,Ben,bread,2.0
8,Mike,bread,3.5
9,John,meat,13.0
```

```python
import pandas as pd
from pysankey import sankey

df = pd.read_csv(
    'pysankey/customers-goods.csv', sep=',',
    names=['id', 'customer', 'good', 'revenue']
)
weight = df['revenue'].values[1:].astype(float)

ax = sankey(
      left=df['customer'].values[1:], right=df['good'].values[1:],
      rightWeight=weight, leftWeight=weight, aspect=20, fontsize=20
)
plt.show() # to display
plt.savefig('customers-goods.png', bbox_inches='tight') # to save
```

![Customer goods](pysankey/customers-goods.png)

Similar to seaborn, you can pass a matplotlib `Axes` to `sankey` function:
```python
import pandas as pd
from pysankey import sankey
import matplotlib.pyplot as plt

df = pd.read_csv(
        'pysankey/fruits.txt',
        sep=' ', names=['true', 'predicted']
)
colorDict = {
    'apple': '#f71b1b',
    'blueberry': '#1b7ef7',
    'banana': '#f3f71b',
    'lime': '#12e23f',
    'orange': '#f78c1b'
}

ax1 = plt.axes()

sankey(
      df['true'], df['predicted'], aspect=20, colorDict=colorDict,
      fontsize=12, ax=ax1
)

plt.show()
```

## Important informations

Use of `figureName`, `closePlot`, `figSize` in `sankey()` is deprecated and will be remove in a future version.
This is done so matplotlib is used more transparently as this [issue](https://github.com/anazalea/pySankey/issues/26#issue-429312025) on the original github repo suggested.

Now, `sankey` does less of the customization and let the user do it to their liking by returning a matplotlib `Axes` object, which mean the user also has access to the `Figure` to customise.
Then they can choose what to do with it - showing it, saving it with much more flexibility.

### Recommended changes to your code
 - To save a figure, one can simply do:
  ```python
    plt.savefig("<figureName>.png", bbox_inches="tight", dpi=150)
  ```

 - The `closePlot` is not needed anymore because without `plt.show()` after `sankey()`, no plot is displayed.
  You can still do `plt.close()` to be sure to not display this plot if you display other plots afterwards.

- You can modify the sankey size by changing the one from the matplotlib figure.
  ```python
    plt.gcf().set_size_inches(figSize)
  ```

## Package development

    pip3 install -e ".[test]"

### Lint

	pylint pysankey

### Testing

	python -m unittest

### Coverage

	coverage run -m unittest
	coverage html
	# Open htmlcov/index.html in a navigator
