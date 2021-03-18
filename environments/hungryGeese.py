# This module contains the class for "Hungry-Geese" Kaggle competition
#

from environments.baseEnvironment import BaseEnvironment

HUNGRY_GEESE_TITLE    = "Hungry Geese"
HUNGRY_GEESE_SUBTITLE = "Dont. Stop. Eating."
HUNGRY_GEESE_LINK     = "https://www.kaggle.com/c/hungry-geese"
HUNGRY_GEESE_INFO     = [
    """
    Whether it be in an arcade, on a phone, as an app, on a computer, or maybe stumbled upon in a web search, many 
    of us have likely developed fond memories playing a version of Snake. It’s addicting to control a slithering 
    serpent and watch it grow along the grid until you make one… wrong… move. Then you have to try again because 
    surely you won’t make the same mistake twice!
    """,

    """
    With Hungry Geese, Kaggle has taken this classic in the video game industry and put a multi-player, simulation 
    spin to it. You will create an AI agent to play against others and survive the longest. You must make sure your 
    goose doesn’t starve or run into other geese; it’s a good thing that geese love peppers, donuts, and pizza—which 
    show up across the board.
    """,

    """
    Extensive research exists in building Snake models using reinforcement learning, Q-learning, neural networks, 
    and more (maybe you’ll use… Python?). Take your grid-based reinforcement learning knowledge to the next level 
    with this exciting new challenge!
    """
]


class HungryGeese(BaseEnvironment):
    """ Class for Hungry Geese environment """

    def __init__(self):
        self.environmentName = HUNGRY_GEESE_TITLE
        self.environmentSubtitle = HUNGRY_GEESE_SUBTITLE
        self.competitionLink = HUNGRY_GEESE_LINK
        self.description = self.buildDescription(HUNGRY_GEESE_INFO)