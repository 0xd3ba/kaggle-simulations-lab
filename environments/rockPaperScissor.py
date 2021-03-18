# This module contains the class for "Hungry-Geese" Kaggle competition
#

from environments.baseEnvironment import BaseEnvironment

ROCK_PAPER_TITLE    = "Rock, Paper, Scissors"
ROCK_PAPER_SUBTITLE = "Shoot!"
ROCK_PAPER_LINK     = "https://www.kaggle.com/c/rock-paper-scissors"
ROCK_PAPER_INFO     = [
    """
    Rock, Paper, Scissors (sometimes called roshambo) has been a staple to settle playground disagreements or 
    determine who gets to ride in the front seat on a road trip. The game is simple, with a balance of power. 
    There are three options to choose from, each winning or losing to the other two. In a series of truly random games, 
    each player would win, lose, and draw roughly one-third of games. But people are not truly random, which provides a 
    fun opportunity for AI.
    """,

    """
    Studies have shown that a Rock, Paper, Scissors AI can consistently beat human opponents. With previous 
    games as input, it studies patterns to understand a player’s tendencies. But what happens when we expand the simple 
    “Best-of-3” game to be “Best-of-1000”? How well can artificial intelligence perform?
    """,

    """
    In this simulation competition, you will create an AI to play against others in many rounds of this classic game. 
    Can you find patterns to make yours win more often than it loses? It’s possible to greatly outperform a random 
    player when the matches involve non-random agents. A strong AI can consistently beat predictable AI.
    """,

    """
    This problem is fundamental to the fields of machine learning, artificial intelligence, and data compression. 
    There are even potential applications in human psychology and hierarchical temporal memory. Warm up your hands and 
    get ready to Rock, Paper, Scissors in this challenge.
    """
]


class RockPaperScissor(BaseEnvironment):
    """ Class for Hungry Geese environment """

    def __init__(self):
        self.environmentName = ROCK_PAPER_TITLE
        self.environmentSubtitle = ROCK_PAPER_SUBTITLE
        self.competitionLink = ROCK_PAPER_LINK
        self.description = self.buildDescription(ROCK_PAPER_INFO)