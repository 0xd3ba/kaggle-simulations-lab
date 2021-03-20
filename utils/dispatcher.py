# This module takes care of starting the training loop

import os
import sys
import time

import config.algoConfig as acfg
import config.envConfig as ecfg
import utils.nn as unn                      # Module for building a neural network


# Keys for directory names (also used as directory names, except ROOT_DIR)
ROOT_DIR  = 'root_dir'
LOG_DIR   = 'logs'                          # Directory storing the TensorBoard logs
CHKPT_DIR = 'saved_models'                  # Directory storing the models at checkpoints

# Status codes for returning the status of the dispatch
SUCCESS = 0                                 # Warning: Don't change this value
FAILED  = -1


DISPATCH_ERR_INVAL_DIR = "Invalid Path. Check if the directory exists or you have write permission"


def _tryCreatingDirectory(environ, parentDir):
    """ Try creating the directory inside the given directory path (from the GUI) """

    currTime = time.asctime()                               # Day Month Date Time Year
    dirName = f'{environ}-{currTime}'                       # EnvironmentName-{Day Month Date ...etc }

    rootDirPath = os.path.join(parentDir, dirName)          # Path to the directory where we'll be working
    logDirPath = os.path.join(rootDirPath, LOG_DIR)         # Path to the directory for storing TensorBoard logs
    modelDirPath = os.path.join(rootDirPath, CHKPT_DIR)     # Path to the directory for storing models

    try:
        os.mkdir(rootDirPath)                               # Create the main directory
        os.mkdir(logDirPath)                                # Create the log directory
        os.mkdir(modelDirPath)                              # Create the model directory

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

def dispatcher(configData, trainingTextBox, progressBar):
    """ """

    # First create the directories that will be used to save stuff during training
    status, createdDirs = _tryCreatingDirectory(configData[acfg.KEY_ENVIRONMENT], configData[acfg.KEY_WORKSPACE])
    if status:
        return FAILED, [DISPATCH_ERR_INVAL_DIR]

    # Create the environment
    env_name = configData[acfg.KEY_ENVIRONMENT]
    training_env = ecfg.ENV_MAP[env_name]()

    # Create the neural network
    network = unn.build_fc_net(env=training_env,
                               nLayers=configData[acfg.KEY_NUM_LAYERS],
                               unitsList=configData[acfg.KEY_UNITS_LIST],
                               activList=configData[acfg.KEY_ACTIV_LIST]
                               )

    #TODO: Make updates to the environment classes to work with tf-agents
    #TODO: Start the training loop (and start tensorboard as well)

    return SUCCESS, None