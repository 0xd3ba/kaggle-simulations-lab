# This module contains methods for building neural network models

import torch
import torch.nn as nn
import torch.optim as optim


# Mapping of the list of optimizers supported
OPTIM_MAP = {
    'AdaDelta':             optim.Adadelta,
    'Adagrad':              optim.Adagrad,
    'Adam':                 optim.Adam,
    'AdamW':                optim.AdamW,
    'SparseAdam':           optim.SparseAdam,
    'AdaMax':               optim.Adamax,
    'ASGD (Averaged SGD)':  optim.ASGD,
    'RMSProp':              optim.RMSprop,
    'RProp':                optim.Rprop,
    'SGD':                  optim.SGD
}

# Mapping of the list of activations supported
ACTIV_MAP = {
    'CELU':       nn.CELU,
    'ELU':        nn.ELU,
    'GELU':       nn.GELU,
    'HardTanh':   nn.Hardtanh,
    'LeakyReLU':  nn.LeakyReLU,
    'LogSigmoid': nn.LogSigmoid,
    'PReLU':      nn.PReLU,
    'RReLU':      nn.RReLU,
    'ReLU':       nn.ReLU,
    'ReLU6':      nn.ReLU6,
    'SELU':       nn.SELU,
    'Sigmoid':    nn.Sigmoid,
    'Tanh':       nn.Tanh
}


class FeedForwardNet(nn.Module):
    """ Builds a simple feed forward net with the supplied parameters """

    def __init__(self, ip_dim, op_dim, units_list, activ_list):
        super().__init__()
        self.layers = []

        curr_dim = ip_dim
        for next_dim, activation in zip(units_list, activ_list):
            layer_i = nn.Linear(curr_dim, next_dim)
            activ_i = ACTIV_MAP[activation]()

            self.layers.append(layer_i)
            self.layers.append(activ_i)

            curr_dim = next_dim

        # Finally need to add the output layer (raw scores)
        # And and then build the model
        layer_i = nn.Linear(curr_dim, op_dim)
        self.layers.append(layer_i)
        self.model = nn.Sequential(*self.layers)

    def forward(self, x):
        # Assumption is made that x is a torch tensor
        return self.model(x)



def buildOptimizer(network, optim_key, lr):
    """ Builds an optimizer for the given neural network with the given parameters """
    optimizer = OPTIM_MAP[optim_key](network.parameters(), lr=lr)
    return optimizer