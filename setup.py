# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['diglett']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.26.0,<8.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'pandas>=1.3.1,<2.0.0',
 'plotly>=5.1.0,<6.0.0',
 'seaborn>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'diglett',
    'version': '0.2.0',
    'description': 'Tools for data wrangling',
    'long_description': None,
    'author': 'Geoff Ruddock',
    'author_email': 'geoff@ruddock.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
