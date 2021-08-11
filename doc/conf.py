import enum
import inspect
import os
import re

from sphinx.ext import autodoc

# PROJECT INFORMATION

project = 'xpx-chain'
copyright = '2020, ProximaX'
author = 'ProximaX'
version = ''
release = '0.6.7'

# GENERAL CONFIGURATION

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.ifconfig',
    'sphinx.ext.githubpages',
    'sphinx_autodoc_typehints',
]
add_module_names = False
autoclass_content = 'both'
autodoc_default_options = {
    'members': None,
    'undoc-members': None,
    'member-order': 'bysource',
}
exclude_patterns = []
language = None
master_doc = 'index'
pygments_style = None
source_suffix = '.rst'
templates_path = ['_templates']
set_type_checking_flag = True

# OPTIONS FOR HTML OUTPUT

html_theme = None
if os.environ.get('READTHEDOCS') != 'True':
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']

# OPTIONS FOR HTMLHELP OUTPUT

htmlhelp_basename = 'xpxchaindoc'

# OPTIONS FOR LATEX OUTPUT

latex_elements = {}
latex_documents = [
    (master_doc, 'xpxchain.tex', 'XPX Chain SDK Documentation',
     'ProximaX', 'manual'),
]

# OPTIONS FOR MANUAL PAGE OUTPUT

man_pages = [
    (master_doc, 'xpxchain', 'xpx Documentation',
     [author], 1)
]

# OPTIONS FOR TEXINFO OUTPUT

texinfo_documents = [
    (master_doc, 'xpxchain', 'XPX Chain SDK Documentation',
     author, 'xpxchain', 'One line description of project.',
     'Miscellaneous'),
]

# OPTIONS FOR EPUB OUTPUT

epub_title = project
epub_exclude_files = ['search.html']

# HANDLERS

def autodoc_skip_member_handler(app, what, name, obj, skip, options):
    """Skip members using camel case."""

    if inspect.ismodule(obj) or inspect.isclass(obj) or isinstance(obj, enum.EnumMeta):
        return skip
    # Skip all functions and properties with capital letters.
    return skip or re.search('[A-Z]', name) is not None


def is_function_or_method(obj):
    """Monkey-patch to skip classmethods and staticmethods in enums."""

    return any((
        autodoc.isfunction(obj),
        autodoc.isbuiltin(obj),
        inspect.ismethod(obj),
        isinstance(obj, classmethod),
        isinstance(obj, staticmethod),
    ))


autodoc.AttributeDocumenter.is_function_or_method = staticmethod(is_function_or_method)

def setup(app):
    """Connect handlers."""

    app.connect('autodoc-skip-member', autodoc_skip_member_handler)

