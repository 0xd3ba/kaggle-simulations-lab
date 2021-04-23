# This module takes care of starting the training loop

import config.algorithmsConfig as acfg
import config.environmentConfig as ecfg
import utils.nn as unn              # Module for building a neural network
import utils.trainer as utrainer    # Module for training
import utils.foldersPrep as fprep   # Module for creating the directories


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
    n_warmup = configData[acfg.KEY_NUM_WARMUP]

    # Create the directories, if possible
    folder_prep = fprep.PrepareFolders(env_name=env_name, path=env_workspace)
    folder_prep.prepare()

    # Create the environment
    training_env = ecfg.ENV_MAP[env_name].getEnvironment()
    training_env = training_env(n_agents, n_warmup)

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
                        model_dir=folder_prep.get_chkpt_dir(),
                        log_dir=folder_prep.get_log_dir())

    trainer = utrainer.Trainer(worker_thread=worker,
                               config_data=configData,
                               agent=agent)

    # Everything is ready. Start the training loop
    trainer.start()
