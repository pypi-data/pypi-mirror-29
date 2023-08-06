# RoomAI

[![Build Status](https://travis-ci.org/roomai/RoomAI.svg?branch=master)](https://travis-ci.org/roomai/RoomAI.svg?branch=master)
[![Documentation Status](https://readthedocs.org/projects/roomai/badge/?version=latest)](http://roomai.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/roomai.svg)](https://pypi.python.org/pypi/roomai)



RoomAI is a toolkit for developing and comparing AI-bots of imperfect information games.



# Installation and The First Try

You can install roomai with pip

<pre>
pip install roomai
</pre>

Try your first RoomAI program


<pre>
#!/bin/python
from roomai.kuhn import *;
import random
import roomai
import roomai.common

class KuhnPokerExamplePlayer(roomai.common.AbstractPlayer):
    def receive_info(self, info):
        if info.person_state.available_actions is not None:
            self.available_actions = info.person_state.available_actions
            
    def take_action(self):
        values = self.available_actions.values()
        return list(values)[int(random.random() * len(values))]
        
    def reset(self):
        pass

if __name__ == "__main__":
        players = [KuhnPokerExamplePlayer() for i in range(2)] + [roomai.common.RandomPlayerChance()]
        #RandomChancePlayer is the chance player with the uniform distribution over every output
        env = KuhnPokerEnv()
        scores = KuhnPokerEnv.compete(env, players)
        print (scores)
</pre>



# For More Information

 - [RoomAI Tutorials](docs/document/tutorials.md)
 
 - [Guides for AI Developers](docs/document/guides_ai.md)
 
 - [Guides for Game Developers](docs/document/guides_game.md)
 
 - [API Docs](http://roomai.readthedocs.io/en/latest/?badge=latest)
 
 - [Model Zoo](docs/document/model_zoo.md)
 
 - [FQA](docs/document/fqa.md)
 


# Contributors

If you would like to contribute to the project, please send me (lili1987mail at gmail.com) an email. We are always happy for more help.
