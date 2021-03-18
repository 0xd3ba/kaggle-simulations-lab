# This module contains the base class for Kaggle environments

import config.windowConfig as wcfg

class BaseEnvironment:
    """ Base class for all Kaggle Environments """

    def __init__(self):
        self.environmentName = wcfg.DEF_ENV_TITLE                       # Default title (i.e. Project Name)
        self.environmentSubtitle = wcfg.DEF_ENV_SUBTITLE                # Default subtitle
        self.competitionLink = wcfg.DEF_ENV_LINK                        # Link to the Github Repo
        self.description = self.buildDescription(wcfg.DEF_ENV_INFO)     # Description about the project


    def buildDescription(self, paras):
        """ Builds an HTML formatted description for the environment and returns it"""

        fmt_desc = [
            '<html><head/><body>',      # Opening tag
            None,                       # The title of the competition
            None,                       # The subtitle of the competition
            None,                       # The description of the competition
            '</body></html>'            # Closing tag
        ]

        # First format the title appropriately
        fmt_title = f"""
        <p align="center"> <a href="{self.getCompetitionLink()}"> <span style=" font-size:16pt; font-weight:600; 
        color:#0000ff;"> {self.getEnvironmentName()} </span> </a> </p>
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


    def getEnvironmentName(self):
        """ Returns the name of the environment """
        return self.environmentName


    def getEnvironmentSubtitle(self):
        """ Returns the subtitle of the environment """
        return self.environmentSubtitle


    def getDescription(self):
        """ Returns the description of the competition on the environment """
        return self.description


    def getCompetitionLink(self):
        """ Returns the link of the Kaggle competition """
        return self.competitionLink


    #TODO: Add more environment related methods later