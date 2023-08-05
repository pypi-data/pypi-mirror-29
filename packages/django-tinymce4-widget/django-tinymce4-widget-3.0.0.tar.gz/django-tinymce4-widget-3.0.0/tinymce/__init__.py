# coding: utf-8
# License: MIT, see LICENSE.txt
"""
django-tinymce4-lite
--------------------

This application provides a rich-text WYSIWYG `TinyMCE 4`_ widget
for Django forms and models.

.. _TinyMCE 4: https://www.tinymce.com/
"""

from __future__ import absolute_import, unicode_literals
from .models import HTMLField
from .widgets import TinyMCE, AdminTinyMCE

__all__ = ['HTMLField', 'TinyMCE', 'AdminTinyMCE']

VERSION = '3.0.0'
