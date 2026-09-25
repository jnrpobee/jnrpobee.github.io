#!/usr/bin/env python3
"""The markup of each page, one module per page.

A page module holds that page's HTML and nothing else, except where a
page has a little machinery of its own - the CV's download buttons.
The marks in the markup (<!--BLOGPOSTS--> and the rest) are filled in
by build.py from the modules that own them.

Each page keeps its own BODY dict and this file merges them, so adding
a page is two lines here and one new file - no long list to keep in
order, and nothing to rename if a page is dropped.
"""
BODY = {}

from . import home as _home
from . import research as _research
from . import projects as _projects
from . import publications as _publications
from . import about as _about
from . import blog as _blog
from . import cv as _cv
BODY.update(_home.BODY)
BODY.update(_research.BODY)
BODY.update(_projects.BODY)
BODY.update(_publications.BODY)
BODY.update(_about.BODY)
BODY.update(_blog.BODY)
BODY.update(_cv.BODY)

from .cv import CV_MARK, cv_actions  # noqa: E402  (the CV page owns these)
