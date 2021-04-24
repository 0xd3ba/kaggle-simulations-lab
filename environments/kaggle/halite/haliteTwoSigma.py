# This module contains the class for "Halite Two Sigma" Kaggle competition

# Custom module for supporting self-play
from environments.selfplay import SelfPlay


class HaliteTwoSigma(SelfPlay):
    """ Class for Halite Two Sigma environment """

    def __init__(self, n_agents, n_warmup, delta):
        super().__init__(n_agents, n_warmup, delta)
        # TODO: Write the code for supporting this environment later
