# This module contains the base class for a RL-Agent

import os
import time
import pickle


class Agent:
    """ The base class for all agents """

    def __init__(self, env, network, optimizer, model_dir, log_dir):
        self.environment = env  # An instance of the environment
        self.network = network  # The neural-network for the agent
        self.optimizer = optimizer  # The optimizer for the network
        self.model_dir = model_dir  # The place to dump the saved models
        self.log_dir = log_dir  # The place to dump the training logs

    def get_model_directory(self):
        """ Returns the directory to store the models """
        return self.model_dir

    def get_log_directory(self):
        """ Returns the directory to store the logs """
        return self.log_dir

    def get_environment(self):
        """ Returns the environment """
        return self.environment

    def get_network(self):
        """ Returns the neural network stored """
        return self.network

    def get_optimizer(self):
        """ Returns the optimizer stored """
        return self.optimizer

    def save(self, i):
        """ Responsible for dumping the model's weights to the model directory """
        state_dict = self.network.state_dict()

        # <model_name>_<episode #>_<time>.pkl
        model_name = f'{self.get_acronym()}_{i}_{time.asctime()}.pkl'
        model_path = os.path.join(self.get_model_directory(), model_name)
        model_file = open(model_path, 'wb')

        # Finally save the configuration of the network to disk
        pickle.dump(state_dict, model_file)

        model_file.close()

    # ****************************************************
    # The following methods need to be overridden by
    # the inherited classes
    # ****************************************************

    @staticmethod
    def get_acronym():
        """ Returns the acronym of the agent (used for naming the saved models) """
        raise NotImplementedError

    @staticmethod
    def get_name():
        """ Returns the name of the agent, i.e. algorithm (used for displaying on GUI) """
        raise NotImplementedError

    def predict_action(self, state, eval=False):
        """ Returns an action by predicting it from the state """
        raise NotImplementedError

    def play_one_episode(self, eval=False):
        """ Plays one episode until the end of the episode """
        raise NotImplementedError

    def train(self):
        """ Responsible for training the network based on the experience obtained """
        raise NotImplementedError
