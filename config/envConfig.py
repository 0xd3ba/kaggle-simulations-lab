# This module contains the class that stores the environment specific information

from environments.hungryGeese import HungryGeese
from environments.rockPaperScissor import RockPaperScissor
from environments.haliteTwoSigma import HaliteTwoSigma
from environments.connectX import ConnectX
from environments.santaCandyCane import SantaCandyCane
from environments.googleResearchFootball import GoogleResearchFootball


ENV_HUNGRY_GEESE       = 'Hungry Geese'
ENV_ROCK_PAPER_SCISSOR = 'Rock, Paper, Scissors'
ENV_HALITE_TWO_SIGMA   = 'Halite by Two Sigma (Playground Edition)'
ENV_CONNECT_X          = 'Connect X'
ENV_SANTA_CANDY_CANE   = 'Santa 2020 - The Candy Cane Contest'
ENV_GRESEARCH_FOOTBALL = 'Google Research Football with Manchester City F.C.'

# Reference list of all the environments
ENV_LIST = [
    HungryGeese,
    RockPaperScissor,
    HaliteTwoSigma,
    ConnectX,
    SantaCandyCane,
    GoogleResearchFootball
]

# List of supported environments till now
ENV_SUPPORTED_LIST = [
    HungryGeese
]

ENV_MAP = {env().getEnvironmentName():env for env in ENV_LIST}
ENV_SUPPORTED = {env().getEnvironmentName() for env in ENV_SUPPORTED_LIST}
