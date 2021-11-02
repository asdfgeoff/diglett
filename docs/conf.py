"""Sphinx configuration."""

import os
import sys

sys.path.insert(0, os.path.abspath('../src'))

print(os.getcwd())
print(sys.executable)

project = "diglett"
author = "Geoff Ruddock"
copyright = f"2021, {author}"
html_theme = "sphinx_book_theme"
html_theme_options = {"single_page": True}

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_book_theme",
]
