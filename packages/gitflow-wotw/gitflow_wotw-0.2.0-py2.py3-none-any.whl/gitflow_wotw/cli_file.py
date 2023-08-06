# pylint: disable=W,C,R

from gitflow_wotw.components import Command

from gitflow_wotw.subcommands import FeatureSubcommand


def cli():
    demo = Command()
    demo['feature'] = FeatureSubcommand()
    demo.bootstrap()
