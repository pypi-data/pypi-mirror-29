import os
import pkg_resources


__version__ = pkg_resources.get_distribution(
    'lsst_sphinx_bootstrap_theme').version
__version_full__ = __version__


def get_html_theme_path():
    """Path (str) of the sphinx HTML theme.

    In a project's ``conf.py``,

    ::
       html_theme_path = [lsst_sphinx_bootstrap_theme.get_html_theme_path()]
    """
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_html_templates_path():
    """Path of reST templates provided with this theme.

    In a project's ``conf.py``,

    ::
       templates_path = ['_templates',
                         lsst_sphinx_bootstrap_theme.get_html_templates_path()]
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        'templates'))
