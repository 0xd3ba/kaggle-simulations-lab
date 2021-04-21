# This module contains the class that stores the environment specific information

from utils.jsonParser import EnvironmentJsonParser
from environments.environmentWrapper import EnvironmentWrapper

# The classes for the kaggle environments
from environments.kaggle.hungry_geese.hungryGeese import HungryGeese
from environments.kaggle.rock_paper_scissor.rockPaperScissor import RockPaperScissor
from environments.kaggle.halite.haliteTwoSigma import HaliteTwoSigma
from environments.kaggle.connectX.connectX import ConnectX
from environments.kaggle.santa_candy_cane.santaCandyCane import SantaCandyCane
from environments.kaggle.gfootball.googleResearchFootball import GoogleResearchFootball


#########################################################################################
# Reference list of all the environments and their JSON files
# NOTE: The path to JSON file must be relative to the root of project directory
# For e.g.
#           environments/json/<your_environment_json>.json
#
ENV_LIST = {
    HungryGeese: 'environments/json/hungry_geese.json',
    RockPaperScissor: 'environments/json/rock_paper_scissor.json',
    HaliteTwoSigma: 'environments/json/halite.json',
    ConnectX: 'environments/json/connect_x.json',
    SantaCandyCane: 'environments/json/santa_candy_cane.json',
    GoogleResearchFootball: 'environments/json/gfootball.json'
}

# This is a dummy environment used to display the information about the application
DUMMY_ENVIRONMENT = None
DUMMY_ENVIRONMENT_JSON = 'environments/json/_default_lab.json'

#########################################################################################

# List of supported environments (and their mappings to the references) till now
# It's filled depending on the value of the supported flag in the environment's JSON file
ENV_SUPPORTED_LIST = []
ENV_MAP = {}


def build_dummy_environment():
    parser = EnvironmentJsonParser(DUMMY_ENVIRONMENT_JSON)
    try:
        parser.parse()
    except Exception:
        print(f'Unable to create dummy environment. Exiting.')
        exit(-1)

    global DUMMY_ENVIRONMENT
    DUMMY_ENVIRONMENT = EnvironmentWrapper(
        environment=None,
        title=parser.getTitle(),
        subtitle=parser.getSubtitle(),
        description=parser.getDescription(),
        link=parser.getLink(),
        max_agents=parser.getMaxAgents(),
        supported=False
    )


def registerEnvironments():
    """ Registers the given environment (overwrites if same title) in the supported environments """

    build_dummy_environment()

    for env, json in ENV_LIST.items():
        parser = EnvironmentJsonParser(json)

        # Try parsing the JSON file -- Might throw errors
        # In such cases, simply skip the environment
        try:
            parser.parse()
        except Exception:
            print('Skipping the environment ... ')
            continue

        # Parsing successful -- Extract the contents
        title = parser.getTitle()
        subtitle = parser.getSubtitle()
        description = parser.getDescription()
        link = parser.getLink()
        supported = parser.isEnvironmentSupported()
        max_agents = parser.getMaxAgents()

        # Add this environment to the supported list if it is supported.
        # Then go ahead and build the mapping between environment names and the wrapped environment
        if supported:
            ENV_SUPPORTED_LIST.append(title)

        ENV_MAP[title] = EnvironmentWrapper(environment=env,
                                            title=title,
                                            subtitle=subtitle,
                                            description=description,
                                            link=link,
                                            max_agents=max_agents,
                                            supported=supported)
