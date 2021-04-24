# This module implements the REINFORCE policy gradient algorithm

import numpy as np
import torch
import torch.nn.functional as F

# Custom module imports for agent
from agents.agent import Agent


class REINFORCE(Agent):
    """ Class for REINFORCE algorithm """

    def __init__(self, env, network, optimizer, model_dir, log_dir):
        super().__init__(env, network, optimizer, model_dir, log_dir)
        self.observations = []
        self.actions = []
        self.rewards = []

    @staticmethod
    def get_acronym():
        """ Return the name (acronym) of this agent, i.e. reinforce """
        return 'reinforce'

    @staticmethod
    def get_name():
        """ Return the name of this agent, i.e. REINFORCE """
        return 'REINFORCE'

    def predict_action(self, state, eval=False):
        """ Predicts an action given the observations """
        env = self.get_environment()

        state = torch.tensor(state, dtype=torch.float)      # Shape (observation_len, )

        # Important: Do not detach from the computation graph. They will be required to back-propagate
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
        won = False       # Did we win ?
        total_steps = 0   # Number of steps before game was finished
        total_reward = 0  # Total reward (cumulative) we got in the episode

        while not done:
            action = self.predict_action(curr_state, eval)

            # Now take an action and get the appropriate rewards and next state
            next_state, reward, done, won, _ = env.step(action)
            total_reward += reward

            # Save the reward obtained. Log probabilities of the action was aleady saved
            # in the call to predict action
            if not eval:
                self.actions.append(action)
                self.rewards.append(reward)
                self.observations.append(curr_state)

            curr_state = next_state
            total_steps += 1

        return total_reward, total_steps, won

    def train(self):
        """ Trains the agent using the policy gradient approach """

        optimizer = self.get_optimizer()

        # Calculate the discounted rewards and then the loss
        disc_rewards = self._get_discounted_rewards()

        # Need to calculate the log probabilities from the stored observations
        actions_tensor = torch.tensor(self.actions, dtype=torch.long)               # Shape (batch, )
        states_tensor = torch.tensor(self.observations, dtype=torch.float32)        # Shape (batch, observation_len)
        scores_tensor = self.network(states_tensor)                                 # Shape (batch, n_actions)
        probs_tensor = F.softmax(scores_tensor, dim=-1)                             # Shape (batch, n_actions)

        # Now select the probabilities of the actions that we used in the episode
        # Then calculate the log probabilities
        actions_probs = torch.gather(probs_tensor, dim=1, index=actions_tensor.unsqueeze(1)).squeeze(1)

        log_probs = torch.log(actions_probs)
        loss = (disc_rewards * log_probs).sum()
        loss = -loss            # We need to do a gradient ascent step

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
        self.observations = []
        self.actions = []
        self.rewards = []
