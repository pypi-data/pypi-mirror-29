# pylint: disable=W,C,R

from __future__ import print_function

from gitflow_wotw.components import Argument


class ShowcommandsArgument(Argument):
    ARGS = ['--showcommands']
    KWARGS = {
        'action': 'store_true',
        'dest': 'showcommands',
        'help': 'Prints git commands as they are used'
    }

    def __init__(self):
        Argument.__init__(self, *self.ARGS, **self.KWARGS)
