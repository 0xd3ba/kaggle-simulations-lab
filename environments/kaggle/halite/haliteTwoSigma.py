# This module contains the class for "Hungry-Geese" Kaggle competition
#

from environments.environmentWrapper import EnvironmentWrapper

HALITE_TITLE    = "Halite by Two Sigma - Playground Edition"
HALITE_SUBTITLE = "Collect the most halite during your match in space"
HALITE_LINK     = "https://www.kaggle.com/c/halite-iv-playground-edition"
HALITE_INFO     = [
    """
    Ahoy there! There's halite to be had and ships to be deployed! Are you ready to navigate the skies and secure 
    your territory?
    """,

    """
    Halite by Two Sigma ("Halite") is a resource management game where you build and control a small armada of ships. 
    Your algorithms determine their movements to collect halite, a luminous energy source. The most halite at the end 
    of the match wins, but it's up to you to figure out how to make effective and efficient moves. You control your 
    fleet, build new ships, create shipyards, and mine the regenerating halite on the game board.
    """,

    """
    Created by Two Sigma in 2016, more than 15,000 people around the world have participated in a Halite challenge. 
    Players apply advanced algorithms in a dynamic, open source game setting. The strategic depth and immersive, 
    interactive nature of Halite games make each challenge a unique learning environment.
    """,

    """
    Halite IV builds on the core game design of Halite III with a number of key changes that shift the focus of the 
    game towards tighter competition on a smaller board. New game features include regenerating halite, shipyard 
    creation, no more ship movement costs, and stealing halite from other players!
    """,

    """
    So dust off your halite meters and fasten your seatbelts. The fourth season of Halite is about to begin!
    """
]


class HaliteTwoSigma(EnvironmentWrapper):
    """ Class for Hungry Geese environment """

    def __init__(self):
        self.environmentName = HALITE_TITLE
        self.environmentSubtitle = HALITE_SUBTITLE
        self.competitionLink = HALITE_LINK
        self.description = self.buildDescription(HALITE_INFO)