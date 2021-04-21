# This module contains the parser that will be used to parse the JSON files

import json

# *********************************************
# WARNING: Don't change the keys
#
# If there is a need to change the keys, make
# sure to reflect the changes in ALL the JSON
# files as well

JSON_ENV_TITLE = 'title'
JSON_ENV_SUBTITLE = 'subTitle'
JSON_ENV_DESC = 'description'
JSON_ENV_LINK = 'link'
JSON_ENV_SUPPORTED = 'supported'
JSON_MAX_AGENTS = 'max_agents'
# *********************************************


class EnvironmentJsonParser:
    """ Class for parsing the environment JSON file """

    def __init__(self, path):
        self.path = path            # The path to the json file
        self.title = None           # Title of the environment (string)
        self.subtitle = None        # Subtitle of the environment (string)
        self.description = None     # Description of the environment (list of paragraphs)
        self.link = None            # Link to the kaggle competition
        self.supported = None       # Is the environment supported by this lab
        self.max_agents = None      # Maximum number of agents that can be in the environment

    def parse(self):
        """ Tries to parse the JSON file. In case of any errors, the environment is skipped
            Raises a generic exception in case any issue occurs and the status message is printed
            in the terminal
        """
        path = self.getPath()
        try:
            file = open(path)
        except FileNotFoundError:
            print(f'ERROR: Could not open "{path}"')
            raise Exception

        # Alright, file exists
        # Parse it and extract the contents. Check for key errors in case
        try:
            parsed_json = json.load(file)
        except json.JSONDecodeError:
            print(f'ERROR: Parsing Error while decoding "{path}"')
            raise Exception

        file.close()    # No use for the file, now that we decoded the json
        try:
            title = parsed_json[JSON_ENV_TITLE]
            subtitle = parsed_json[JSON_ENV_SUBTITLE]
            description = parsed_json[JSON_ENV_DESC]
            link = parsed_json[JSON_ENV_LINK]
            supported = parsed_json[JSON_ENV_SUPPORTED]
            max_agents = parsed_json[JSON_MAX_AGENTS]

        except KeyError as kerr:
            print(f'ERROR: Required Key "[{kerr}]" missing from "{path}"')
            raise Exception

        # Parsing successful. Store the obtained values
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.link = link
        self.supported = supported
        self.max_agents = max_agents

    def getPath(self):
        return self.path

    def getTitle(self):
        return self.title

    def getSubtitle(self):
        return self.subtitle

    def getDescription(self):
        return self.description

    def getLink(self):
        return self.link

    def getMaxAgents(self):
        return self.max_agents

    def isEnvironmentSupported(self):
        return self.supported
