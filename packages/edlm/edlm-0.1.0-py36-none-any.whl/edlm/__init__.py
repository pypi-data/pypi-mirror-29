# coding=utf-8
"""
Etcher's Document Library Manager
"""
from pathlib import Path
import warnings

import elib
from pkg_resources import DistributionNotFound, get_distribution

LOGGER = elib.custom_logging.get_logger('EDLM', log_to_file=True)
elib.custom_logging.activate_elib_logging()

HERE = Path(__file__).parent.parent.absolute()

try:
    __version__ = get_distribution('edlm').version
except DistributionNotFound:  # pragma: no cover
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            from setuptools_scm import get_version
            __version__ = get_version()
    except (ImportError, ModuleNotFoundError):
        __version__ = 'not installed'
