# This module implements the Cross-Entropy Method algorithm

import numpy as np
import torch
import torch.nn.functional as F

# Custom module imports for agent
from agents.agent import Agent


class CrossEntropyMethod(Agent):
    """ Class for Cross-Entropy Method algorithm """

    def __init__(self, env, network, optimizer, model_dir, log_dir):
        super().__init__(env, network, optimizer, model_dir, log_dir)
        self.actions = []           # The action taken in the environment
        self.rewards = []           # The reward got for taking the action
        self.observations = []      # The states of the environment


    @staticmethod
    def get_acronym():
        """ Return the name (acronym) of this agent, i.e. reinforce """
        return 'ce-method'

    @staticmethod
    def get_name():
        """ Return the name of this agent, i.e. REINFORCE """
        return 'Cross-Entropy Method'

    def predict_action(self, state, eval=False):
        """ Predicts an action given the observations """
        env = self.get_environment()
        state = torch.tensor(state, dtype=torch.float)      # Shape (observation_len, )

        scores = self.network(state)                        # Shape (n_actions, )
        action_probs = F.softmax(scores, dim=-1)            # Shape (n_actions, )

        # Create a categorical distribution from the probabilities and sample an action from it
        dist = torch.distributions.Categorical(action_probs)
        action = dist.sample().item()

        return action

    def play_one_episode(self, eval=False):
        """ Responsible for playing one episode """
        env = self.get_environment()
        curr_state = env.reset()
        done = False      # Is the game finished yet ?
        won = False       # Did we total_wins ?
        total_steps = 0   # Number of steps before game was finished
        total_reward = 0  # Total reward (cumulative) we got in the episode

        while not done:
            action = self.predict_action(curr_state, eval)

            # Now take an action and get the appropriate rewards and next state
            next_state, reward, done, won, _ = env.step(action)
            total_reward += reward

            # Save the current state, action and the reward obtained.
            if not eval:
                self.observations.append(curr_state)
                self.actions.append(action)
                self.rewards.append(reward)

            curr_state = next_state
            total_steps += 1

        return total_reward, total_steps, won

    def train(self):
        """ Trains the agent using the policy gradient approach """

        optimizer = self.get_optimizer()

        actions = torch.tensor(self.actions, dtype=torch.long)
        observations = torch.tensor(self.observations, dtype=torch.float32)

        # Do a forward pass again, but on the batch of observations
        scores = self.network(observations)
        loss = F.cross_entropy(scores, actions)
        loss = -loss            # Need to do a gradient ascent

        # Back-propagate the loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        self._memory_reset()    # No use for the memory -- Clear them now

    def _get_discounted_rewards(self):
        """ Calculates the discounted rewards and returns them """
        # Because we are dealing with Episodic tasks, the discounting factor is 1
        rewards = self.rewards
        discounted_rewards = torch.zeros(len(rewards))

        r = 0
        for i in reversed(range(discounted_rewards.shape[0])):
            r += rewards[i]
            discounted_rewards[i] = r

        return discounted_rewards

    def _memory_reset(self):
        """ Clears the memory, i.e. rewards and log probabilities """
        self.actions = []
        self.rewards = []
        self.observations = []