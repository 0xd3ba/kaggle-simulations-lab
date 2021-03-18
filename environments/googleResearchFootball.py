# This module contains the class for "Hungry-Geese" Kaggle competition
#

from environments.baseEnvironment import BaseEnvironment

GRESEARCH_FOOTBALL_TITLE    = "Google Research Football with Manchester City F.C."
GRESEARCH_FOOTBALL_SUBTITLE = "Train agents to master the world's most popular sport"
GRESEARCH_FOOTBALL_LINK     = "https://www.kaggle.com/c/google-football/"
GRESEARCH_FOOTBALL_INFO     = [
    """
    The world gets a kick out of football (soccer in the United States). As the most popular sport on the planet, 
    millions of fans enjoy watching Sergio Agüero, Raheem Sterling, and Kevin de Bruyne on the field. Football video 
    games are less lively, but still immensely popular, and we wonder if AI agents would be able to play those properly.
    """,

    """
    Researchers want to explore AI agents' ability to play in complex settings like football. The sport requires a 
    balance of short-term control, learned concepts such as passing, and high-level strategy, which can be difficult 
    to teach agents. A current environment exists to train and test agents, but other solutions may offer better 
    results.
    """,

    """
    The teams at Google Research aspire to make discoveries that impact everyone. Essential to their approach is 
    sharing research and tools to fuel progress in the field. Together with Manchester City F.C., Google Research has 
    put forth this competition to get help in reaching their goal.
    """,

    """
    In this competition, you’ll create AI agents that can play football. Teams compete in “steps,” where agents 
    react to a game state. Each agent in an 11 vs 11 game controls a single active player and takes actions to 
    improve their team’s situation. As with a typical football game, you want your team to score more than the 
    other side. You can optionally see your efforts rendered in a physics-based 3D football simulation.
    """,

    """
    If controlling 11 football players with code sounds difficult, don't be discouraged! You only need to control 
    one player at a time (the one with the ball on offense, or the one closest to the ball on defense) and your 
    code gets to pick from 1 of 19 possible actions. We have prepared a getting started example to show you how 
    simple a basic strategy can be. Before implementing your own strategy, however, you might want to learn more 
    about the Google Research football environment, especially observations provided to you by the environment and 
    available actions. You can also play the game yourself on your computer locally to get better understanding of 
    the environment's dynamics and explore different scenarios.
    """,

    """
    If successful, you'll help researchers explore the ability of AI agents to play in complex settings. 
    This could offer new insights into the strategies of the world's most-watched sport. Additionally, this research 
    could pave the way for a new generation of AI agents that can be trained to learn complex skills.
    """
]


class GoogleResearchFootball(BaseEnvironment):
    """ Class for Hungry Geese environment """

    def __init__(self):
        self.environmentName = GRESEARCH_FOOTBALL_TITLE
        self.environmentSubtitle = GRESEARCH_FOOTBALL_SUBTITLE
        self.competitionLink = GRESEARCH_FOOTBALL_LINK
        self.description = self.buildDescription(GRESEARCH_FOOTBALL_INFO)