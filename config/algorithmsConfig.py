# This module contains the class that stores the algorithm specific information
# depending on the user's choice

import os

# Custom algorithm imports
from agents.a2c.a2c import A2C
from agents.a3c import A3C
from agents.dqn.deepQNetwork import DeepQNetwork
from agents.ddqn.doubleDeepQNetwork import DoubleDeepQNetwork
from agents.reinforce.reinforce import REINFORCE


# List of algorithms supported
# Supporting a new algorithm only needs an entry added into this.
ALGO_LIST = [
    DeepQNetwork,
]

# Create the mappings between names of the algorithms and their classes
ALGO_MAP = {algo.get_name(): algo for algo in ALGO_LIST}

# Keys related to the packing of the algorithm configuration data
KEY_ALGO            = 'algorithm'
KEY_OPTIM           = 'optimizer'
KEY_ENVIRONMENT     = 'environment'
KEY_NUM_AGENTS      = 'num_agents'
KEY_LEARN_RATE      = 'learning_rate'
KEY_NUM_LAYERS      = 'num_layers'
KEY_NUM_EPISODES    = 'num_episodes'
KEY_NUM_WARMUP      = 'num_warmup_episodes'
KEY_SELF_PLAY_EP    = 'self_play_ep_per_update'
KEY_SELF_PLAY_DELTA = 'self_play_delta'
KEY_UPDATE_INT      = 'checkpoint_interval'
KEY_UNITS_LIST      = 'units_list'
KEY_ACTIV_LIST      = 'activations_list'
KEY_WORKSPACE       = 'workspace'


# Default configuration values
ALGO_DEF_LEARN_RATE     = 0.01
ALGO_DEF_NUM_LAYERS     = 2
ALGO_DEF_NUM_AGENTS     = 2
ALGO_DEF_NUM_EPISODES   = 10
ALGO_DEF_NUM_WARMUP     = 0
ALGO_DEF_UPDATE_INT     = 2
ALGO_DEF_SPLAY_EPISODES = 10
ALGO_DEF_SPLAY_DELTA    = 0.01
ALGO_DEF_NUM_UNITS      = 32
ALGO_DEF_ACTIVATION     = 'ReLU'


def get_agent(agent_name):
    """ Returns class reference to the agent """
    return ALGO_MAP[agent_name]


class AlgoConfig:
    """ Algorithm Configuration class """

    def __init__(self, *args, **kwargs):
        """ """
        self.environ   = None
        self.algorithm = None
        self.optimizer = None
        self.learnRate = None
        self.numLayers = None
        self.numEpisodes = None
        self.numWarmup = None
        self.uInterval = None
        self.splayUpdate = None
        self.splayDelta = None
        self.layerList = None
        self.workspace = None
        self.numAgents = None

    # *****************************************
    # Setter methods for the instance variables
    # *****************************************

    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm

    def setEnvironment(self, env):
        self.environ = env

    def setNumAgents(self, n):
        self.numAgents = n

    def setOptimizer(self, optimizer):
        self.optimizer = optimizer

    def setLearningRate(self, learnRate):
        self.learnRate = learnRate

    def setNumLayers(self, numLayers):
        self.numLayers = numLayers

    def setNumEpisodes(self, numEpochs):
        self.numEpisodes = numEpochs

    def setNumWarmupEpisodes(self, numWarmup):
        self.numWarmup = numWarmup

    def setSelfPlayUpdateEpisodes(self, episodes):
        self.splayUpdate = episodes

    def setSelfPlayDelta(self, delta):
        self.splayDelta = delta

    def setUpdateInterval(self, uInterval):
        self.uInterval = uInterval

    def setLayerList(self, units, activations):
        if units is None and activations is None:
            self.layerList = None
        else:
            self.layerList = [(u,a) for u,a in zip(units, activations)]


    def setWorkspace(self, workspace):
        self.workspace = workspace


    # *****************************************
    # Getter methods for the instance variables
    # *****************************************

    def getAlgorithm(self):
        return self.algorithm

    def getEnvironment(self):
        return self.environ

    def getNumAgents(self):
        return self.numAgents

    def getOptimizer(self):
        return self.optimizer

    def getLearningRate(self):
        return self.learnRate

    def getNumLayers(self):
        return self.numLayers

    def getNumEpisodes(self):
        return self.numEpisodes

    def getNumWarmupEpisodes(self):
        return self.numWarmup

    def getSelfPlayUpdateEpisodes(self):
        return self.splayUpdate

    def getSelfPlayDelta(self):
        return self.splayDelta

    def getUpdateInterval(self):
        return self.uInterval

    def getLayerList(self):
        unitsList = None
        actvsList = None

        if self.layerList is not None:
            unitsList = [t[0] for t in self.layerList]
            actvsList = [t[1] for t in self.layerList]

        return (unitsList, actvsList)


    def getWorkspace(self):
        return self.workspace


    def getConfigData(self):
        """ Packing method that packs all the data obtained so far as a dictionary and returns it """
        unitsList, actvsList = self.getLayerList()
        config_data = {
            KEY_ALGO:            self.getAlgorithm(),
            KEY_ENVIRONMENT:     self.getEnvironment(),
            KEY_NUM_AGENTS:      self.getNumAgents(),
            KEY_OPTIM:           self.getOptimizer(),
            KEY_LEARN_RATE:      self.getLearningRate(),
            KEY_NUM_LAYERS:      self.getNumLayers(),
            KEY_NUM_EPISODES:    self.getNumEpisodes(),
            KEY_NUM_WARMUP:      self.getNumWarmupEpisodes(),
            KEY_SELF_PLAY_EP:    self.getSelfPlayUpdateEpisodes(),
            KEY_SELF_PLAY_DELTA: self.getSelfPlayDelta(),
            KEY_UPDATE_INT:      self.getUpdateInterval(),
            KEY_WORKSPACE:       self.getWorkspace(),
            KEY_UNITS_LIST:      unitsList,
            KEY_ACTIV_LIST:      actvsList
        }
        return config_data


    def checkAndUpdateConfigData(self, configData):
        """ Checks the values of the given configuration data and fills with defaults wherever applicable """

        if configData[KEY_NUM_AGENTS] is None:
            configData[KEY_NUM_AGENTS] = ALGO_DEF_NUM_AGENTS

        if configData[KEY_NUM_LAYERS] is None:
            configData[KEY_NUM_LAYERS] = ALGO_DEF_NUM_LAYERS

        if configData[KEY_NUM_EPISODES] is None:
            configData[KEY_NUM_EPISODES] = ALGO_DEF_NUM_EPISODES

        if configData[KEY_NUM_WARMUP] is None:
            configData[KEY_NUM_WARMUP] = ALGO_DEF_NUM_WARMUP

        if configData[KEY_LEARN_RATE] is None:
            configData[KEY_LEARN_RATE] = ALGO_DEF_LEARN_RATE

        if configData[KEY_UPDATE_INT] is None:
            configData[KEY_UPDATE_INT] = ALGO_DEF_UPDATE_INT

        if configData[KEY_SELF_PLAY_EP] is None:
            configData[KEY_SELF_PLAY_EP] = ALGO_DEF_SPLAY_EPISODES

        if configData[KEY_SELF_PLAY_DELTA] is None:
            configData[KEY_SELF_PLAY_DELTA] = ALGO_DEF_SPLAY_DELTA

        if configData[KEY_WORKSPACE] is None:
            configData[KEY_WORKSPACE] = os.path.abspath(os.curdir)

        numLayers = configData[KEY_NUM_LAYERS]
        if configData[KEY_UNITS_LIST] is None:
            configData[KEY_UNITS_LIST] = [ALGO_DEF_NUM_UNITS] * numLayers
            configData[KEY_ACTIV_LIST] = [ALGO_DEF_ACTIVATION] * numLayers

        return configData