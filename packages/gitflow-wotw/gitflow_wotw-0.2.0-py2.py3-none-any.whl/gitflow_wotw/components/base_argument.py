# pylint: disable=W,C,R

from __future__ import print_function


class Argument(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def attach_argument(self, parser=None):
        parser.add_argument(*self.args, **self.kwargs)
