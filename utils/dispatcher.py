# This module takes care of starting the training loop

import os
import sys
import time

import config.algorithmsConfig as acfg
import config.environmentConfig as ecfg
import utils.nn as unn  # Module for building a neural network
import utils.trainer as utrainer  # Module for training

# Keys for directory names (also used as directory names, except ROOT_DIR)
ROOT_DIR = 'root_dir'
LOG_DIR = 'logs'  # Directory storing the TensorBoard logs
CHKPT_DIR = 'saved_models'  # Directory storing the models at checkpoints

# Status codes for returning the status of the dispatch
SUCCESS = 0  # Warning: Don't change this value
FAILED = -1

DISPATCH_ERR_INVAL_DIR = "Invalid Path. Check if the directory exists or you have write permission"


# *******************************************************************
# WARNING: Assumption is made that the directories can be created
# TODO: Handle the case when they can't be created later
# *******************************************************************
def _tryCreatingDirectory(environ, parentDir):
    """ Try creating the directory inside the given directory path (from the GUI) """

    currTime = time.asctime()  # Day Month Date Time Year
    dirName = f'{environ}-{currTime}'  # EnvironmentName-{Day Month Date ...etc }

    rootDirPath = os.path.join(parentDir, dirName)  # Path to the directory where we'll be working
    logDirPath = os.path.join(rootDirPath, LOG_DIR)  # Path to the directory for storing TensorBoard logs
    modelDirPath = os.path.join(rootDirPath, CHKPT_DIR)  # Path to the directory for storing models

    try:
        os.mkdir(rootDirPath)  # Create the main directory
        os.mkdir(logDirPath)  # Create the log directory
        os.mkdir(modelDirPath)  # Create the model directory

    except OSError:
        return FAILED, None  # Couldn't create one or more directories, fail the dispatch

    # The dictionary for the directories
    dirsDict = {
        ROOT_DIR: rootDirPath,
        LOG_DIR: logDirPath,
        CHKPT_DIR: modelDirPath
    }

    return SUCCESS, dirsDict


# *****************************************
# Dispatcher method that builds the network,
# environment ... etc before starting the
# training loop
# *****************************************

def dispatcher(configData, worker):

    env_name = configData[acfg.KEY_ENVIRONMENT]
    env_workspace = configData[acfg.KEY_WORKSPACE]
    n_agents = configData[acfg.KEY_NUM_AGENTS]
    algorithm = configData[acfg.KEY_ALGO]
    units_list = configData[acfg.KEY_UNITS_LIST]
    activ_list = configData[acfg.KEY_ACTIV_LIST]
    optim = configData[acfg.KEY_OPTIM]
    learn_rate = configData[acfg.KEY_LEARN_RATE]

    # TODO: Create a separate class to do this job
    # First create the directories that will be used to save stuff during training
    # status, createdDirs = _tryCreatingDirectory(env_name, env_workspace)
    # if status:
    #     return FAILED, [DISPATCH_ERR_INVAL_DIR]

    # Create the environment
    training_env = ecfg.ENV_MAP[env_name].getEnvironment()
    training_env = training_env(n_agents)

    # Create the neural network
    network = unn.FeedForwardNet(ip_dim=training_env.getObservationLength(),
                                 op_dim=training_env.getNumActions(),
                                 units_list=units_list,
                                 activ_list=activ_list)
    # Now create the optimizer
    optimizer = unn.buildOptimizer(network, optim, learn_rate)

    # Finally create the agent
    agent_class = acfg.get_agent(algorithm)
    agent = agent_class(env=training_env,
                        network=network,
                        optimizer=optimizer,
                        model_dir=None, #createdDirs[CHKPT_DIR],
                        log_dir=None) #createdDirs[LOG_DIR])

    # TODO: Start the training loop (and start tensorboard as well)
    trainer = utrainer.Trainer(worker_thread=worker, config_data=configData, agent=agent)
    trainer.start()
