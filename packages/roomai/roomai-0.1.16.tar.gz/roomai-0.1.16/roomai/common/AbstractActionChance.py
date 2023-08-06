#!/bin/python
#coding=utf8

import roomai
import roomai.common
logger = roomai.get_logger()



class AbstractActionChance(object):
    '''
    The abstract class of an chance action. The chance action is used by the chance player.
    '''

    def __init__(self, key):
        self.__key__ = key

    def __get_key__(self):
        return self.__key__

    key = property(__get_key__, doc="The key of the chance action. Every chance action in RoomAI has a key as its identification."
                                    " We strongly recommend you to use the lookup function to get an chance action with the specified key")

    @classmethod
    def lookup(self, key):
        '''
        Get an action with the specified key. \n
        We strongly recommend you to use the lookup function to get an action with the specified key, rather than use the constructor function.\n

        :param key: the specified key
        :return:  the action with the specified key
        '''
        raise NotImplementedError("Not implemented")

    def __deepcopy__(self, memodict={}, newinstance=None):
        if newinstance is None:
            newinstance = AbstractActionChance()
        newinstance.__key__ = self.__key__
        return newinstance
