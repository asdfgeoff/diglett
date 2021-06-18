from setuptools import setup, find_packages

setup(name='Diglett',
      version='0.01',
      description='Tools for EDA and data munging.',
      url='https://github.com/asdfgeoff/Diglett',
      author='Geoff Ruddock',
      author_email='geoff@ruddock.ca',
      install_requires=['pandas', 'numpy', 'deprecated'],
      dependency_links=[],
      zip_safe=False,
      packages=['diglett'])
