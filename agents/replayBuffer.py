# This module contains the class for Replay-Buffer

import random
from collections import deque


class ReplayBuffer:
    CURR_STATE_KEY = 'current_state'
    ACTION_KEY = 'action'
    REWARD_KEY = 'reward'
    NEXT_STATE_KEY = 'next_state'
    DONE_KEY = 'done'

    def __init__(self, buffer_size):
        self.buffer = deque(maxlen=buffer_size)

    def store(self, curr_state, action, reward, next_state, done):
        """ Store the obtained experience onto the buffer """
        data = self._prepare_data(curr_state, action, reward, next_state, done)
        self.buffer.append(data)

    def sample(self, batch_size):
        """ Samples a batch of data from the buffer and returns it """
        batch = random.sample(self.buffer, k=batch_size)
        curr_states = []
        actions = []
        rewards = []
        next_states = []
        done = []

        for data in batch:
            curr_states.append(data[self.CURR_STATE_KEY])
            actions.append(data[self.ACTION_KEY])
            rewards.append(data[self.REWARD_KEY])
            next_states.append(data[self.NEXT_STATE_KEY])
            done.append(data[self.DONE_KEY])

        return curr_states, actions, rewards, next_states, done

    def _prepare_data(self, curr_state, action, reward, next_state, done):
        """ Packs the data into a nice dictionary and returns it """
        data = {
            self.CURR_STATE_KEY: curr_state,
            self.ACTION_KEY: action,
            self.REWARD_KEY: reward,
            self.NEXT_STATE_KEY: next_state,
            self.DONE_KEY: done
        }

        return data

    def __len__(self):
        """ Returns the length of the current buffer """
        return len(self.buffer)
