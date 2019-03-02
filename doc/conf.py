import enum
import inspect
import os
import re

# PROJECT INFORMATION

project = 'nem2'
copyright = '2019, NEM Foundation'
author = 'NEM Foundation'
version = ''
release = '0.0.1'

# GENERAL CONFIGURATION

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.ifconfig',
    'sphinx.ext.githubpages',
    'sphinx_autodoc_typehints',
]
add_module_names = False
autodoc_member_order = 'bysource'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = []
pygments_style = None

# OPTIONS FOR HTML OUTPUT

html_theme = None
if os.environ.get('READTHEDOCS') != 'True':
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']

# OPTIONS FOR HTMLHELP OUTPUT

htmlhelp_basename = 'nem2doc'

# OPTIONS FOR LATEX OUTPUT

latex_elements = {}
latex_documents = [
    (master_doc, 'nem2.tex', 'nem2 Documentation',
     'NEM Foundation', 'manual'),
]

# OPTIONS FOR MANUAL PAGE OUTPUT

man_pages = [
    (master_doc, 'nem2', 'nem2 Documentation',
     [author], 1)
]

# OPTIONS FOR TEXINFO OUTPUT

texinfo_documents = [
    (master_doc, 'nem2', 'nem2 Documentation',
     author, 'nem2', 'One line description of project.',
     'Miscellaneous'),
]

# OPTIONS FOR EPUB OUTPUT

epub_title = project
epub_exclude_files = ['search.html']

# HANDLERS

def autodoc_skip_member_handler(app, what, name, obj, skip, options):
    """Skip members using camel case."""

    if inspect.ismodule(obj) or inspect.isclass(obj) or isinstance(obj, enum.Enum):
        return skip
    # Skip all functions and properties with capital letters.
    return skip or re.search('[A-Z]', name) is not None


def setup(app):
    """Connect handlers."""

    app.connect('autodoc-skip-member', autodoc_skip_member_handler)
