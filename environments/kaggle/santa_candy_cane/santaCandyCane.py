# This module contains the class for "Santa Candy Cane" Kaggle competition

# Custom module for supporting self-play
from environments.selfplay import SelfPlay


class SantaCandyCane(SelfPlay):
    """ Class for Santa Candy Cane environment """

    def __init__(self, n_agents, n_warmup, delta):
        super().__init__(n_agents, n_warmup, delta)
        # TODO: Write the code for supporting this environment later
