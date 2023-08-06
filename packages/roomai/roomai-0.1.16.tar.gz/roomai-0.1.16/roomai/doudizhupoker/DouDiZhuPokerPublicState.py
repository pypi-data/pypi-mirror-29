#!/bin/python
import os
import roomai.common
from roomai.doudizhupoker.DouDiZhuPokerAction import DouDiZhuActionElement
import copy



class DouDiZhuPokerPublicState(roomai.common.AbstractPublicState):
    '''
    The public state of DouDiZhuPoker
    '''
    def __init__(self):
        super(DouDiZhuPokerPublicState, self).__init__()
        self.__landlord_candidate_id__ = -1
        self.__landlord_id__ = -1
        self.__license_playerid__ = -1
        self.__license_action__ = None
        self.__continuous_cheat_num__ = 0
        self.__is_response__ = False

        self.__keep_cards__ = None
        self.__first_player__ = -1
        self.__phase__ = -1
        self.__epoch__ = -1

    def __get_landlord_candidate_id__(self):    return self.__landlord_candidate_id__
    landlord_candidate_id = property(__get_landlord_candidate_id__, doc = "The candiate landlord player id during the betting_for_be_landlord phase")

    def __get_landlord_id__(self):  return self.__landlord_id__
    landlord_id = property(__get_landlord_id__, doc = "The landlord player id.")
    def __get_license_playerid__(self): return self.__license_playerid__
    license_playerid = property(__get_license_playerid__, doc="The license player id."+
                                                               " During the \"playing\" phase, if is_response is True, the current player need take an valid action with the same pattern as the license action, which was taken by the license player. "+
                                                              "Unless, he takes the check action. If two continuous cheat actions are taken, is_response will be false, so that the current player needn't response the license action and can take any valid action")

    def __get_license_action__(self):   return self.__license_action__
    license_action = property(__get_license_action__, doc="The license action.  During the \"playing\" phase, if is_response is True, the current player need take an valid action with the same pattern as the license action, which was taken by the license player. "+
                                                      "Unless, he takes the check action. If two continuous cheat actions are taken, is_response will be false, so that the current player needn't response the license action and can take any valid action")

    def __get_continuous_cheat_num__(self): return self.__continuous_cheat_num__
    continuous_cheat_num = property(__get_continuous_cheat_num__, doc="The number of the continuous cheat actions.During the \"playing\" phase, if is_response is True, the current player need take an valid action with the same pattern as the license action, which was taken by the license player. "+
                                                      "Unless, he takes the check action. If two continuous cheat actions are taken, is_response will be false, so that the current player needn't response the license action and can take any valid action")

    def __get_is_response__(self):  return  self.__is_response__
    is_response = property(__get_is_response__, doc = "is_response.  During the \"playing\" phase, if is_response is True, the current player need take an valid action with the same pattern as the license action, which was taken by the license player. "
                                                      "Unless, he takes the check action. If two continuous cheat actions are taken, is_response will be false, so that the current player needn't response the license action and can take any valid action")

    def __get_keep_cards__(self):   return self.__keep_cards__
    keep_cards = property(__get_keep_cards__, doc = "The keep cards")

    def __get_first_player__(self): return self.__first_player__
    first_player = property(__get_first_player__, doc = "The players[first_player] is first to take an action")

    def __get_phase__(self):    return self.__phase__
    phase = property(__get_phase__,
                     doc = "There are two stages in DouDiZhu, namely 0) betting for being the landlord and 1) playing the game.\n"+
                           "0 denotes the betting for being the landlord phase, 1 denotes the playing the game phase.\n")

    def __get_epoch__(self):    return self.__epoch__
    epoch = property(__get_epoch__, doc = "The epoch denotes the count about a player takes an action.")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = DouDiZhuPokerPublicState()
        newinstance = super(DouDiZhuPokerPublicState, self).__deepcopy__(newinstance=newinstance)

        newinstance.__landlord_candidate_id__ = self.landlord_candidate_id
        newinstance.__landlord_id__ = self.landlord_id
        newinstance.__license_playerid__ = self.license_playerid
        if self.license_action is None:
            newinstance.__license_action__  = None
        else:
            newinstance.__license_action__ = self.license_action.__deepcopy__()
        newinstance.__continuous_cheat_num__ = self.continuous_cheat_num
        newinstance.__is_response__ = self.is_response

        if self.keep_cards == None:
            newinstance.__keep_cards__ = None
        else:
            newinstance.__keep_cards__ = self.keep_cards.__deepcopy__()

        newinstance.__first_player__ = self.first_player
        newinstance.__phase__ = self.phase
        newinstance.__epoch__ = self.epoch

        return newinstance