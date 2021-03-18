# This module contains the class for "Hungry-Geese" Kaggle competition
#

from environments.baseEnvironment import BaseEnvironment

CONNECT_X_TITLE    = "Connect X"
CONNECT_X_SUBTITLE = "Connect your checkers in a row before your opponent!"
CONNECT_X_LINK     = "https://www.kaggle.com/c/connectx"
CONNECT_X_INFO     = [
    """
    In this game, your objective is to get a certain number of your checkers in a row horizontally, vertically, or 
    diagonally on the game board before your opponent. When it's your turn, you “drop” one of your checkers into 
    one of the columns at the top of the board. Then, let your opponent take their turn. This means each move may be 
    trying to either win for you, or trying to stop your opponent from winning. The default number is four-in-a-row, 
    but we’ll have other options to come soon.
    """
]


class ConnectX(BaseEnvironment):
    """ Class for Hungry Geese environment """

    def __init__(self):
        self.environmentName = CONNECT_X_TITLE
        self.environmentSubtitle = CONNECT_X_SUBTITLE
        self.competitionLink = CONNECT_X_LINK
        self.description = self.buildDescription(CONNECT_X_INFO)