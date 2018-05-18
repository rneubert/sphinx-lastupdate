# -*- coding: utf-8 -*-
import datetime
import os
import subprocess


def _get_last_updated(app, pagename):
    """
    Pull the date from a git log call that represents the date a documentation
    page was last updated.
    """
    last_updated = None
    src_file = app.builder.env.doc2path(pagename)
    if os.path.exists(src_file):
        try:
            last_updated_t = subprocess.check_output(
                [
                    'git', 'log', '-n1', '--format=%ad', '--date=short',
                    '--', src_file,
                ]
            ).decode('utf-8').strip()
            last_updated = datetime.datetime.strptime(last_updated_t,
                                                      '%Y-%m-%d')
        except (ValueError, subprocess.CalledProcessError):
            pass
    return last_updated


def html_page_context(app, pagename, templatename, context, doctree):
    context['last_updated'] = _get_last_updated(app, pagename)


def setup(app):
    app.connect('html-page-context', html_page_context)
