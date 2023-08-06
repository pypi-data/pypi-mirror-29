#!/bin/python
#coding:utf-8
import roomai.common
import roomai.bridge
import random
import roomai.bridge
from functools import cmp_to_key
import logging


class BridgeEnv(roomai.common.AbstractEnv):
    '''
    The Bridge game environment
    '''


    def init(self, params = dict()):

        if "start_turn" in params:
            self.__params__["start_turn"] = params["start_turn"]
        else:
            self.__params__["start_turn"] = int(random.random() * 4)

        if self.__params__["start_turn"] not in [roomai.bridge.Direction.north,roomai.bridge.Direction.east, roomai.bridge.Direction.south,roomai.bridge.Direction.west]:
            raise ValueError("start_turn is %s, not one of [roomai.bridge.Direction.north,roomai.bridge.Direction.east, roomai.bridge.Direction.south,roomai.bridge.Direction.west]"%(str(self.__params__["start_turn"])))


        if "vulnerable" in params:
            self.__params__["vulnerable"] = list(params["vulnerable"])
        else:
            self.__params__["vulnerable"] = [False for i in range(4)]

        if len(self.__params__["vulnerable"]) != 4:
            raise ValueError("len(self.__params__[\"vulnerable\"]) != 4")

        if self.__params__["vulnerable"][roomai.bridge.Direction.south] != self.__params__["vulnerable"][roomai.bridge.Direction.north]:
            raise ValueError("The north and south players have different vulnerable states. (north vulnerable: %s, south vulnerable: %s)"%(str(self.__params__["vulnerable"][roomai.bridge.Direction.north]),str(self.__params__["vulnerable"][roomai.bridge.Direction.south])))

        if self.__params__["vulnerable"][roomai.bridge.Direction.west]  != self.__params__["vulnerable"][roomai.bridge.Direction.east]:
            raise ValueError("The east and west players have different vulnerable states. (north vulnerable: %s, south vulnerable: %s)"%(str(self.__params__["vulnerable"][roomai.bridge.Direction.north]),str(self.__params__["vulnerable"][roomai.bridge.Direction.south])))

        if "num_normal_players" in params:
            logger = roomai.get_logger()
            logger.warning("Bridge is a game of 4 normal players. Ingores the \"num_normal_players\" option")
        self.__params__["num_normal_players"] = 4

        self.public_state                        = roomai.bridge.BridgePublicState()
        self.public_state.__stage__              = "bidding"
        self.public_state.__turn__               = self.__params__["start_turn"]
        self.public_state.__playing_is_vulnerable__ = list(self.__params__["vulnerable"])

        self.person_states = [roomai.bridge.BridgePersonState() for i in range(5)]
        for i in range(5):
            self.person_states[i].__id__ = i
        num = int(len(roomai.bridge.AllBridgePlayingPokerCards) / 4)

        allcards = list(roomai.bridge.AllBridgePlayingPokerCards.values())
        #allcards.sort(key = cmp_to_key(roomai.bridge.BridgePlayingPokerCard.compare))
        random.shuffle(allcards)
        for i in range(4):
            self.person_states[i].__hand_cards_dict__ = dict()
            for card in allcards[i*num:(i+1)*num]:
                self.person_states[i].__hand_cards_dict__[card.key] = card
        self.person_states[self.public_state.turn].__available_actions__ \
            = self.available_actions(self.public_state, self.person_states[self.public_state.turn])


        self.private_state = roomai.bridge.BridgePrivateState()

        self.__gen_state_history_list__()
        return self.__gen_infos__(), self.public_state, self.person_states, self.private_state

    def forward(self, action):
        '''
        The Bridge game go forward with this action
        
        :param action: 
        :return: 
        '''

        pu  = self.public_state
        pes = self.person_states
        pr  = self.private_state
        if self.is_action_valid(action, pu, pes[pu.turn]) == False:
            raise ValueError("%s is invalid action"%(action.key))
        pes[pu.turn].__available_actions__ = dict()
        pu.__action_history__.append((pu.turn, action))

        if pu.stage == "bidding": ## the bidding stage
            if len(pu.action_history) == 4:
                flag = True
                for i in range(4):
                    flag = flag and (pu.action_history[i][1].bidding_option == "pass")
                if flag == True:
                    pu.__is_terminal__ = True
                    pu.__scores__      = [0,0,0,0]
                    self.__gen_state_history_list__()
                    return self.__gen_infos__(), self.public_state, self.person_states, self.private_state

            if action.bidding_option == "pass":
                if len(pu.action_history) > 3 \
                    and pu.action_history[-2][1].bidding_option == "pass"\
                    and pu.action_history[-3][1].bidding_option == "pass":
                        self.__bidding_to_playing__(action)
                else:
                    self.__bidding_process_pass__(action)
            elif action.bidding_option == "bid":
                self.__bidding_process_bid__(action)
            elif action.bidding_option == "double":
                self.__bidding_process_double__(action)
            elif action.bidding_option == "redouble":
                self.__bidding_process_redouble__(action)
            else:
                raise  ValueError("In the bidding stage, the action's bidding_option must be one of \"pass\",\"bid\",\"double\" and \"redouble\". But a \"%s\" action is found"%(action.key))


        elif pu.stage == "playing": ## the playing stage
            pu.__playing_cards_on_table__.append(action.playing_card)
            self.__remove_card_from_hand_cards__(pes[pu.playing_card_turn], action.playing_card)

            if len(pu.playing_cards_on_table) == 4:
                playerid1,playerid2 = self.__whois_winner_per_pier__(pu)
                logger = roomai.get_logger()
                if logger.level <= logging.DEBUG:
                    logger.debug("The winners of this pier are %d and %d"%(playerid1,playerid2))

                pu.__playing_win_tricks_sofar__[playerid1] += 1
                pu.__playing_win_tricks_sofar__[playerid2] += 1
                pu.__playing_cards_on_table__ = []
                if len(pes[pu.playing_card_turn].hand_cards_dict) == 0:
                    pu.__is_terminal__ = True
                    self.__compute_score__()
                else:
                    pu.__playing_card_turn__ = playerid1
                    pu.__turn__                = playerid1
                    if pu.__playing_card_turn__ == (pu.__playing_dealerid__ + 2)%4:
                        pu.__turn__ = playerid2

                    pes[pu.__turn__].__available_actions__ = BridgeEnv.available_actions(public_state= pu, person_state=pes[pu.playing_card_turn])
            else:
                pu.__playing_card_turn__ = (pu.__playing_card_turn__ + 1) % 4
                if pu.playing_card_turn == (pu.playing_dealerid + 2)%4:
                    pu.__turn__ = (pu.playing_card_turn + 2) % 4
                else:
                    pu.__turn__ = pu.playing_card_turn
                pes[pu.turn].__available_actions__ = BridgeEnv.available_actions(public_state=pu, person_state=pes[pu.playing_card_turn])

        else:
            raise ValueError("The public_state.stage = %d is invalid"%(self.public_state.stage))


        self.__gen_state_history_list__()
        return self.__gen_infos__(), self.public_state,self.person_states, self.private_state

    def __remove_card_from_hand_cards__(self, person_state, card):
        del person_state.__hand_cards_dict__[card.key]

    def __compare_card_with_contract_suit__(self, card1, card2, contract_suit):
        if card1.suit == contract_suit and card2.suit == contract_suit:
            return roomai.bridge.BridgeBiddingPokerCard.compare(card1, card2)
        elif card1.suit == contract_suit and card2.suit != contract_suit:
            return 1
        elif card1.suit != contract_suit and card2.suit == contract_suit:
            return -1
        else:
            return roomai.bridge.BridgeBiddingPokerCard.compare(card1, card2)

    def __compute_score__(self):
        '''
        https://zh.wikipedia.org/wiki/%E6%A9%8B%E7%89%8C%E8%A8%88%E5%88%86
        
        :return: 
        '''
        pu = self.public_state
        pu.__scores__ = [0, 0, 0, 0]
        playing_point_rank = pu.playing_contract_card.point_rank
        excessive_tricks = pu.playing_win_tricks_sofar[pu.playing_dealerid]  - 6 - playing_point_rank

        if excessive_tricks >= 0:
            ####
            tricks_score     = 0
            if pu.playing_contract_card.suit == "NotTrump":
                tricks_score = (excessive_tricks * 30 + 10) * pu.playing_magnification
            elif pu.playing_contract_card.suit == "Spade" or pu.playing_contract_card.suit == "Heart":
                tricks_score = excessive_tricks * 30 * pu.playing_magnification
            elif pu.playing_contract_card.suit == 'Diamond' or pu.playing_contract_card.suit == 'Club':
                tricks_score = excessive_tricks * 20
            else:
                raise ValueError("%s is not valid playing_contract_suit (NotTrump, Spade, Heart, Diamond, Club)"%(pu.playing_contract_suit))
            pu.__scores__[pu.playing_dealerid] = tricks_score
            pu.__scores__[(pu.playing_dealerid + 2)%4] = tricks_score

            ####
            stage_score = 0
            if pu.playing_is_vulnerable[pu.playing_dealerid] == True:
                if tricks_score < 100:
                    stage_score = 50
                else:
                    stage_score = 500

                if playing_point_rank == 6:
                    stage_score += 750
                if playing_point_rank == 7:
                    stage_score += 1500
            else:
                if tricks_score < 100:
                    stage_score = 50
                else:
                    stage_score = 300

                if playing_point_rank == 6:
                    stage_score += 500
                if playing_point_rank == 7:
                    stage_score += 1000
            pu.__scores__[pu.playing_dealerid] += stage_score
            pu.__scores__[(pu.playing_dealerid + 2) % 4] += stage_score

            #####
            extensive_trick_score = 0
            if pu.playing_magnification == 1:
                if pu.playing_contract_card.suit == "NotTrump" \
                        or pu.playing_contract_card.suit == "Spade" \
                        or pu.playing_contract_card.suit == "Heart":
                    extensive_trick_score = excessive_tricks * 30
                else:
                    extensive_trick_score = excessive_tricks * 20
            elif pu.playing_magnification == 2:
                if pu.playing_is_vulnerable[pu.playing_dealerid] == True:
                    extensive_trick_score = excessive_tricks * 200
                else:
                    extensive_trick_score = excessive_tricks * 100
            elif pu.playing_magnification == 4:
                if pu.playing_is_vulnerable[pu.playing_dealerid] == True:
                    extensive_trick_score = excessive_tricks * 400
                else:
                    extensive_trick_score = excessive_tricks * 200
            pu.__scores__[pu.playing_dealerid] += extensive_trick_score
            pu.__scores__[(pu.playing_dealerid + 2) % 4] += extensive_trick_score


        else:
            penalty_trick = -excessive_tricks
            penalty_score = 0
            if pu.playing_is_vulnerable[(pu.playing_dealerid + 1)%4] == True:
                if pu.playing_magnification == 1:
                    penalty_score = 100 * penalty_trick
                elif pu.playing_magnification == 2:
                    if penalty_trick == 1:
                        penalty_score = 200
                    elif penalty_trick  in [2,3]:
                        penalty_score = 200 + (penalty_trick-1) * 300
                    elif penalty_trick >= 4:
                        penalty_score = 200 + 300 * 2 + (penalty_trick-3) * 300
                elif pu.playing_magnification == 4:
                    if penalty_trick == 1:
                        penalty_score = 400
                    elif penalty_trick  in [2,3]:
                        penalty_score = 400 + (penalty_trick-1) * 600
                    elif penalty_trick >= 4:
                        penalty_score = 400 + 600 * 2 + (penalty_trick-3) * 600
            else:
                if pu.playing_magnification == 1:
                    penalty_score = 50 * penalty_trick
                elif pu.playing_magnification == 2:
                    if penalty_trick == 1:
                        penalty_score = 100
                    elif penalty_trick  in [2,3]:
                        penalty_score = 100 + (penalty_trick-1) * 200
                    elif penalty_trick >= 4:
                        penalty_score = 100 + 200 * 2 + (penalty_trick-3) * 300
                elif pu.playing_magnification == 4:
                    if penalty_trick == 1:
                        penalty_score = 200
                    elif penalty_trick  in [2,3]:
                        penalty_score = 200 + (penalty_trick-1) * 400
                    elif penalty_trick >= 4:
                        penalty_score = 200 + 400 * 2 + (penalty_trick-3) * 600
            pu.__scores__[(pu.playing_dealerid+1)%4] += penalty_score
            pu.__scores__[(pu.playing_dealerid+3)%4] += penalty_score



    def __whois_winner_per_pier__(self, pu):
        max_id   = pu.action_history[-1][0]
        max_card = pu.playing_cards_on_table[-1]
        for i in range(2,5):
            if self.__compare_card_with_contract_suit__(max_card, pu.playing_cards_on_table[-i], pu.playing_contract_card.suit) < 0:
                max_id   = pu.action_history[-i][0]
                max_card = pu.playing_cards_on_table[-i]

        return max_id, (max_id + 2)%4

    def __bidding_process_pass__(self, action):
        pu = self.public_state

        pu.__previous_id__ = pu.turn
        pu.__previous_action__ = action
        pu.__turn__ = (pu.turn + 1) % 4

        self.person_states[pu.turn].__available_actions__ = self.available_actions(pu,self.person_states[pu.turn])

    def __bidding_process_double__(self, action):
        pu = self.public_state
        pu.__bidding_magnification__ = 2

        pu.__previous_id__ = pu.turn
        pu.__previous_action__ = action
        pu.__turn__ = (pu.turn + 1) % 4

        self.person_states[pu.turn].__available_actions__ = self.available_actions(pu,self.person_states[pu.turn])

    def __bidding_process_redouble__(self, action):
        pu = self.public_state
        pu.__bidding_magnification__ = 4

        pu.__previous_id__ = pu.turn
        pu.__previous_action__ = action
        pu.__turn__ = (pu.turn + 1) % 4

        self.person_states[pu.turn].__available_actions__ = self.available_actions(pu,self.person_states[pu.turn])

    def __bidding_process_bid__(self, action):
        pu = self.public_state
        pu.__bidding_candidate_contract_card__ = action.bidding_card
        pu.__bidding_last_bidder__ = pu.turn
        pu.__bidding_magnification__ = 1

        pu.__previous_id__ = pu.turn
        pu.__previous_action__ = action
        pu.__turn__ = (pu.turn + 1) % 4

        self.person_states[pu.turn].__available_actions__ = self.available_actions(pu,self.person_states[pu.turn])

    def __bidding_to_playing__(self, action):
        pu = self.public_state
        pu.__stage__                  = "playing"
        pu.__playing_contract_card__  = pu.bidding_candidate_contract_card
        pu.__playing_magnification__  = pu.bidding_magnification

        start_turn  = self.__params__["start_turn"]
        last_bidder = pu.bidding_last_bidder
        for i in range(len(pu.action_history)):
            if (i+start_turn)%4 == last_bidder or (i + start_turn + 2) % 4 == last_bidder:
                if pu.action_history[i][1].bidding_option == "bid" \
                        and pu.action_history[i][1].bidding_card.suit == pu.playing_contract_card.suit:
                    pu.__playing_dealerid__ = i
                    break

        pu.__turn__ = (pu.playing_dealerid +1)%4
        pu.__playing_card_turn__ = (pu.playing_dealerid + 1)%4
        self.person_states[pu.turn].__available_actions__ = self.available_actions(pu,self.person_states[pu.turn])


    @classmethod
    def __available_contract__(self, pu, card):

        if pu.bidding_candidate_contract_card is None:
            return True
        elif card.point_rank > pu.bidding_candidate_contract_card.point_rank:
            return True
        elif card.point_rank == pu.bidding_candidate_contract_card.point_rank:
            if card.suit_rank > pu.bidding_candidate_contract_card.point_rank:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def is_action_valid(cls, action, public_state, person_state):
        return action.key in person_state.available_actions

    @classmethod
    def available_actions(cls, public_state, person_state):
        if public_state.stage == "bidding": ## the bidding stage
            available_actions = dict()
            for card in roomai.bridge.AllBridgeBiddingPokerCards.values():
                    if BridgeEnv.__available_contract__(public_state, card) == True:
                        key = "bidding_bid_%s"%(card.key)
                        available_actions[key] = roomai.bridge.BridgeAction.lookup(key)
            available_actions["bidding_pass"] = roomai.bridge.BridgeAction.lookup("bidding_pass")

            if len(public_state.__action_history__) >= 1:
                pre_action  = public_state.__action_history__[-1][1]
                if pre_action.bidding_option == "bid":
                    key = "bidding_double"
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)

                if pre_action.bidding_option == "double":
                    key = "bidding_redouble"
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)

            if len(public_state.__action_history__) >= 3:
                pre_action1 = public_state.__action_history__[-1][1]
                pre_action2 = public_state.__action_history__[-2][1]
                pre_action3 = public_state.__action_history__[-3][1]
                if pre_action3.bidding_option == "bid" and pre_action2.bidding_option == "pass" and pre_action1.bidding_option == "pass":
                    key = "bidding_double"
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)

            return available_actions


        elif public_state.stage == "playing": ## the playing stage
            available_actions = dict()
            if public_state.playing_cards_on_table == tuple([]) or public_state.playing_cards_on_table is None:
                for card in list(person_state.hand_cards_dict.values()):
                    key = "playing_%s"%(card.key)
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)
            else:
                for card in person_state.hand_cards_dict.values():
                    if len(public_state.playing_cards_on_table) == 0:
                        x = 0
                    if card.suit == public_state.playing_cards_on_table[0].suit:
                        key = "playing_%s" % (card.key)
                        available_actions[key] = roomai.bridge.BridgeAction.lookup(key)

            if len(available_actions) == 0:
                for card in person_state.hand_cards_dict.values():
                    key = "playing_%s" % (card.key)
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)

            return available_actions

        else:
            raise ValueError("The public_state.stage = %s is invalid. The public_state.stage must be one of [\"bidding\",\"playing\"]"%(public_state.stage))


    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = BridgeEnv()
        newinstance = super(BridgeEnv, self).__deepcopy__(newinstance=newinstance)
        return newinstance