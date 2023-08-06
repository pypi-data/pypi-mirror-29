# pylint: disable=W,C,R

from __future__ import print_function

from argparse import ArgumentParser
from sys import argv

from gitflow_wotw.constants import HIERARCHY
from gitflow_wotw.parsers import ParserNode


class ParserSource(ParserNode):

    def __init__(self, identifier=None, help_string=None, tier=None):
        if tier is None:
            tier = HIERARCHY[0]
        ParserNode.__init__(self, identifier, help_string, tier)

    def add_parser(self, subparsers=None):
        self.parser = ArgumentParser(
            description=self.help_string
        )

    def parse_args(self, args=None):
        if args is None:
            if argv[1:]:
                args = argv[1:]
            else:
                args = ['-h']
        return self.parser.parse_known_args(args)
