# This module contains the trainer class for training our agent
from torch.utils.tensorboard import SummaryWriter
import config.algorithmsConfig as acfg


class Trainer:
    """ Trainer class responsible for training the agent and logging """

    EPOCH_KEY = 'epoch'
    TOTAL_TRAIN_REWARD_KEY = 'total_train_rewards'
    TOTAL_TRAIN_STEPS_KEY = 'total_train_steps'
    TOTAL_TRAIN_WINS_KEY = 'total_train_wins'

    WIN_RATE_KEY = 'win_rate'
    AVG_SHOWDOWN_REWARD_KEY = 'avg_showdown_reward'
    AVG_SHOWDOWN_STEPS_KEY = 'avg_showdown_steps'
    SHOWDOWN_KEY = 'showdown'

    def __init__(self, worker_thread, config_data, agent):
        self.config_data = config_data              # Dictionary containing training information
        self.worker_thread = worker_thread          # Thread on which this trainer is running
        self.agent = agent                          # The agent to train
        self.writer = None                          # Tensorboard writer
        self.can_log = False                        # Can we log the results ? Only true when writer is not None
        self.total_train_wins_till_now = 0          # Track the number of games we won till now
        self.total_train_rewards_till_now = 0       # Track the total rewards we got till now
        self.total_train_steps_till_now = 0         # Track the total steps we did till now
        self.total_showdowns_till_now = 0           # Track the total number of showdowns till now
        self.total_showdown_win_rate_till_now = 0   # Track the cumulative win rate till now
        self.total_showdown_steps_till_now = 0      # Track the total number of steps in the showdown till now
        self.total_showdown_rewards_till_now = 0    # Track the total number of showdown rewards till now


    def need_to_stop(self):
        """ Returns a boolean indicating whether or not to stop the training """
        return not self.worker_thread.is_active()


    def start(self):
        """ Trains until stop signal is received or all episodes have been looped """

        self.instantiate_writer()        # Instantiate the summary writer object

        env = self.agent.get_environment()
        chkpt_dir = self.agent.get_model_directory()

        episodes = self.config_data[acfg.KEY_NUM_EPISODES]
        warmup_episodes = self.config_data[acfg.KEY_NUM_WARMUP]
        selfplay_update_interval = self.config_data[acfg.KEY_SELF_PLAY_EP]
        chkpt_interval = self.config_data[acfg.KEY_CHKPT_INT]
        showdown_interval = self.config_data[acfg.KEY_EVAL_INTERVAL]
        showdown_episodes = self.config_data[acfg.KEY_EVAL_EPISODES]

        # Create the initial clones of itself before we begin training
        env.setAgents(self.agent)

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

            # Update the summary statistics (need to display in the GUI)
            if won:
                self.total_train_wins_till_now += 1
            self.total_train_rewards_till_now += total_reward
            self.total_train_steps_till_now += total_steps

            # If it is time to save the agent to disk, save it to disk
            if e % chkpt_interval == 0 and chkpt_dir is not None:
                self.agent.save(e)

            # If it is showdown time, start the showdown
            if e % showdown_interval == 0:
                win_rate, avg_reward, avg_steps = self.showdown(showdown_episodes)

                self.total_showdowns_till_now += 1
                self.total_showdown_win_rate_till_now += win_rate
                self.total_showdown_steps_till_now += avg_steps
                self.total_showdown_rewards_till_now += avg_reward

                # print(f'win_rate: {win_rate}\navg. reward: {avg_reward}\navg_steps: {avg_steps}\n')

                if self.logging_possible():
                    self.writer.add_scalar('Evaluation/win_rate', win_rate, e)
                    self.writer.add_scalar('Evaluation/avg_reward', avg_reward, e)
                    self.writer.add_scalar('Evaluation/avg_steps', avg_steps, e)

                # Now update the contents in the GUI
                self.update_text_box_showdown(e)

            # If we have crossed the warmup episodes and we have reached the episode
            # when we can increase the difficulty by updating the clones
            if (e > warmup_episodes) and (e % selfplay_update_interval) == 0:
                env.updateAgents(self.agent)

            if self.logging_possible():
                self.writer.add_scalar('Training/total_reward', total_reward, e)
                self.writer.add_scalar('Training/total_steps', total_steps, e)
                self.writer.add_scalar('Training/wins', int(won), e)

            # Update the GUI components
            self.update_progress_bar(e)
            self.update_text_box_training(e)

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


    def update_text_box_training(self, epoch):
        """ Updates the textbox by filling it with new stats of training """
        # Let the worker thread do the job
        data = self._prepare_data_training(epoch)
        self.worker_thread.update_textbox_training(data)


    def update_text_box_showdown(self, epoch):
        """ Updates the textbox by filling it with new stats of the showdown """
        data = self._prepare_data_showdown(epoch)
        self.worker_thread.update_textbox_showdown(data)


    def instantiate_writer(self):
        """ Instantiates the summary writer object for tensorboard logging """
        log_dir = self.agent.get_log_directory()
        if log_dir is not None:
            self.can_log = True
            self.writer = SummaryWriter(log_dir=log_dir)


    def logging_possible(self):
        """ Returns a boolean indicating whether we can log or not """
        return self.can_log


    def _prepare_data_training(self, epoch):
        """ Bundles the data that needs to be sent to the parent GUI for update """

        # Average out the data based on the number of epochs passed
        total_reward = round(self.total_train_rewards_till_now / epoch, 3)
        total_steps = round(self.total_train_steps_till_now / epoch, 3)
        total_wins = round(self.total_train_wins_till_now / epoch, 3) * 100

        data = {
            self.EPOCH_KEY: epoch,
            self.TOTAL_TRAIN_REWARD_KEY: total_reward,
            self.TOTAL_TRAIN_STEPS_KEY: total_steps,
            self.TOTAL_TRAIN_WINS_KEY: total_wins
        }

        return data


    def _prepare_data_showdown(self, epoch):
        """ Bundles the data that needs to be sent to the parent GUI for update """

        # Average out the data based on the number of showdowns till now
        showdowns = self.total_showdowns_till_now
        win_rate = round(self.total_showdown_win_rate_till_now / showdowns, 3)
        avg_reward = round(self.total_showdown_rewards_till_now / showdowns, 3)
        avg_steps = round(self.total_showdown_steps_till_now / showdowns, 3)

        data = {
            self.EPOCH_KEY: epoch,
            self.SHOWDOWN_KEY: showdowns,
            self.WIN_RATE_KEY: win_rate,
            self.AVG_SHOWDOWN_REWARD_KEY: avg_reward,
            self.AVG_SHOWDOWN_STEPS_KEY: avg_steps
        }

        return data