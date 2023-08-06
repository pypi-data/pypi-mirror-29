# pylint: disable=W,C,R

from __future__ import print_function

from sys import exit as sys_exit

from gitflow_wotw.actions import StartAction
from gitflow_wotw.components import Subcommand


class FeatureSubcommand(Subcommand):
    SUBCOMMAND = 'feature'
    HELP_STRING = 'Manages feature branches'

    def __init__(self):
        super(
            FeatureSubcommand,
            self
        ).__init__(
            self.SUBCOMMAND,
            self.HELP_STRING
        )
        # print(dir(self))
        # sys_exit(1)
        self.populate()

    def populate(self):
        self['start'] = StartAction()
