# This module contains the class for "Hungry-Geese" Kaggle competition
#

from environments.environmentWrapper import EnvironmentWrapper

class GoogleResearchFootball(EnvironmentWrapper):
    """ Class for Hungry Geese environment """

    def __init__(self):
        self.environmentName = GRESEARCH_FOOTBALL_TITLE
        self.environmentSubtitle = GRESEARCH_FOOTBALL_SUBTITLE
        self.competitionLink = GRESEARCH_FOOTBALL_LINK
        self.description = self.buildDescription(GRESEARCH_FOOTBALL_INFO)