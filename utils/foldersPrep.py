# This module is responsible for creating the folders for storing logs
# and model checkpoints periodically

import os
import time

class PrepareFolders:

    # Keys for directory names (also used as directory names, except ROOT_DIR)
    ROOT_DIR = 'root_dir'       # Directory storing the below two folders
    LOG_DIR = 'logs'            # Directory storing the TensorBoard logs
    CHKPT_DIR = 'saved_models'  # Directory storing the models at checkpoints

    def __init__(self, env_name, path):
        self.name = env_name
        self.path = path
        self.root_dir = None
        self.log_dir = None
        self.chkpt_dir = None

        currTime = time.asctime()                       # Day Month Date Time Year
        self.parentDirName = f'{self.name}-{currTime}'  # EnvironmentName-{Day Month Date ...etc }


    def get_root_dir(self):
        """ Returns the root directory of the model """
        return self.root_dir


    def get_log_dir(self):
        """ Returns the log directory of the model """
        return self.log_dir


    def get_chkpt_dir(self):
        """ Returns the log directory of the model """
        return self.chkpt_dir


    def prepare(self):
        """ Prepares all the directories """
        self.create_root_dir()
        self.create_log_dir()
        self.create_checkpoint_dir()


    def create_root_dir(self):
        """ Creates the root directory for storing other information """
        root_path = os.path.join(self.path, self.parentDirName)  # Path to the directory where we'll be working
        try:
            os.mkdir(root_path)
            self.root_dir = root_path
        except OSError:
            print(f'WARNING: Unable to create root directory {root_path} -- Other directories will also not be created')


    def create_log_dir(self):
        """ Creates the log directory within the root directory """
        if self.root_dir is None:
            print('WARNING: Root directory is not present. Skipping creation of logs directory')
            return

        logs_path = os.path.join(self.root_dir, self.LOG_DIR)  # Path to the directory for storing TensorBoard logs
        try:
            os.mkdir(logs_path)
            self.log_dir = logs_path
        except OSError:
            print(f'WARNING: Unable to create log directory {logs_path}')



    def create_checkpoint_dir(self):
        """ Creates the checkpoint directory within the root directory """
        if self.root_dir is None:
            print('WARNING: Root directory is not present. Skipping creation of checkpoint directory')
            return

        chkpt_path = os.path.join(self.root_dir, self.CHKPT_DIR)  # Path to the directory for storing models
        try:
            os.mkdir(chkpt_path)
            self.chkpt_dir = chkpt_path
        except OSError:
            print(f'WARNING: Unable to create checkpoint directory {chkpt_path}')