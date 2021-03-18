# This module contains the class for "Hungry-Geese" Kaggle competition
#

from environments.baseEnvironment import BaseEnvironment

SANTA_CANDY_TITLE    = "Santa 2020 - The Candy Cane Contest"
SANTA_CANDY_SUBTITLE = "May your workdays be merry and bright"
SANTA_CANDY_LINK     = "https://www.kaggle.com/c/santa-2020"
SANTA_CANDY_INFO     = [
    """
    Morale has been low at the North Pole this year. But Santa really believes in “making spirits bright!” 
    So he has planned a friendly competition among the elves to keep the Christmas cheer alive and make as 
    many toys as possible! And the winning team gets a snow cone party!
    """,

    """
    As one of the team leaders, you know that nothing keeps your fellow elves more productive and motivated 
    than a steady supply of candy canes! But all seven levels of the Candy Cane Forest are closed for revegetation, 
    so the only ones available are stuck in the break room vending machines. And even though you receive free snacks 
    on the job, the vending machines are always broken and don’t always give you what you want.
    """,

    """
    Due to social distancing, only two elves can be in the break room at once. You and another team leader will take 
    turns trying to get candy canes out of the 100 possible vending machines in the room, but each machine is 
    unpredictable in how likely it is to work. You do know, however, that the more often you try to use a machine, the 
    less likely it will give you a candy cane. Plus, you only have time to try 2000 times on the vending machines until 
    you need to get back to the workshop!
    """,

    """
    If you can collect more candy canes than the other team leaders, you’ll surely be able to help your team win Santa's
     contest! Try your hand at this multi-armed candy cane challenge!
    """
]


class SantaCandyCane(BaseEnvironment):
    """ Class for Hungry Geese environment """

    def __init__(self):
        self.environmentName = SANTA_CANDY_TITLE
        self.environmentSubtitle = SANTA_CANDY_SUBTITLE
        self.competitionLink = SANTA_CANDY_LINK
        self.description = self.buildDescription(SANTA_CANDY_INFO)