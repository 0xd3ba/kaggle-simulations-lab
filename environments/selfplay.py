# This module contains the base environment class for Self-Play

import copy
import numpy as np
import torch
import torch.nn.functional as F


class SelfPlay:
    """ Base environment for self-play """

    def __init__(self, n_agents=2):
        """
        n_agents: Number of agents in the game (including our agent)
        """
        self.our_index = 0                                  # Index of our agent
        self.n_agents = n_agents                            # Total number of agents in the game
        self.clones = [None for _ in range(self.n_agents)]  # Cloned models of our agent
        self.curr_obs = None                                # Current observation
        self.n_obs = None                                   # Number of components in the observation vector
        self.n_actions = None                               # Number of valid actions

    def updateAgents(self, agent):
        """ Responsible for updating the agents by cloning the provided model """
        self.clones = [copy.deepcopy(agent) if i != self.getOurAgentIndex() else None
                       for i in range(self.n_agents)
                       ]

    # *****************************************
    # Methods that the kaggle environment
    # needs to override
    def reset(self):
        """ Resets the environment and returns the starting state """
        raise NotImplementedError

    def step(self, action):
        """ Takes an action (so does the opponents) and returns
            (next_state, reward, done, info)
        """
        raise NotImplementedError
    # *****************************************

    def getActionsList(self, action, obs):
        """ Takes an action (so does the opponents) and returns
            (next_state, reward, done, info)
            NOTE: The caller will need to decode the actions as Kaggle has this weird style
                  of naming actions as strings.
        """
        our_index = self.getOurAgentIndex()
        actions_list = [None for _ in range(self.getNumAgents())]
        actions_list[our_index] = action

        # Now we need to get the actions from all the other agents
        for j in range(self.getNumAgents()):
            if j == our_index or self.isAgentDone(j):       # Either it's us or the opponent is dead
                continue

            # The opponent is alive and kicking !
            opp_action = self._clone_predict(j, obs[j])
            actions_list[j] = opp_action

        # Now return the encoded action list
        return actions_list

    def _clone_predict(self, agentID, agentObs):
        """ Predicts the next action of the clone (i.e. our opponent) based on its observation """
        clone_agent = self.clones[agentID]

        # Now predict the action. Note that agentObs is a vector of shape (n_observations, )
        # clone_agent is an instance of a child of "Agent" class
        action = clone_agent.predict_action(agentObs)
        return action

    def updateCurrentObservation(self, obs):
        """ Responsible for updating the current observation of the environment """
        self.curr_obs = obs

    def updateNumActions(self, n):
        """ Updates the number of actions. Called only during initialization of the environment """
        self.n_actions = n

    def updateNumObservations(self, n):
        self.n_obs = n

    def isAgentDone(self, agentID):
        """ Checks if the agent with the specified ID is done """
        status = self.curr_obs[agentID]['status']
        done = False
        if status == 'DONE' or status == 'INACTIVE' or status == 'INVALID':
            done = True

        return done

    def getObservationLength(self):
        """ Returns the length of the observation vector """
        return self.n_obs

    def getNumActions(self):
        """ Returns the length of the number of actions """
        return self.n_actions

    def getNumAgents(self):
        """ Returns the total number of agents """
        return self.n_agents

    def getOurAgentIndex(self):
        """ Returns the index of our agent """
        return self.our_index

    def getInfo(self, agentID):
        """ Returns the debugging info of the agent with specified ID """
        return self.curr_obs[agentID]['info']

    def getReward(self, agentID):
        """ Returns the reward of the agent with specified ID """
        return self.curr_obs[agentID]['reward']

    def getAgentStatus(self, agentID):
        """ Returns the status (one of the below mentioned) of the agent
                - ACTIVE:     The agent can take an action in this time-step
                - INACTIVE:   The agent can't take an action in this time-step
                - INVALID:    The agent took an invalid action, hence Dead
                - DONE:       The agent either won/lost
        """
        return self.curr_obs[agentID]['status']

    def getObservation(self):
        """ Returns the current state of the game (includes state of all the agents) """
        return self.curr_obs[0]['observation']