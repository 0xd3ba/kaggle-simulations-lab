import os
# import torch
import time

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
        episodes = self.config_data[acfg.KEY_NUM_EPISODES]

        for e in range(episodes):

            if self.need_to_stop():
                break

            print(f'epoch[{e}]')
            self.update_progress_bar(e+1)
            time.sleep(1)


    def update_progress_bar(self, e):
        """ Updates the progress bar by a step """
        total_episodes = self.config_data[acfg.KEY_NUM_EPISODES]
        perc_done = int((e*100 / total_episodes))

        # Let the worker thread do the job
        self.worker_thread.update_progress_bar(perc_done)


    def update_text_box(self):
        """ Updates the textbox by filling it with new stats """
        pass
