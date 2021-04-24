# This module implements the Deep-Q Network algorithm

import copy
import numpy as np
import torch
import torch.nn.functional as F

# Custom module imports for agent
from agents.agent import Agent
from agents.replayBuffer import ReplayBuffer


class DeepQNetwork(Agent):
    """ Class for Deep-Q Network algorithm """

    REPLAY_BUFF_SIZE = 50_000
    REPLAY_BATCH_SIZE = 256
    EPSILON_DECAY = 0.99
    STEPS_PER_TARGET_UPDATE = 200

    def __init__(self, env, network, optimizer, model_dir, log_dir):
        super().__init__(env, network, optimizer, model_dir, log_dir)

        self.buffer = ReplayBuffer(buffer_size=self.REPLAY_BUFF_SIZE)  # Create the replay buffer
        self.target_net = copy.deepcopy(network)  # Create the target network
        self.epsilon = 1  # The exploration rate -- Initially full exploration
        self._steps_trained = 0  # Counter used to track and update target net every 'x' steps

        self.epsilon_decay = self.EPSILON_DECAY  # TODO: Provide this as a parameter
        self._steps_threshold = self.STEPS_PER_TARGET_UPDATE  # TODO: Provide this as a parameter

        self.target_net.eval()

    @staticmethod
    def get_acronym():
        """ Return the name (acronym) of this agent, i.e. DQN """
        return 'dqn'

    @staticmethod
    def get_name():
        """ Return the name of this agent, i.e. Deep Q-Network """
        return 'Deep Q-Network'

    def predict_action(self, state, eval=False):
        """ Returns an action -- Predicts it from the state """
        env = self.get_environment()
        state = torch.tensor(state, dtype=torch.float)
        q_vals = self.network(state).detach()

        # Sample a random action if we are still exploring, then decay the exploration rate
        if np.random.uniform() < self.epsilon and eval:
            self.epsilon *= self.epsilon_decay
            action = np.random.choice(env.getNumActions())
        else:
            action = torch.argmax(q_vals, dim=-1).item()

        return action

    def play_one_episode(self, eval=False):
        """ Responsible for playing one episode and storing the experience obtained into the memory """
        env = self.get_environment()
        curr_state = env.reset()
        done = False        # Is the game finished yet ?
        won = False         # Did we total_wins ?
        total_steps = 0     # Number of steps before game was finished
        total_reward = 0    # Total reward (cumulative) we got in the episode

        while not done:
            action = self.predict_action(curr_state, eval)

            # Now take an action and get the appropriate rewards and next state
            next_state, reward, done, won, _ = env.step(action)
            total_reward += reward

            # Save the experience obtained into the buffer
            if not eval:
                self.buffer.store(curr_state, action, reward, next_state, done)

            curr_state = next_state
            total_steps += 1

        return total_reward, total_steps, won

    def train(self):
        """ Responsible for training the network """

        # If our buffer is not yet ready to be sampled from, wait until it is
        # before starting the training process
        if len(self.buffer) < self.REPLAY_BATCH_SIZE:
            return

        # Yep, the buffer is ready to be sampled from
        # Sample a batch from the buffer
        current_states, actions, rewards, next_states, done = self.buffer.sample(self.REPLAY_BATCH_SIZE)
        optimizer = self.get_optimizer()

        # TODO: Use GPU if available -- Set it in the parent class

        curr_states_t = torch.tensor(current_states, dtype=torch.float)  # Shape (batch, n_obs)
        next_states_t = torch.tensor(next_states, dtype=torch.float)  # Shape (batch, n_obs)
        actions_t = torch.tensor(actions, dtype=torch.long)  # Shape (batch, )
        done_t = torch.tensor(done, dtype=torch.bool)  # Shape (batch, )
        rewards_t = torch.tensor(rewards, dtype=torch.float)  # Shape (batch, )

        curr_q_vals = self.network(curr_states_t)  # Shape (batch, n_actions)
        target_q_vals = self.target_net(next_states_t).detach()  # Shape (batch, n_actions)

        # Extract the Q-values of the actions that we took on the current state
        curr_q_vals = torch.gather(curr_q_vals, dim=1, index=actions_t.unsqueeze(1)).squeeze(1)
        target_q_vals = target_q_vals.max(dim=1)[0]  # Off-policy selection

        target_q_vals[done_t] = 0.0  # The long-term reward starting from terminal state is 0
        updated_q_val = rewards_t + target_q_vals  # No need for discounting, because it is a finite episode

        # Finally calculate the loss and perform a back-propagation
        loss = F.mse_loss(curr_q_vals, updated_q_val)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        self._steps_trained += 1
        if self._steps_trained > self._steps_threshold:
            self._steps_threshold = 0
            self.target_net.load_state_dict(self.network.state_dict())
