# This module contains the base class for Kaggle environments

class BaseEnvironment:
    """ Base class for all Kaggle Environments """

    def __init__(self):
        self.environmentName = None     # Name of the environment
        self.competitionLink = None     # Link to the Kaggle competition
        self.description = None         # Description about the environment


    def buildDescription(self, paras):
        """ Builds an HTML formatted description for the environment and returns it"""

        fmt_desc = [
            '<html><head/><body>',      # Opening tag
            None,                       # The title of the competition
            None,                       # The description of the competition
            '</body></html>'            # Closing tag
        ]

        # First format the title appropriately
        fmt_title = f"""
        <p align="center"> <a href="{self.getCompetitionLink()}"> <span style=" font-size:16pt; font-weight:600; 
        color:#0000ff;"> {self.getDescription()} <br/> </span> </a> </p>
        """

        # Format each of the paragraphs by embedding them inside p-tags
        # Then convert them to a single string
        fmt_paras = ['<p>' + para_i + '</p>' for para_i in paras]
        fmt_paras = '\n\n'.join(fmt_paras)

        # Update their corresponding values
        fmt_desc[1] = fmt_title
        fmt_desc[2] = fmt_paras

        # Merge the list into a single string and return it
        return "\n".join(fmt_desc)


    def getEnvironmentName(self):
        """ Returns the name of the environment """
        return self.environmentName


    def getDescription(self):
        """ Returns the description of the competition on the environment """
        return self.description


    def getCompetitionLink(self):
        """ Returns the link of the Kaggle competition """
        return self.competitionLink


    #TODO: Add more environment related methods later