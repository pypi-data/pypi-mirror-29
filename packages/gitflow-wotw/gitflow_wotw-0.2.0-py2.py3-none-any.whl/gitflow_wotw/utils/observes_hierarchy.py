# pylint:disable=W,C,R

from gitflow_wotw.constants import HIERARCHY


class ObservesHierarchy(object):

    __index = len(HIERARCHY)
    above = None
    below = None

    def __init__(self, tier=None):
        self.tier = tier
        self.consume_hierarchy()

    def validate_tier(self):
        self.__index = HIERARCHY.index(self.tier)

    def determine_above(self):
        if 0 == self.__index:
            self.above = None
        else:
            self.above = HIERARCHY[self.__index - 1]

    def determine_below(self):
        if len(HIERARCHY) - 1 <= self.__index:
            self.below = None
        else:
            self.below = HIERARCHY[self.__index + 1]

    def consume_hierarchy(self):
        self.validate_tier()
        self.determine_above()
        self.determine_below()
