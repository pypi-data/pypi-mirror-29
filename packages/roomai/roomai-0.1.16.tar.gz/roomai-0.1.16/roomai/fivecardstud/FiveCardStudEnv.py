#!/bin/python
#coding:utf-8
import roomai.common
import copy
import logging
import random
import sys
from functools import cmp_to_key


from roomai.fivecardstud   import FiveCardStudPokerCard
from roomai.fivecardstud   import FiveCardStudPublicState
from roomai.fivecardstud   import FiveCardStudPersonState
from roomai.fivecardstud   import FiveCardStudPrivateState
from roomai.fivecardstud   import FiveCardStudAction

class FiveCardStudEnv(roomai.common.AbstractEnv):
    '''
    FiveCardStud game enviroment
    '''

    #@override
    def init(self, params = dict()):
        '''
        Initialize FiveCardStud game enviroment with the params. The params are as follows:
        1) num_normal_players denotes how many players join in this game, default 3
        2) chips denotes the initialization chips of players, default [500,500,500]
        3) floor_bet denotes the minimal bet, default 10
        4) backward_enable denotes whether the environment will stores all history information. If you need call the backward function, please set it to bet True. default False
        An example of params is {"num_normal_players":3,"chips":[500,500,500]}
        
        :param params: initialization param
        :return: infos, public_state, person_states, private_state
        '''
        self.logger         = roomai.get_logger()

        self.__params__     = dict()
        if "num_normal_players" in params:
            self.__params__["num_normal_players"] = params["num_normal_players"]
        else:
            self.__params__["num_normal_players"] = 3

        if "chips" in params:
            self.__params__["chips"]       = params["chips"]
        else:
            self.__params__["chips"]       = [500 for i in range(self.__params__["num_normal_players"])]

        if "floor_bet" in params:
            self.__params__["floor_bet"]   = params["floor_bet"]
        else:
            self.__params__["floor_bet"]   = 10

        if "backward_enable" in params:
            self.__params__["backward_enable"] = params["backward_enable"]
        else:
            self.__params__["backward_enable"] = False


        allcards = []
        for i in range(13):
            for j in range(4):
                allcards.append(FiveCardStudPokerCard(i, j))
        random.shuffle(allcards)


        FiveCardStudEnv.__valid_initialization_params__(self)

        self.public_state   = FiveCardStudPublicState()
        self.private_state  = FiveCardStudPrivateState()
        self.person_states  = [FiveCardStudPersonState() for i in range(self.__params__["num_normal_players"]+1)]

        self.public_state_history  = []
        self.private_state_history = []
        self.person_states_history = []



        ## private_state
        self.private_state.all_hand_cards      = allcards[0: 5 * self.__params__["num_normal_players"]]

        ## public_state
        self.public_state.num_normal_players   = self.__params__["num_normal_players"]
        self.public_state.chips                = self.__params__["chips"]
        self.public_state.second_hand_cards    = self.private_state.all_hand_cards[1*self.__params__["num_normal_players"]:  2 * self.__params__["num_normal_players"]]
        self.public_state.floor_bet            = self.__params__["floor_bet"]
        self.public_state.upper_bet            = min(self.public_state.chips)
        #print "public_state.upper_bet", self.public_state.upper_bet,"chips", self.public_state.chips

        self.public_state.bets                 = [self.public_state.floor_bet for i in range(self.__params__["num_normal_players"])]
        self.public_state.chips                = [self.public_state.chips[i] - self.public_state.floor_bet for i in range(self.__params__["num_normal_players"])]
        self.public_state.max_bet_sofar        = self.public_state.floor_bet
        self.public_state.is_quit              = [False for i in range(self.__params__["num_normal_players"])]
        self.public_state.num_quit             = 0
        self.public_state.is_needed_to_action  = [True for i in range(self.__params__["num_normal_players"])]
        self.public_state.num_needed_to_action = self.__params__["num_normal_players"]
        self.public_state.is_raise             = [False for i in range(self.__params__["num_normal_players"])]
        self.public_state.num_raise            = 0

        self.public_state.round                = 1
        self.public_state.__turn__                 = FiveCardStudEnv.__choose_player_at_begining_of_round__(self.public_state)
        self.public_state.__is_terminal__          = False
        self.public_state.__scores__               = None

        ## person_state
        for i in range(self.__params__["num_normal_players"]):
            self.person_states[i].__id__ = i
            self.person_states[i].first_hand_card  = self.private_state.all_hand_cards[i]
            self.person_states[i].second_hand_card = self.private_state.all_hand_cards[self.__params__["num_normal_players"]+i]
        self.person_states[self.__params__["num_normal_players"]] .__id__= self.__params__["num_normal_players"]

        turn = self.public_state.turn
        self.person_states[turn].__available_actions__ = FiveCardStudEnv.available_actions(self.public_state, self.person_states[turn])

        self.__gen_state_history_list__()
        infos = self.__gen_infos__()

        return infos, self.public_state, self.person_states, self.private_state


    #@override
    def forward(self, action):
        '''
        The environment steps foward with the action
        
        :param action: 
        :return: 
        '''
        turn = self.public_state.turn
        if not FiveCardStudEnv.is_action_valid(action,self.public_state, self.person_states[turn]):
            self.logger.critical("action=%s is invalid" % (action.key()))
            raise ValueError("action=%s is invalid" % (action.key()))

        pu = self.public_state
        pe = self.person_states
        pr = self.private_state
        pu.__action_history__.append((self.public_state.turn,action))
        pe[pu.turn].__available_actions__ = dict()

        if action.option == FiveCardStudAction.Fold:
            self.action_fold(action)
        elif action.option == FiveCardStudAction.Check:
            self.action_check(action)
        elif action.option == FiveCardStudAction.Call:
            self.action_call(action)
        elif action.option == FiveCardStudAction.Raise:
            self.action_raise(action)
        elif action.option == FiveCardStudAction.Showhand:
            self.action_showhand(action)
        elif action.option == FiveCardStudAction.Bet:
            self.action_bet(action)
        else:
            raise Exception("action.option(%s) not in [Fold, Check_, Call, Raise, Showhand, Bet]" % (action.option))
        ##pu.previous_id     = pu.turn
        #pu.previous_action = action
        pu.__action_history__.append((pu.turn, action))
        pu.previous_round  = pu.round

        # computing_score
        if FiveCardStudEnv.__is_compute_scores__(self.public_state):
            num_normal_players          = pu.num_normal_players
            pu.hand_cards        = []
            pu.first_hand_cards  = pr.all_hand_cards[0:                1 * num_normal_players]
            pu.second_hand_cards = pr.all_hand_cards[1 * num_normal_players:  2 * num_normal_players]
            pu.third_hand_cards  = pr.all_hand_cards[2 * num_normal_players:  3 * num_normal_players]
            pu.fourth_hand_cards = pr.all_hand_cards[3 * num_normal_players:  4 * num_normal_players]
            pu.fifth_hand_cards  = pr.all_hand_cards[4 * num_normal_players:  5 * num_normal_players]
            pu.round             = 4


            pu.__is_terminal__ = True
            pu.__scores__      = self.__compute_scores__(pu)

            for i in range(num_normal_players):
                pu.chips[i] += pu.bets[i] + pu.scores[i]

            for i in range(num_normal_players):
                pe[i].first_hand_card  = pr.all_hand_cards[0 * num_normal_players + i]
                pe[i].second_hand_card = pr.all_hand_cards[1 * num_normal_players + i]
                pe[i].third_hand_card  = pr.all_hand_cards[2 * num_normal_players + i]
                pe[i].fourth_hand_card = pr.all_hand_cards[3 * num_normal_players + i]
                pe[i].fifth_hand_card  = pr.all_hand_cards[4 * num_normal_players + i]

            pu.__turn__                              = 0

        # enter into the next stage
        elif FiveCardStudEnv.is_nextround(self.public_state):
            num_normal_players = self.public_state.num_normal_players
            add_cards   = []
            if pu.round == 1:
                pu.third_hand_cards        = pr.all_hand_cards[2 * num_normal_players:  3 * num_normal_players]
                for i in range(num_normal_players):
                    pe[i].third_hand_card  = pr.all_hand_cards[2 * num_normal_players + i]
            if pu.round == 2:
                pu.fourth_hand_cards       = pr.all_hand_cards[3 * num_normal_players:  4 * num_normal_players]
                for i in range(num_normal_players):
                    pe[i].fourth_hand_card = pr.all_hand_cards[3 * num_normal_players + i]
            if pu.round == 3:
                pu.fifth_hand_cards        = pr.all_hand_cards[4 * num_normal_players:  5 * num_normal_players]
                for i in range(num_normal_players):
                    pe[i].fifth_hand_card  = pr.all_hand_cards[4 * num_normal_players + i]


            pu.round                = pu.round + 1
            pu.__turn__             = FiveCardStudEnv.__choose_player_at_begining_of_round__(pu)

            pu.num_needed_to_action = 0
            for i in range(self.__params__["num_normal_players"]):
                if pu.is_quit[i] == False and pu.bets[i] < pu.upper_bet:
                    pu.is_needed_to_action[i] = True
                    pu.num_needed_to_action  += 1
                pu.is_raise[i]            = False
            pu.num_raise = 0

            pe[pu.turn].__available_actions__        = FiveCardStudEnv.available_actions(pu, pe[pu.turn])

        else:
            pu.__turn__                              = self.__next_player__(pu)
            pe[pu.turn].__available_actions__        = FiveCardStudEnv.available_actions(pu, pe[pu.turn])


        self.__gen_state_history_list__()
        infos  = self.__gen_infos__()


        return infos, self.public_state, self.person_states, self.private_state


    #@override
    @classmethod
    def compete(cls, env, players):
        '''
        
        :param env: the fivecardstud game environment 
        :param players: the list of players. The n-1 player is AI bot and the last player is the chance player
        :return: scores
        '''
        num_normal_players = len(players) - 1

        total_scores   = [0 for i in range(num_normal_players)]
        total_count    = 1000
        for count in range(total_count):
            chips       = [(100 +int(random.random()*500)) for i in range(num_normal_players)]

            floor_bet   = 10
            infos, public, persons, private = env.init({"num_normal_players":num_normal_players,"chips":chips, "floor_bet":10})
            for i in range(len(players)):
                players[i].receive_info(infos[i])

            while public.is_terminal == False:
                turn = public.turn
                action = players[turn].take_action()
                infos, public, persons, private = env.forward(action)
                for i in range(len(players)):
                    players[i].receive_info(infos[i])

            for i in range(num_normal_players):
                players[i].reset()
                total_scores[i] += public.scores[i]


            if (count + 1)%500 == 0:
                tmp_scores = [0 for i in range(len(total_scores))]
                for i in range(len(total_scores)):
                    tmp_scores[i] = total_scores[i] / (count+1)
                roomai.get_logger().info("FiveCardStud completes %d competitions, scores=%s"%(count+1, ",".join([str(i) for i in tmp_scores])))

        for i in range(num_normal_players):
            total_scores[i]   /= total_count * 1.0

        return total_scores;


    def action_fold(self, action):
        pu = self.public_state
        pu.is_quit[pu.turn] = True
        pu.num_quit        += 1

        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1

    def action_check(self, action):
        pu = self.public_state
        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1

    def action_call(self, action):
        pu = self.public_state
        pu.chips[pu.turn]               -= action.price
        pu.bets[pu.turn]                += action.price
        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1


    def action_bet(self, action):
        pu = self.public_state

        pu.chips[pu.turn] -= action.price
        pu.bets[pu.turn]  += action.price
        pu.max_bet_sofar   = pu.bets[pu.turn]

        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1
        p = (pu.turn + 1)%pu.num_normal_players
        while p != pu.turn:
            if  pu.is_quit[p] == False and pu.is_needed_to_action[p] == False and pu.bets[p] < pu.upper_bet:
                pu.num_needed_to_action   += 1
                pu.is_needed_to_action[p]  = True
            p = (p + 1) % pu.num_normal_players

    def action_raise(self, action):
        pu = self.public_state

        pu.chips[pu.turn] -= action.price
        pu.bets[pu.turn]  += action.price
        pu.max_bet_sofar   = pu.bets[pu.turn]

        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1
        pu.is_raise[pu.turn]            = True
        pu.num_raise                   +=1
        p = (pu.turn + 1)%pu.num_normal_players
        while p != pu.turn:
            if pu.is_quit[p] == False and pu.is_needed_to_action[p] == False and pu.bets[p] < pu.upper_bet:
                pu.num_needed_to_action   += 1
                pu.is_needed_to_action[p]  = True
            p = (p + 1) % pu.num_normal_players


    def action_showhand(self, action):

        pu = self.public_state

        pu.bets[pu.turn]               += action.price
        pu.chips[pu.turn]               = 0

        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1
        if pu.bets[pu.turn] > pu.max_bet_sofar:
            p = (pu.turn + 1) % pu.num_normal_players
            while p != pu.turn:
                if pu.is_quit[p] == False and pu.is_needed_to_action[p] == False and pu.bets[p] < pu.upper_bet:
                    pu.num_needed_to_action  += 1
                    pu.is_needed_to_action[p] = True
                p = (p + 1) % pu.num_normal_players

            pu.is_raise[pu.turn] = True
            pu.max_bet_sofar     = pu.bets[pu.turn]
            pu.num_raise         = False

############################################# Utils Function ######################################################
    @classmethod
    def __valid_initialization_params__(cls, env):
        if len(env.__params__["chips"]) != env.__params__["num_normal_players"] :
            raise ValueError("len(env.chips)%d != env.num_normal_players%d"%(len(env.__params__["chips"]), env.__params__["num_normal_players"]))

        if env.__params__["num_normal_players"] * 5 > 52:
            raise ValueError("env.num_normal_players * 5 must be less than 51, now env.num_normal_players = %d"%(env.__params__["num_normal_players"]))

        return True

    @classmethod
    def __is_compute_scores__(cls, public_state):
        '''
        
        :param public_state: 
        :return: 
        '''

        pu = public_state

        if pu.num_quit == pu.num_normal_players - 1:
            return True

        if pu.round == 4 and pu.num_needed_to_action == 0:
            return True
        if pu.num_needed_to_action == 0 and pu.max_bet_sofar == pu.upper_bet:
            return True

        return False

    @classmethod
    def __compute_scores__(cls, public_state):
        '''
        
        :param public_state: 
        :return: 
        '''
        if public_state.num_quit + 1 == public_state.num_normal_players:
            player_id = 0
            for i in range(public_state.num_normal_players):
                if public_state.is_quit[i] == False:
                    player_id = i
                    scores = [0 for k in range(public_state.num_normal_players)]
                    for p in range(public_state.num_normal_players):
                        if p == player_id:
                            scores[p] = sum(public_state.bets) - public_state.bets[p]
                        else:
                            scores[p] = -public_state.bets[p]
                    for p in range(public_state.num_normal_players):
                        scores[p] /= public_state.floor_bet * 1.0
                    return scores

            raise ValueError("__compute_scores__ error, is_quit = ", public_state.is_quit, "num_quit=", public_state.num_quit)


        max_cards = [public_state.first_hand_cards[0],\
                     public_state.second_hand_cards[0], public_state.third_hand_cards[0],\
                     public_state.fourth_hand_cards[0], public_state.fifth_hand_cards[0]]
        max_id    = 0
        for i in range(1, public_state.num_normal_players):
            tmp = [public_state.first_hand_cards[i],\
                   public_state.second_hand_cards[i], public_state.third_hand_cards[i],\
                   public_state.fourth_hand_cards[i], public_state.fifth_hand_cards[i]]
            if FiveCardStudEnv.compare_cards(max_cards, tmp) < 0:
                max_cards = tmp
                max_id    = i
     
        scores = [0 for i in range(public_state.num_normal_players)]
        for i in range(public_state.num_normal_players):
            if i == max_id:
                scores[i] = sum(public_state.bets) - public_state.bets[i]
            else:
                scores[i] = -public_state.bets[i]
        for i in range(public_state.num_normal_players):
            scores[i]    /= public_state.floor_bet * 1.0

        return scores

    @classmethod
    def __choose_player_at_begining_of_round__(cls, public_state):
        '''
        
        :param public_state: 
        :return: 
        '''

        round = public_state.round
        if round in [1,2,3]:
            public_cards = None
            if   round == 1: public_cards = public_state.second_hand_cards
            elif round == 2: public_cards = public_state.third_hand_cards
            elif round == 3: public_cards = public_state.fourth_hand_cards

            max_id = 0
            for i in range(public_state.num_normal_players):
                if public_state.is_quit[i] == False:
                    max_id = i
                    break
            max_card = public_cards[max_id]

            for i in range(1, public_state.num_normal_players):
                if FiveCardStudPokerCard.compare(max_card, public_cards[i]) < 0 and public_state.is_quit[i] == False:
                    max_card = public_cards[i]
                    max_id   = i
            return max_id

        elif round == 4:
            max_cards = [public_state.second_hand_cards[0], public_state.third_hand_cards[0],\
                         public_state.fourth_hand_cards[0], public_state.fifth_hand_cards[0]]
            max_id    = 0
            for i in range(1, public_state.num_normal_players):
                tmp = [public_state.second_hand_cards[i], public_state.third_hand_cards[i], \
                       public_state.fourth_hand_cards[i], public_state.fifth_hand_cards[i]]
                if FiveCardStudEnv.compare_cards(max_cards, tmp) < 0:
                    max_cards = tmp
                    max_id    = i
            return max_id

        else:
            raise ValueError("pulic_state.round(%d) not in [1,2,3,4]"%(public_state.turn))

    @classmethod
    def __next_player__(self, pu):
        i = pu.turn
        if pu.num_needed_to_action == 0:
            return -1

        p = (i+1)%pu.num_normal_players
        while pu.is_needed_to_action[p] == False:
            p = (p+1)%pu.num_normal_players
        return p

    @classmethod
    def is_action_valid(cls, action, public_state, person_state):
        '''
        
        :param action: 
        :param public_state: 
        :param person_state: 
        :return: 
        '''

        if action.key not in person_state.available_actions:
            return False
        return True

    @classmethod
    def available_actions(cls, public_state, person_state):
        '''
        
        :param public_state: the public state of the game 
        :param person_state: the person state corresponding to the current player
        :return: 
        '''
        pu              = public_state
        round           = pu.round
        turn            = pu.turn
        Showhand_count  = pu.upper_bet - pu.bets[turn]
        Call_count      = pu.max_bet_sofar - pu.bets[turn]

        actions = dict()
        if round  == 1 or round == 2 or round == 3:
            if pu.previous_round is None or pu.previous_round == round -1:
                ## bet
                for i in range(int(Call_count+1), int(pu.upper_bet-pu.bets[turn])):
                    actions["Bet_%d"%i]                 = FiveCardStudAction.lookup("Bet_%d"%i)
                ## fold
                actions["Fold_0"]                       = FiveCardStudAction.lookup("Fold_0")
                ## showhand
                if Showhand_count > 0:
                    actions["Showhand_%d"%(Showhand_count)] = FiveCardStudAction.lookup("Showhand_%d"%Showhand_count)
                ## Check_
                actions["Check_0"]                      = FiveCardStudAction.lookup("Check_0")
            else:
                ## fold
                actions["Fold_0"]                       = FiveCardStudAction.lookup("Fold_0")
                ## showhand
                if Showhand_count > 0:
                    actions["Showhand_%d"%Showhand_count]   = FiveCardStudAction.lookup("Showhand_%d"%(Showhand_count))
                ## Call
                if Call_count  < Showhand_count:
                    if Call_count == 0:
                        actions["Check_0"]                 = FiveCardStudAction.lookup("Check_0")
                    else:
                        actions["Call_%d"%(Call_count )]   = FiveCardStudAction.lookup("Call_%d"%(Call_count))
                ## "raise"
                if pu.is_raise[turn] == False:
                    for i in range(int(Call_count + 1),int(Showhand_count)):
                        actions["Raise_%d"%(i)] = FiveCardStudAction.lookup("Raise_%d"%i)


        elif round == 4:
            if pu.previous_round == round - 1:
                ## showhand
                if Showhand_count > 0:
                    actions["Showhand_%d"%(Showhand_count)] = FiveCardStudAction.lookup("Showhand_%d"%(Showhand_count))
                ## bet
                for i in range( Call_count + 1, int(pu.upper_bet) - int(pu.bets[turn])):
                    actions["Bet_%d"%i] = FiveCardStudAction.lookup("Bet_%d"%i)
                ## fold
                actions["Fold_0"]     = FiveCardStudAction.lookup("Fold_0")

            else:
                ## fold
                actions["Fold_0"]     = FiveCardStudAction("Fold_0")
                ## Call
                if Call_count  == Showhand_count and Showhand_count > 0:
                    actions["Showhand_%d"%(Call_count)]       = FiveCardStudAction.lookup("Showhand_%d"%(Call_count))
                elif Call_count == 0:
                    actions["Check_0"]                        = FiveCardStudAction.lookup("Check_0")
                else:
                    actions["Call_%d"%(Call_count )]          = FiveCardStudAction.lookup("Call_%d"%(Call_count))

        else:
            raise ValueError("pulic_state.round(%d) not in [1,2,3,4]" % (public_state.turn))

        return actions

    @classmethod
    def is_nextround(self, public_state):
        '''
        
        :return: A boolean variable indicates whether is it time to enter the next stage
        '''
        return public_state.num_needed_to_action == 0

    @classmethod
    def compare_cards(cls, cards1, cards2):
        """

        Args:
            cards1:
            cards2:

        Returns:

        """
        if len(cards1) == len(cards2) and len(cards1) == 4:
            pattern1 = cls.fourcards2pattern(cards1)
            pattern2 = cls.fourcards2pattern(cards2)
            if pattern1[5] != pattern2[5]:
                return pattern1[5] - pattern2[5]
            else:
                cards1.sort(key = cmp_to_key(FiveCardStudPokerCard.compare))
                cards2.sort(key = cmp_to_key(FiveCardStudPokerCard.compare))
                return FiveCardStudPokerCard.compare(cards1[-1], cards2[-1])

        elif len(cards1) == len(cards2) and len(cards1) == 5:
            pattern1 = cls.cards2pattern(cards1)
            pattern2 = cls.cards2pattern(cards2)
            if pattern1[5] != pattern2[5]:
                return pattern1[5] - pattern2[5]
            else:
                cards1.sort(key = cmp_to_key(FiveCardStudPokerCard.compare))
                cards2.sort(key = cmp_to_key(FiveCardStudPokerCard.compare))
                return FiveCardStudPokerCard.compare(cards1[-1], cards2[-1])

        else:
            raise  ValueError("len(cards1)%d, and len(cards2)%d are same and are 4 or 5 "%(len(cards1),len(cards2)))

    @classmethod
    def cards2pattern(cls, cards):

        """

        Args:
            cards:

        Returns:

        """

        pointrank2cards = dict()
        for c in cards:
            if c.point_rank in pointrank2cards:
                pointrank2cards[c.point_rank].append(c)
            else:
                pointrank2cards[c.point_rank] = [c]
        for p in pointrank2cards:
            pointrank2cards[p].sort(key = cmp_to_key(FiveCardStudPokerCard.compare))

        suitrank2cards = dict()
        for c in cards:
            if c.suit_rank in suitrank2cards:
                suitrank2cards[c.suit_rank].append(c)
            else:
                suitrank2cards[c.suit_rank] = [c]
        for s in suitrank2cards:
            suitrank2cards[s].sort(key = cmp_to_key(FiveCardStudPokerCard.compare))

        num2pointrank = [[], [], [], [], []]
        for p in pointrank2cards:
            num = len(pointrank2cards[p])
            num2pointrank[num].append(p)
        for i in range(5):
            num2pointrank[num].sort()

        sorted_pointrank = []
        for p in pointrank2cards:
            sorted_pointrank.append(p)
        sorted_pointrank.sort()

        ##straight_samesuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                numStraight = 1
                for i in range(len(suitrank2cards[s]) - 2, -1, -1):
                    if suitrank2cards[s][i].point_rank == suitrank2cards[s][i + 1].point_rank - 1:
                        numStraight += 1
                    else:
                        numStraight = 1

                    if numStraight == 5:
                        pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["Straight_SameSuit"]
                        return pattern

        ##4_1
        if len(num2pointrank[4]) ==1:
            pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["4_1"]
            return pattern

        ##3_2
        if len(num2pointrank[3]) == 1 and len(num2pointrank[2]) == 1:
            pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["3_2"]
            return pattern

        ##SameSuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["SameSuit"]
                return pattern

        ##Straight_DiffSuit
        numStraight = 1
        for idx in range(len(sorted_pointrank) - 2, -1, -1):
            if sorted_pointrank[idx] + 1 == sorted_pointrank[idx]:
                numStraight += 1
            else:
                numStraight = 1

            if numStraight == 5:
                pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["Straight_DiffSuit"]
                for p in range(idx, idx + 5):
                    point = sorted_pointrank[p]
                return pattern

        ##3_1_1
        if len(num2pointrank[3]) == 1:
            pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["3_1_1"]
            return pattern

        ##2_2_1
        if len(num2pointrank[2]) >= 2:
            pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["2_2_1"]
            return pattern

        ##2_1_1_1
        if len(num2pointrank[2]) == 1:
            pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["2_1_1_1"]
            return pattern

        ##1_1_1_1_1
        return  roomai.fivecardstud.FiveCardStudAllCardsPattern["1_1_1_1_1"]

    @classmethod
    def fourcards2pattern(cls, cards):
        """

        Args:
            cards:

        Returns:

        """
        pointrank2cards = dict()
        for c in cards:
            if c.point_rank in pointrank2cards:
                pointrank2cards[c.point_rank].append(c)
            else:
                pointrank2cards[c.point_rank] = [c]
        for p in pointrank2cards:
            pointrank2cards[p].sort(key = cmp_to_key(FiveCardStudPokerCard.compare))

        suitrank2cards = dict()
        for c in cards:
            if c.suit_rank in suitrank2cards:
                suitrank2cards[c.suit_rank].append(c)
            else:
                suitrank2cards[c.suit_rank] = [c]
        for s in suitrank2cards:
            suitrank2cards[s].sort(key = cmp_to_key(FiveCardStudPokerCard.compare))

        num2pointrank = [[], [], [], [], []]
        for p in pointrank2cards:
            num = len(pointrank2cards[p])
            num2pointrank[num].append(p)
        for i in range(5):
            num2pointrank[num].sort()

        sorted_pointrank = []
        for p in pointrank2cards:
            sorted_pointrank.append(p)
        sorted_pointrank.sort()

        ##candidate straight_samesuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 4:
                numStraight = 1
                for i in range(len(suitrank2cards[s]) - 2, -1, -1):
                    if suitrank2cards[s][i].point_rank == suitrank2cards[s][i + 1].point_rank  - 1:
                        numStraight += 1
                    else:
                        numStraight = 1

                    if numStraight == 4:
                        pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["Straight_SameSuit"]
                        return pattern

        ##4_1
        if len(num2pointrank[4]) == 1:
            pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["4_1"]
            return pattern

        ##3_2 impossible
        if len(num2pointrank[3]) == 1 and len(num2pointrank[2]) == 1:
            pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["3_2"]
            return pattern

        ##SameSuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 4:
                pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["SameSuit"]
                return pattern

        ##Straight_DiffSuit
        numStraight = 1
        for idx in range(len(sorted_pointrank) - 2, -1, -1):
            if sorted_pointrank[idx] + 1 == sorted_pointrank[idx]:
                numStraight += 1
            else:
                numStraight = 1

            if numStraight == 4:
                pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["Straight_DiffSuit"]
                return pattern

        ##3_1_1
        if len(num2pointrank[3]) == 1:
            pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["3_1_1"]
            return pattern

        ##2_2_1
        if len(num2pointrank[2]) >= 2:
            pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["2_2_1"]
            return pattern

        ##2_1_1_1
        if len(num2pointrank[2]) == 1:
            pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["2_1_1_1"]
            return pattern

        ##1_1_1_1_1
        return roomai.fivecardstud.FiveCardStudAllCardsPattern["1_1_1_1_1"]

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = FiveCardStudEnv()
        newinstance = super(FiveCardStudEnv, self).__deepcopy__(newinstance=newinstance)
        return newinstance