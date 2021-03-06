# This module implements the Advantage Actor-Critic algorithm

import numpy as np
import torch
import torch.nn.functional as F

# Custom module imports for agent
from agents.agent import Agent


class A2C(Agent):
    """ Class for Advantage Actor-Critic algorithm """

    def __init__(self, env, network, optimizer, model_dir, log_dir):
        super().__init__(env, network, optimizer, model_dir, log_dir)
        # TODO: Write code to support this algorithm later on