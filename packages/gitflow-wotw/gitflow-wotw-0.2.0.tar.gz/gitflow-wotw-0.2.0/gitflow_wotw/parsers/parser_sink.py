# pylint: disable=W,C,R

from collections import OrderedDict

from gitflow_wotw.constants import HIERARCHY
from gitflow_wotw.utils import ObservesHierarchy


class ParserSink(ObservesHierarchy):

    def __init__(self, identifier=None, help_string=None, tier=None):
        if tier is None:
            tier = HIERARCHY[2]
        super(ParserSink, self).__init__(tier)
        self.identifier = identifier
        self.help_string = help_string
        self.parser = None
        self.arguments = OrderedDict()

    def add_parser(self, subparsers=None):
        self.parser = subparsers.add_parser(
            self.identifier,
            description=self.help_string,
            help=self.help_string
        )

    def attach_arguments(self):
        for _, value in self.arguments.items():
            value.attach_argument(self.parser)

    def attach(self, subparsers=None):
        self.add_parser(subparsers)
        self.attach_arguments()

    def print_help(self):
        self.parser.print_help()
