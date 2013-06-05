from __future__ import print_function, absolute_import

import os
import shutil

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Deletes all of the cached copies of your markers from your MEDIA_ROOT.
    Note that on large sites where django-markers is heavily used, this can
    introduce a rather crushing performance hit, as it will force the
    recreation of all markers.
    """

    option_list = BaseCommand.option_list + (
        make_option(
            '--noinput',
            action='store_true',
            dest='noinput',
            default=False,
            help='Automatically assume "yes" to everything'
        ),
    )

    def handle(self, *args, **options):

        path = os.path.join(settings.MEDIA_ROOT, "cache", "markers")

        if not os.path.exists(path):
            return '\n  Your markers cache directory "%s" does not appear to exist.\n\n' % path

        response = None
        if not options["noinput"]:
            response = raw_input('\n  Deleting "%s", is that cool? (Y/n) ' % path)

        if not response or response == "y":
            shutil.rmtree(path)
            return '\n  Directory "%s" removed\n\n' % path
