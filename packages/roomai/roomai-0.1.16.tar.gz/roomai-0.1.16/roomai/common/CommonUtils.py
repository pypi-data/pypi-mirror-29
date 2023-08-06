#!/bin/python
#coding=utf8

import roomai
import roomai.common
logger = roomai.get_logger()


############################################################### Some Utils ############################################################################

point_str_to_rank  = {'2':0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12, 'r':13, 'R':14}
point_rank_to_str  = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A', 13: 'r', 14: 'R'}
suit_str_to_rank   = {'Spade':0, 'Heart':1, 'Diamond':2, 'Club':3,  'ForKing':4}
suit_rank_to_str   = {0:'Spade', 1: 'Heart', 2: 'Diamond', 3:'Club', 4:'ForKing'}
class PokerCard(object):
    '''
    A Poker Card. \n
    A Poker Card has a point (2,3,4,....,K,A,r,R) and a suit (Spade, Heart, Diamond, Club, ForKing). \n
    Different points have different ranks, for example the point 2's rank is 0, and the point A's rank is 12. \n
    Different suits have different ranks too. The "ForKing" suit is a placeholder used for the card with the point "r" or "R".\n
    A Poker Card has a key (point_suit). We strongly recommend you to get a poker card by using the class function lookup with the key. \n
    Examples of the class usages: \n
    >> import roomai.common \n
    >> card = roomai.common.PokerCard.lookup("2_Spade") \n
    >> card.point \n
    2\n
    >> card.suit\n
    Spade\n
    >> card.point_rank\n
    0\n
    >> card.suit_rank\n
    0\n
    >> card.key\n
    "2_Spade"\n
    '''
    def __init__(self, point, suit = None):
        point1 = 0
        suit1  = 0
        if suit is None:
            kv = point.split("_")
            point1 = point_str_to_rank[kv[0]]
            suit1  = suit_str_to_rank[kv[1]]
        else:
            point1 = point
            if isinstance(point, str):
                point1 = point_str_to_rank[point]
            suit1  = suit
            if isinstance(suit, str):
                suit1 = suit_str_to_rank[suit]

        self.__point__  = point_rank_to_str[point1]
        self.__suit__   = suit_rank_to_str[suit1]
        self.__point_rank__ = point1
        self.__suit_rank__  = suit1
        self.__key__        = "%s_%s" % (self.__point__, self.__suit__)


    def __get_point_str__(self):
        return self.__point__
    point = property(__get_point_str__, doc="The point of the poker card")

    def __get_suit_str__(self):
        return self.__suit__
    suit = property(__get_suit_str__, doc="The suit of the poker card")

    def __get_point_rank__(self):
        return self.__point_rank__
    point_rank = property(__get_point_rank__, doc="The point rank of the poker card")

    def __get_suit_rank__(self):
        return self.__suit_rank__
    suit_rank = property(__get_suit_rank__, doc="The suit rank of the poker card")

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the poker card")


    @classmethod
    def lookup(cls, key):
        '''
        lookup a PokerCard with the specified key
        
        :param key: The specified key
        :return: The PokerCard with the specified key
        '''
        return AllPokerCards[key]

    @classmethod
    def point_to_rank(cls, point):
        if point not in point_str_to_rank:
            raise ValueError("%s is invalid poker point for PokerCard")
        return point_str_to_rank[point]

    @classmethod
    def suit_to_rank(cls, suit):
        if suit not in suit_str_to_rank:
            raise ValueError("%s is invalid poker suit for PokerCard")
        return suit_str_to_rank[suit]

    @classmethod
    def rank_to_point(cls, rank):
        if rank not in point_rank_to_str:
            raise  ValueError("%d is invalid poker point rank for PokerCard")
        return point_rank_to_str[rank]

    @classmethod
    def rank_to_suit(cls, rank):
        if rank not in suit_rank_to_str:
            raise ValueError("%d is invalid poker suit rank for PokerCard")
        return suit_rank_to_str[rank]

    @classmethod
    def compare(cls, pokercard1, pokercard2):
        '''
        Compare two poker cards with their point ranks and suit ranks.
        The poker card with the higher point rank has the higher rank.
        With the same point rank, the poker card with the higher suit rank has the higher rank.
        
        :param pokercard1: 
        :param pokercard2: 
        :return: A number, which is >0 when the poker card1 has the higher rank than the poker card2, =0 when their share the same rank, <0 when the poker card1 has the lower rank than the poker card2
        
        '''
        pr1 = pokercard1.point_rank
        pr2 = pokercard2.point_rank

        if pr1 != pr2:
            return pr1 - pr2
        else:
            return pokercard1.suit_rank - pokercard2.suit_rank


    def __deepcopy__(self,  memodict={}, newinstance = None):
        return   AllPokerCards[self.key]


AllPokerCards = dict()
AllPokerCards_Without_King = dict()
for point in point_str_to_rank:
    if point != 'r' and point != "R":
        for suit in suit_str_to_rank:
            if suit != "ForKing":
                AllPokerCards["%s_%s" % (point, suit)] = PokerCard("%s_%s" % (point, suit))
                AllPokerCards_Without_King["%s_%s" % (point, suit)] = PokerCard("%s_%s" % (point, suit))
AllPokerCards["r_ForKing"] = (PokerCard("r_ForKing"))
AllPokerCards["R_ForKing"] = (PokerCard("R_ForKing"))




class FrozenDict(dict):
    def __setitem__(self, key, value):
        raise NotImplementedError("The FrozenDict doesn't support the __setitem__ function")

