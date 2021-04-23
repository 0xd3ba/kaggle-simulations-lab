# This module contains the class for "Hungry-Geese" Kaggle competition

import numpy as np
import kaggle_environments as kaggle_env
from kaggle_environments.envs.hungry_geese import hungry_geese

# Custom module for supporting self-play
from environments.selfplay import SelfPlay


class HungryGeese(SelfPlay):
    """ Class for Hungry Geese environment """

    HUNGRY_GEESE_ENV_NAME = 'hungry_geese'

    # Markers to indicate geese and food status on the grid
    OUR_GEESE_HEAD_MARKER = 3
    OUR_GEESE_BODY_MARKER = 2
    OUR_GEESE_TAIL_MARKER = 1
    OPPONENT_GEESE_HEAD_MARKER = -3
    OPPONENT_GEESE_BODY_MARKER = -2
    OPPONENT_GEESE_TAIL_MARKER = -1
    FOOD_MARKER = 4

    def __init__(self, n_agents, n_warmup):
        super().__init__(n_agents, n_warmup)

        self.env = kaggle_env.make(self.HUNGRY_GEESE_ENV_NAME)
        self.minFood = self.env.configuration['min_food']   # Minimum number of food on the board
        self.nRows = self.env.configuration['rows']         # Number of rows on the board
        self.nCols = self.env.configuration['columns']      # Number of columns on the board
        self.we_won = False                                 # Did we win the game

        # The warmup bot -- Intially the model is trained against these bots
        # The idea is, we want our agent to get a good start
        self.warmupBots = [hungry_geese.GreedyAgent(self.env.configuration) if i != self.getOurAgentIndex()
                           else None for i in range(n_agents)]

        # There are 4 actions: NORTH, EAST, SOUTH, WEST
        # And they all are strings. Stepping through the environment needs the actions to be
        # strings. So there is a need to build a mapping between integers and the string
        self.actions = {i: a.name for i, a in enumerate(hungry_geese.Action)}

        # The current state of the board. Contains one vector for each agent
        self.board = np.zeros(shape=(n_agents, self.nRows*self.nCols), dtype=np.float32)

        # Update the number of actions and observation vector lengths
        self.updateNumActions(len(self.actions))
        self.updateNumObservations(self.nRows * self.nCols)

    def reset(self):
        """ Responsible for resetting the environment """
        obs = self.env.reset(self.getNumAgents())
        self.updateCurrentObservation(obs)                  # Update the most recent observation
        self._update_board()                                # Update the state of the board with current observation

        # Return the status of the board of each of the agents
        return self.board[self.getOurAgentIndex()]

    def step(self, action):
        """ Responsible for stepping through the environment
            actions is an integer that corresponds to action index
            of our agent. We need to tweak this to get the name of the actions
        """
        our_index = self.getOurAgentIndex()

        if self.isWarmupComplete():
            actions_list = self.getActionsList(action, self.board)
            actions_list = [self.actions[a] if a is not None else None for a in actions_list]
        else:
            # Note that the actions provided by the bots are already decoded strings
            # We don't need to decode them !
            actions_list = self._getWarmupBotsActions()

        # Finally add our own action to the list
        actions_list[our_index] = self.actions[action]

        obs = self.env.step(actions_list)
        self.updateCurrentObservation(obs)
        self._update_board()

        game_over = self.env.done
        we_lost = self.isAgentDone(our_index) and not game_over

        done = we_lost or game_over
        info = self.getInfo(our_index)
        reward = self.getReward(our_index)
        reward = self._tweak_reward(reward)

        if done:
            self.we_won = not we_lost
            self.updateWarmupCounter()

        return self.board[our_index], reward, done, self.we_won, info


    # *****************************************
    # Helper methods for the environment
    # *****************************************

    def _update_board(self):
        """ Updates the state of the board with the observations of all the agents """
        agents = self._get_agent_positions()                # A 2D list containing position of the geese
        food = self._get_food_positions()                   # A 1D list containing position of the food

        for i, pos in enumerate(agents):
            self.board[i, :] = 0                            # First reset the status of the board entirely
            dead = (pos == [])                              # When the goose dies, the position is an empty list

            if not dead:                                    # If the goose is not dead, update the positions
                self.board[i, pos[0]] = self.OUR_GEESE_HEAD_MARKER
                if len(pos) > 1:
                    self.board[i, pos[1:-1]] = self.OUR_GEESE_BODY_MARKER
                    self.board[i, pos[-1]] = self.OUR_GEESE_TAIL_MARKER

            self.board[i, food] = self.FOOD_MARKER          # Now mark the position of food on the grid

            # Now marks the opponents in this goose's grid in a similar way
            for j, opp_pos in enumerate(agents):
                if i == j:
                    continue

                opp_dead = (opp_pos == [])
                if opp_dead:
                    continue

                # Opponent is alive and kicking. Need to update its position on the grid
                self.board[i, opp_pos[0]] = self.OPPONENT_GEESE_HEAD_MARKER
                if len(opp_pos) > 1:
                    self.board[i, opp_pos[1:-1]] = self.OPPONENT_GEESE_BODY_MARKER
                    self.board[i, opp_pos[-1]] = self.OPPONENT_GEESE_TAIL_MARKER

        # All done -- Return


    def _get_agent_positions(self):
        """ Returns a list of positions of all the agents on the board """
        obs = self.getObservation()
        return obs['geese']

    def _get_food_positions(self):
        """ Returns a list of positions of the food present in the board """
        obs = self.getObservation()
        return obs['food']

    def _tweak_reward(self, reward):
        """ Tweaks the reward accordingly -- Depending on the tweak, the agent will perform better/worse """
        reward = int(np.log10(reward + 1))  # Convert to log-scale because the rewards get extremely large
        return reward

    def _getWarmupBotsActions(self):
        """ Get the actions from the warmup bots """
        obs = self.getObservation()
        obs = hungry_geese.Observation(obs)

        actions = [bot(obs) if bot is not None else None for bot in self.warmupBots]

        # NOTE: The actions are already decoded, i.e. they are string names !
        return actions

