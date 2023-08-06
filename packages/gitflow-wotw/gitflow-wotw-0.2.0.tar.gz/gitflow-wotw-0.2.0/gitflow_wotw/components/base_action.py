# pylint:disable=W,C,R

from gitflow_wotw.parsers import ParserSink


class Action(ParserSink):

    def execute(self, parsed):
        """A specific task to be defined by instances"""
