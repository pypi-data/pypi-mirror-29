# pylint: disable=W,C,R

from collections import OrderedDict


from gitflow_wotw.parsers import ParserSource
from gitflow_wotw.constants import HIERARCHY
from gitflow_wotw.components import Subcommand


# class Command(SourceParser, HasDescendants):
class Command(ParserSource, Subcommand):
    IDENTIFIER = 'wotw'
    HELP_STRING = 'An ambitious attempt to duplicate gitflow-avh in Python'

    def __init__(self):
        Subcommand.__init__(
            self,
            self.IDENTIFIER,
            self.HELP_STRING,
            HIERARCHY[0]
        )
        ParserSource.__init__(
            self,
            self.IDENTIFIER,
            self.HELP_STRING,
            HIERARCHY[0]
        )

    def bootstrap(self, args=None):
        self.attach()
        known, unknown = self.parse_args(args)
        self.execute(known)
