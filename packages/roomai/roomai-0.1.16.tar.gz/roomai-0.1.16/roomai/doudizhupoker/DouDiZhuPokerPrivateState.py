#!/bin/python
import os
import roomai.common
from roomai.doudizhupoker.DouDiZhuPokerAction import DouDiZhuActionElement
import copy

class DouDiZhuPokerPrivateState(roomai.common.AbstractPrivateState):
    def __init__(self):
        self.__keep_cards__ = None

    def __get_keep_cards__(self):   return self.__keep_cards__
    keep_cards = property(__get_keep_cards__, doc = "A DouDiZhuPokerHandCards class about the keep cards")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = DouDiZhuPokerPrivateState()
        newinstance.__keep_cards__ = self.keep_cards.__deepcopy__()
        return newinstance
