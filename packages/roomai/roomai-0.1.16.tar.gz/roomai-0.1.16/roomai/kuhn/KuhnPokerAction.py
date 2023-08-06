import roomai.common

class KuhnPokerAction(roomai.common.AbstractAction):
    '''
    The KuhnPoker action used by the normal players. There are only two actions: bet and check. Examples of usages: \n
    >> import roomai.kuhn\n
    >> action = roomai.kuhn.KuhnPokerAction.lookup("bet")\n
    >> action.key\n
    "bet"\n
    >> action = roomai.kuhn.KuhnPokerAction.lookup("check")\n
    >> action.key\n
    "check"\n
    '''
    def __init__(self, key):
        super(KuhnPokerAction,self).__init__(key)
        self.__key__ = key

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the KuhnPoker action, \"bet\" or \"check\".")

    @classmethod
    def lookup(cls, key):
        return AllKuhnActions[key]

    def __deepcopy__(self, memodict={}, newinstance = None):
        return KuhnPokerAction.lookup(self.key)

AllKuhnActions = {"bet":KuhnPokerAction("bet"),"check":KuhnPokerAction("check")}
