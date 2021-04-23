import time
import torch

import config.algorithmsConfig as acfg


class Trainer:
    """ Trainer class responsible for training the agent and logging """
    def __init__(self, worker_thread, config_data, agent):
        self.config_data = config_data
        self.worker_thread = worker_thread
        self.agent = agent


    def need_to_stop(self):
        """ Returns a boolean indicating whether or not to stop the training """
        return not self.worker_thread.is_active()


    def start(self):
        """ Trains until stop signal is received or all episodes have been looped """
        env = self.agent.get_environment()
        log_dir = self.agent.get_log_directory()
        chkpt_dir = self.agent.get_model_directory()

        episodes = self.config_data[acfg.KEY_NUM_EPISODES]
        warmup_episodes = self.config_data[acfg.KEY_NUM_WARMUP]
        selfplay_update_interval = self.config_data[acfg.KEY_SELF_PLAY_EP]
        chkpt_interval = self.config_data[acfg.KEY_CHKPT_INT]
        showdown_interval = self.config_data[acfg.KEY_EVAL_INTERVAL]
        showdown_episodes = self.config_data[acfg.KEY_EVAL_EPISODES]

        # Create the initial clones of itself before we begin training
        env.updateAgents(self.agent)

        for e in range(1, episodes + warmup_episodes + 1):

            # Before playing one episode, check if we need to stop, if yes, then break
            # This check is needed in case "Cancel" button is pressed in the GUI which must
            # stop the training process !
            if self.need_to_stop():
                break

            # Play one episode, then train the network
            # Cumulative reward and whether or not we won, are returned after episode termination
            total_reward, total_steps, won = self.agent.play_one_episode()
            self.agent.train()

            # If it is time to save the agent to disk, save it to disk
            if e % chkpt_interval == 0 and chkpt_dir is not None:
                print(f'saving to {chkpt_dir}')
                self.agent.save(e)

            # If it is showdown time, start the showdown
            if e % showdown_interval == 0:
                win_rate, avg_reward, avg_steps = self.showdown(showdown_episodes)
                print(f'win_rate: {win_rate}\navg. reward: {avg_reward}\navg_steps: {avg_steps}\n')
                # TODO: Log them into tensorboard

            # If we have crossed the warmup episodes and we have reached the episode
            # when we can increase the difficulty by updating the clones
            if (e > warmup_episodes) and (e % selfplay_update_interval) == 0:
                env.updateAgents(self.agent)

            # TODO: Write tensorboard logs'
            # TODO: Periodically save the agent to the directory

            self.update_progress_bar(e)


    def showdown(self, n_episodes):
        """ Perform a showdown of n_episodes against the opponents """
        n_wins = 0
        avg_reward = 0
        avg_steps = 0

        for _ in range(n_episodes):
            total_reward, total_steps, won = self.agent.play_one_episode(eval=True)

            # Now update the statistics
            if won:
                n_wins += 1
            avg_reward += total_reward
            avg_steps += total_steps

        # TODO: There is a bug due to which in 1v1 matches, we are winning 100%, which is wrong
        #       Reason is in `isAgentDone()` method. Check it later 
        win_rate = (n_wins / n_episodes) * 100
        avg_reward = avg_reward / n_episodes
        avg_steps = avg_steps / n_episodes

        return win_rate, avg_reward, avg_steps


    def update_progress_bar(self, e):
        """ Updates the progress bar by a step """
        total_episodes = self.config_data[acfg.KEY_NUM_EPISODES] + self.config_data[acfg.KEY_NUM_WARMUP]
        perc_done = int((e*100 / total_episodes))

        # Let the worker thread do the job
        self.worker_thread.update_progress_bar(perc_done)


    def update_text_box(self):
        """ Updates the textbox by filling it with new stats """
        pass
