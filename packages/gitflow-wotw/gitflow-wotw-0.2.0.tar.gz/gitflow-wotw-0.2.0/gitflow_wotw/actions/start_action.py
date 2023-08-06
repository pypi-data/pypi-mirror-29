# pylint:disable=W,C,R

from __future__ import print_function

from gitflow_wotw.components import Action
from gitflow_wotw.arguments import ShowcommandsArgument


class StartAction(Action):
    ACTION = 'start'
    HELP_STRING = 'Start a new something'

    def __init__(self):
        super(StartAction, self).__init__(self.ACTION, self.HELP_STRING)
        self.populate()

    def populate(self):
        self.arguments['showcommands'] = ShowcommandsArgument()

    def execute(self, parsed):
        print('Firing start!')
        print(parsed)
