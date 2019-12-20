import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='diglett',
    version='0.1.0',
    author='Geoff Ruddock',
    python_requires='>=3.6.0',
    description='Useful python functions for digging through new datasets',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/asdfgeoff/diglett',
    license='MIT',
    packages=['diglett'],
    install_requires=[
          'pandas',
          'numpy',
          'matplotlib',
          'seaborn',
          'scikit-learn',
          'IPython'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ]
)
