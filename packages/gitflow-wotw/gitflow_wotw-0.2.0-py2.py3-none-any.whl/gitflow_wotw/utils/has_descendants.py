# pylint:disable=W,C,R

from __future__ import print_function

from collections import OrderedDict


class HasDescendants(OrderedDict):

    def __init__(self, descendant_arg=None):
        super(HasDescendants, self).__init__()
        self.descendant_arg = descendant_arg

    def add_descendant(self, descendant):
        self[descendant.identifier] = descendant

    def execute(self, parsed_args=None):
        if hasattr(parsed_args, self.descendant_arg):
            desired_descendant = getattr(parsed_args, self.descendant_arg)
            if desired_descendant in self:
                self[desired_descendant].execute(parsed_args)
            else:
                raise ValueError(
                    "Unable to find the %s %s"
                    % (
                        desired_descendant,
                        self.descendant_arg
                    )
                )
        else:
            raise ValueError(
                "No %s discovered" % self.descendant_arg
            )
