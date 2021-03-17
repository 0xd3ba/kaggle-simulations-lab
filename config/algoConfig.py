# This module contains the class that stores the algorithm specific information
# depending on the user's choice

from agents.a2c                import A2C
from agents.a3c                import A3C
from agents.deepQNetwork       import DeepQNetwork
from agents.doubleDeepQNetwork import DoubleDeepQNetwork
from agents.reinforce          import REINFORCE

# List of algorithms supported
# Supporting a new algorithm only needs an entry added into this.
ALGO_LIST = [
    A2C,
    A3C,
    DeepQNetwork,
    DoubleDeepQNetwork,
    REINFORCE
]

# Create the mappings between names of the algorithms and their classes
ALGO_MAP = {algo.ALGO_NAME: algo for algo in ALGO_LIST}

# List of optimizers supported
OPTIM_LIST = [
    'AdaDelta',
    'Adagrad',
    'Adam',
    'AdamW',
    'SparseAdam',
    'AdaMax',
    'ASGD (Averaged SGD)',
    'RMSProp',
    'RProp',
    'SGD'
]

# List of activations supported
ACTIV_LIST = [
    'CELU',
    'ELU',
    'GELU',
    'GLU',
    'HardTanh',
    'LeakyReLU',
    'LogSigmoid',
    'PReLU',
    'RReLU',
    'ReLU',
    'ReLU6',
    'SELU',
    'Sigmoid',
    'Softmax',
    'Tanh',
    'Threshold'
]

# Keys related to the packing of the algorithm configuration data
KEY_ALGO        = 'algorithm'
KEY_OPTIM       = 'optimizer'
KEY_ENVIRONMENT = 'environment'
KEY_LEARN_RATE  = 'learning_rate'
KEY_NUM_LAYERS  = 'num_layers'
KEY_NUM_EPOCHS  = 'num_epochs'
KEY_UPDATE_INT  = 'update_interval'
KEY_UNITS_LIST  = 'units_list'
KEY_ACTIV_LIST  = 'activations_list'


class AlgoConfig:
    """ Algorithm Configuration class """

    def __init__(self, *args, **kwargs):
        """ """
        self.environ   = None
        self.algorithm = None
        self.optimizer = None
        self.learnRate = None
        self.numLayers = None
        self.numEpochs = None
        self.uInterval = None
        self.layerList = None

    # *****************************************
    # Setter methods for the instance variables
    # *****************************************

    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm

    def setEnvironment(self, env):
        self.environ = env

    def setOptimizer(self, optimizer):
        self.optimizer = optimizer

    def setLearningRate(self, learnRate):
        self.learnRate = learnRate

    def setNumLayers(self, numLayers):
        self.numLayers = numLayers

    def setNumEpochs(self, numEpochs):
        self.numEpochs = numEpochs

    def setUpdateInterval(self, uInterval):
        self.uInterval = uInterval

    def setLayerList(self, units, activations):
        if units is None and activations is None:
            self.layerList = None
        else:
            self.layerList = [(u,a) for u,a in zip(units, activations)]


    # *****************************************
    # Getter methods for the instance variables
    # *****************************************

    def getAlgorithm(self):
        return self.algorithm

    def getEnvironment(self):
        return self.environ

    def getOptimizer(self):
        return self.optimizer

    def getLearningRate(self):
        return self.learnRate

    def getNumLayers(self):
        return self.numLayers

    def getNumEpochs(self):
        return self.numEpochs

    def getUpdateInterval(self):
        return self.uInterval

    def getLayerList(self):
        unitsList = None
        actvsList = None

        if self.layerList is not None:
            unitsList = [t[0] for t in self.layerList]
            actvsList = [t[1] for t in self.layerList]

        return (unitsList, actvsList)


    def getConfigData(self):
        """ Packing method that packs all the data obtained so far as a dictionary and returns it """
        unitsList, actvsList = self.getLayerList()
        config_data = {
            KEY_ALGO:        self.getAlgorithm(),
            KEY_ENVIRONMENT: self.getEnvironment(),
            KEY_OPTIM:       self.getOptimizer(),
            KEY_LEARN_RATE:  self.getLearningRate(),
            KEY_NUM_LAYERS:  self.getNumLayers(),
            KEY_NUM_EPOCHS:  self.getNumEpochs(),
            KEY_UPDATE_INT:  self.getUpdateInterval(),
            KEY_UNITS_LIST:  unitsList,
            KEY_ACTIV_LIST:  actvsList
        }
        return config_data