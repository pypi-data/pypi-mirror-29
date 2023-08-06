#!/bin/python
import os
import roomai.common
import copy


#
#0, 1, 2, 3, ..., 7,  8, 9, 10, 11, 12, 13, 14
#^                ^   ^              ^       ^
#|                |   |              |       |
#3,               10, J, Q,  K,  A,  2,  r,  R
#

class DouDiZhuActionElement:
    str_to_rank  = {'3':0, '4':1, '5':2, '6':3, '7':4, '8':5, '9':6, 'T':7, 'J':8, 'Q':9, 'K':10, 'A':11, '2':12, 'r':13, 'R':14, 'x':15, 'b':16}
    # x means check, b means bid
    rank_to_str  = {0: '3', 1: '4', 2: '5', 3: '6', 4: '7', 5: '8', 6: '9', 7: 'T', 8: 'J', 9: 'Q', 10: 'K', 11: 'A', 12: '2', 13: 'r', 14: 'R', 15: 'x', 16: 'b'}

    number_of_pokercards = 15


class DouDiZhuPokerAction(roomai.common.AbstractAction):
    '''
     The DouDiZhuPoker action. The action contains two parts the license and the dipper. Examples of usages:\n
    >> import roomai.doudizhupoker\n
    >> action = roomai.doudizhupoker.SevenKingAction.lookup("55333444") \n
    >> ## We strongly recommend you to get an action with the lookup function.\n
    >> ## The lookup function inputs a string as the key. The key string needn't be sorted\n
    >> action.key \n
    "33344455"\n
    >> action.license\n
    "333444"\n
    >> action.dipper\n
    "55"\n
    >> action.pattern[0]\n
    p_6_2_1_2_0_1 
    '''
    def __init__(self):        pass

    def __init__(self, masterCards, slaveCards):

        self.__masterCards__         = [c for c in masterCards]
        self.__slaveCards__          = [c for c in slaveCards]
        self.__license__             = "".join(sorted([DouDiZhuActionElement.rank_to_str[c] for c in self.__masterCards__]))
        self.__dipper__              = "".join(sorted([DouDiZhuActionElement.rank_to_str[c] for c in self.__slaveCards__]))

        self.__masterPoints2Count__  = None
        self.__slavePoints2Count__   = None
        self.__isMasterStraight__    = None
        self.__maxMasterPoint__      = None
        self.__minMasterPoint__      = None
        self.__pattern__             = None

        self.__action2pattern__()
        self.__key__ = DouDiZhuPokerAction.__master_slave_cards_to_key__(masterCards, slaveCards)


    def __get_key__(self):  return self.__key__
    key = property(__get_key__, doc="The key of DouDiZhuPoker action. For example, key = \"333444\"")
    def __get_masterCards__(self):  return self.__masterCards__
    masterCards = property(__get_masterCards__, doc="The cards act as the master cards")
    def __get_slaveCards__(self):   return self.__slaveCards__
    slaveCards  = property(__get_slaveCards__, doc="The cards act as the slave cards")

    def __get_dipper__(self):   return self.__dipper__
    dipper = property(__get_dipper__, doc = "The dipper of the action. For example:\n"
                                              ">>a = roomai.doudizhupoker.DouDiZhuPokerAction.lookup(\"33344455\")\n"
                                              ">>a.dipper\n"
                                              ">>\"55\" ")

    def __get_license__(self): return self.__license__
    license = property(__get_license__, doc = "The license of the action. For example:\n"
                                                ">>a = roomai.doudizhupoker.DouDiZhuPokerAction.lookup(\"33344455\")\n"
                                                ">>a.license\n"
                                                ">>\"333444\"\n")


    def __get_masterPoints2Count__(self):   return self.__masterPoints2Count__
    masterPoints2Count = property(__get_masterPoints2Count__, doc="The count of different points in the masterCards")
    def __get_slavePoints2Count__(self):    return self.__slavePoints2Count__
    slavePoints2Count  = property(__get_slavePoints2Count__, doc="The count of different points in the slaveCards")
    def __get_isMasterStraight__(self):     return self.__isMasterStraight__
    isMasterStraight   = property(__get_isMasterStraight__, doc="The master cards are straight")
    def __get_maxMasterPoint__(self):       return self.__maxMasterPoint__
    maxMasterPoint     = property(__get_maxMasterPoint__, doc="The max point in the master cards")
    def __get_minMasterPoint__(self):       return self.__minMasterPoint__
    minMasterPoint     = property(__get_minMasterPoint__, doc="The min point in the master cards")
    def __get_pattern__(self):              return self.__pattern__
    pattern            = property(__get_pattern__, doc="The pattern of the action")

    @classmethod
    def lookup(cls, key):
        return AllActions["".join(sorted(key))]

    @classmethod
    def __master_slave_cards_to_key__(cls, masterCards, slaveCards):
        key_int = (masterCards + slaveCards)
        key_str = []
        for key in key_int:
            key_str.append(DouDiZhuActionElement.rank_to_str[key])
        key_str.sort()
        return "".join(key_str)

    def __action2pattern__(self):

        self.__masterPoints2Count__ = dict()
        for c in self.__masterCards__:
            if c in self.__masterPoints2Count__:
                self.__masterPoints2Count__[c] += 1
            else:
                self.__masterPoints2Count__[c] = 1

        self.__slavePoints2Count__ = dict()
        for c in self.__slaveCards__:
            if c in self.__slavePoints2Count__:
                self.__slavePoints2Count__[c] += 1
            else:
                self.__slavePoints2Count__[c] = 1

        self.__isMasterStraight__ = 0
        num = 0
        for v in self.__masterPoints2Count__:
            if (v + 1) in self.__masterPoints2Count__ and (v + 1) < DouDiZhuActionElement.str_to_rank["2"]:
                num += 1
        if num == len(self.__masterPoints2Count__) - 1 and len(self.__masterPoints2Count__) != 1:
            self.__isMasterStraight__ = 1

        self.__maxMasterPoint__ = -1
        self.__minMasterPoint__ = 100
        for c in self.__masterPoints2Count__:
            if self.__maxMasterPoint__ < c:
                self.__maxMasterPoint__ = c
            if self.__minMasterPoint__ > c:
                self.__minMasterPoint__ = c

        ########################
        ## action 2 pattern ####
        ########################


        # is cheat?
        if len(self.__masterCards__) == 1 \
                and len(self.__slaveCards__) == 0 \
                and self.__masterCards__[0] == DouDiZhuActionElement.str_to_rank["x"]:
            self.__pattern__ = AllPatterns["i_cheat"]

        # is roblord
        elif len(self.__masterCards__) == 1 \
                and len(self.__slaveCards__) == 0 \
                and self.__masterCards__[0] == DouDiZhuActionElement.str_to_rank["b"]:
            self.__pattern__ = AllPatterns["i_bid"]

        # is twoKings
        elif len(self.__masterCards__) == 2 \
                and len(self.__masterPoints2Count__) == 2 \
                and len(self.__slaveCards__) == 0 \
                and self.__masterCards__[0] in [DouDiZhuActionElement.str_to_rank["r"], DouDiZhuActionElement.str_to_rank["R"]] \
                and self.__masterCards__[1] in [DouDiZhuActionElement.str_to_rank["r"], DouDiZhuActionElement.str_to_rank["R"]]:
            self.__pattern__ = AllPatterns["x_rocket"]

        else:

            ## process masterCards
            masterPoints = self.__masterPoints2Count__
            if len(masterPoints) > 0:
                count = masterPoints[self.__masterCards__[0]]
                for c in masterPoints:
                    if masterPoints[c] != count:
                        self.__pattern__ = AllPatterns["i_invalid"]

            if self.__pattern__ == None:
                pattern = "p_%d_%d_%d_%d_%d" % (len(self.__masterCards__), len(masterPoints), \
                                                self.__isMasterStraight__, \
                                                len(self.__slaveCards__), 0)

                if pattern in AllPatterns:
                    self.__pattern__= AllPatterns[pattern]
                else:
                    self.__pattern__ = AllPatterns["i_invalid"]

    def __deepcopy__(self, memodict={}, newinstance = None):
        return self.lookup(self.key)



############## read data ################
AllPatterns = dict()
AllActions = dict()
from roomai.doudizhupoker import doudizhu_action_data
from roomai.doudizhupoker import doudizhu_pattern_data


for line in doudizhu_pattern_data:
    line = line.replace(" ", "").strip()
    line = line.split("#")[0]
    if len(line) == 0 or len(line[0].strip()) == 0:
        continue
    lines = line.split(",")
    for i in range(1, len(lines)):
        lines[i] = int(lines[i])
    AllPatterns[lines[0]] = lines


for line in doudizhu_action_data:
    line = line.replace(" ", "").strip()
    lines = line.split("\t")

    if lines[3] not in AllPatterns:
        continue

    m = [int(str1) for str1 in lines[1].split(",")]
    s = []
    if len(lines[2]) > 0:
        s = [int(str1) for str1 in lines[2].split(",")]
    action = DouDiZhuPokerAction(m, s)

    if "b" in line:
        b = 0
    if action.key != lines[0] or action.pattern[0] != lines[3]:
        raise ValueError("%s is wrong. The generated action has key(%s) and pattern(%s)"%(line, action.key,action.pattern[0]))

    AllActions[action.key] = action




