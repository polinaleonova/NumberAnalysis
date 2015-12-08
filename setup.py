from setuptools import setup, find_packages
import setuptools
import py2exe
import number_analysis

setup(
    windows=[{'script': "number_analysis.py"}],
    zipfile=None,
    options={
        'py2exe': {
            'includes': 'cairo, gobject, gtk.keysyms, gtk, gio, pango, pangocairo, atk'
        }
    },
)
