#!/bin/python
import os
import roomai.common
from roomai.doudizhupoker.DouDiZhuPokerAction import DouDiZhuActionElement
import copy



class DouDiZhuPokerPersonState(roomai.common.AbstractPersonState):
    '''
    The person state of DouDiZhu game environment
    '''
    def __init__(self):
        self.__hand_cards__        = None

    def __get_hand_cards__(self):
        return self.__hand_cards__

    hand_cards = property(__get_hand_cards__, doc="The cards in the hand of the corresponding player. For example, hand_cards = [444555rR]")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = DouDiZhuPokerPersonState()

        newinstance = super(DouDiZhuPokerPersonState, self).__deepcopy__(newinstance=newinstance)
        if self.hand_cards is None:
            newinstance.__hand_cards__ = None
        else:
            newinstance.__hand_cards__ = self.hand_cards.__deepcopy__()

        return newinstance