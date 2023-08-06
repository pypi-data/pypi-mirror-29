# pylint:disable=W,C,R

from collections import OrderedDict

from gitflow_wotw.parsers import ParserNode
from gitflow_wotw.utils import HasDescendants


class Subcommand(ParserNode, HasDescendants, OrderedDict):

    def __init__(self, identifier=None, help_string=None, tier=None):
        OrderedDict.__init__(self)
        ParserNode.__init__(self, identifier, help_string, tier)
        HasDescendants.__init__(self, self.below)

    def attach_below(self):
        for _, descendant in self.items():
            descendant.attach(self.subparsers)

    def print_help_below(self):
        for _, descendant in self.items():
            descendant.print_help()
