# This module contains the wrapper class for Kaggle environments

import config.windowConfig as wcfg
import config.environmentConfig as ecfg
import utils.jsonParser as jsonParser


class EnvironmentWrapper:
    """ Wrapper class for all Kaggle Environments """

    def __init__(self, environment, title, subtitle, description, link, max_agents, supported):
        pass
        self.environment = environment                          # Reference to the actual environment class
        self.environmentTitle = title                           # Title of the environment
        self.environmentSubtitle = subtitle                     # Subtitle of the environment
        self.competitionLink = link                             # Link to the environment
        self.description = self.buildDescription(description)   # Description about the environment
        self.isSupported = supported                            # Is the environment supported ?
        self.maxAgents = max_agents                             # The maximum number of agents in the environment

    def buildDescription(self, paras):
        """ Builds an HTML formatted description for the environment and returns it"""

        fmt_desc = [
            '<html><head/><body>',  # Opening tag
            None,  # The title of the competition
            None,  # The subtitle of the competition
            None,  # The description of the competition
            '</body></html>'  # Closing tag
        ]

        # First format the title appropriately
        fmt_title = f"""
        <p align="center"> <a href="{self.getCompetitionLink()}"> <span style=" font-size:16pt; font-weight:600; 
        color:#0000ff;"> {self.getEnvironmentTitle()} </span> </a> </p>
        """

        fmt_subtitle = f"""
        <p align="center"> <span style=" font-size:15pt;"> 
        -- {self.getEnvironmentSubtitle()} -- <br/> </span> </a> </p>
        """

        # Format each of the paragraphs by embedding them inside p-tags
        # Then convert them to a single string
        fmt_paras = ['<p>' + para_i + '</p>' for para_i in paras]
        fmt_paras = '\n\n'.join(fmt_paras)

        # Update their corresponding values
        fmt_desc[1] = fmt_title
        fmt_desc[2] = fmt_subtitle
        fmt_desc[3] = fmt_paras

        # Merge the list into a single string and return it
        return "\n".join(fmt_desc)

    def getEnvironment(self):
        """ Returns the class reference to the environment that was stored """
        return self.environment

    def getEnvironmentTitle(self):
        """ Returns the name of the environment """
        return self.environmentTitle

    def getEnvironmentSubtitle(self):
        """ Returns the subtitle of the environment """
        return self.environmentSubtitle

    def getDescription(self):
        """ Returns the description of the competition on the environment """
        return self.description

    def getCompetitionLink(self):
        """ Returns the link of the Kaggle competition """
        return self.competitionLink

    def getMaxAgents(self):
        """ Returns the maximum number of agents of the environment """
        return self.maxAgents

    def isEnvironmentSupported(self):
        """ Returns true/false depending on whether or not the environment is supported """
        return self.isSupported

    # TODO: Add more environment related methods later
