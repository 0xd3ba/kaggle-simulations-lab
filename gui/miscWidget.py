# This module takes care of creating the misc. layout for the application

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
from PyQt5.QtWidgets import (

    QPushButton,
    QWidget,
    QGridLayout,
    QComboBox,
    QTextBrowser,
    QLineEdit,
    QFileDialog
)

# Custom module imports
import config.algoConfig as acfg                   # Algorithm specific configuration information
import config.envConfig as ecfg                    # Environment configuration information


# Placeholder text constants
PLACEHOLDER_ENV_BOX   = '-- Select your Environment --'

# GUI related contstants
GUI_BUTTON_WORKSPACE = 'Change Workspace'
GUI_SELECT_WORKSPACE = 'Select Workspace'


# Text that displays the information about the competition
GUI_TEXT_BOX_TEXT = """
<html><head/><body>

<p align="center"> <a href="https://www.kaggle.com/c/hungry-geese"> <span style=" font-size:16pt; font-weight:600; 
color:#0000ff;">Hungry Geese: Don't. Stop. Eating.<br/></span></a></p>

<p>Whether it be in an arcade, on a phone, as an app, on a computer, or maybe stumbled upon in a web search, many of us 
have likely developed fond memories playing a version of Snake. It’s addicting to control a slithering serpent and watch 
it grow along the grid until you make one… wrong… move. Then you have to try again because surely you won’t make the 
same mistake twice!</p>

<p>With Hungry Geese, Kaggle has taken this classic in the video game industry and put a multi-player, simulation spin 
to it. You will create an AI agent to play against others and survive the longest. You must make sure your goose doesn’t 
starve or run into other geese; it’s a good thing that geese love peppers, donuts, and pizza—which show up across the 
board. </p>

<p> Extensive research exists in building Snake models using reinforcement learning, Q-learning, neural networks, and 
more (maybe you’ll use… Python?). Take your grid-based reinforcement learning knowledge to the next level with this 
exciting new challenge! </p>
</body></html>
"""


class MiscWidget(QWidget):
    """ Class responsible for building the misc. information subcomponent of the GUI """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.envList = ecfg.ENV_LIST

        self.mainLayout = QGridLayout(self)
        self.fileDialog = QFileDialog(parent)

        self.createProjectInfo()            # Create the project information widget
        self.createTextBox()                # Create the text box about Hungry Geese
        self.createEnvListBox()             # Create the environment selection widgets
        self.createWorkspaceBox()           # Create the workspace selection widgets


    def createProjectInfo(self):
        """ Adds the information about the project team """
        #TODO: Add it later
        pass


    def createTextBox(self):
        """ Creates the textbox widget and fills it with the text """
        self.textBrowser = QTextBrowser()
        self.textBrowser.setText(GUI_TEXT_BOX_TEXT)

        self.mainLayout.addWidget(self.textBrowser, 1, 0, 1, 4)


    def createEnvListBox(self):
        """ Creates the list boxes corresponding to selection of environments """
        self.envListBox = QComboBox()

        self.envListBox.addItem(PLACEHOLDER_ENV_BOX)
        for env in self.envList:
            self.envListBox.addItem(env)

        # Connect it to the event handler for enabling/disabling Start button
        self.envListBox.currentTextChanged.connect(self.envChangedHandler)

        # Add the widget to the layout
        self.mainLayout.addWidget(self.envListBox, 2, 0, 1, 4)


    def createWorkspaceBox(self):
        """ Creates the widget that asks the user to select the workspace directory """
        self.chooseWorkspaceBtn = QPushButton(GUI_BUTTON_WORKSPACE)
        self.currWorkspaceBox = QLineEdit()

        # The user is not allowed to tweak the value inside by typing
        self.currWorkspaceBox.setReadOnly(True)
        self.currWorkspaceBox.setPlaceholderText(os.path.abspath(os.curdir))

        # Connect the button to the handler for updating the workspace
        self.chooseWorkspaceBtn.clicked.connect(self.changeWorkspaceHandler)

        self.mainLayout.addWidget(self.currWorkspaceBox, 3, 0, 1, 3)
        self.mainLayout.addWidget(self.chooseWorkspaceBtn, 3, 3, 1, 1)


    # *****************************************
    # Below methods contains the control logic
    # for handling events that originated from
    # interacting with this subcomponent of GUI
    # *****************************************

    def envChangedHandler(self, selectedEnv):
        """ Handle the event when environment is changed """
        if selectedEnv == PLACEHOLDER_ENV_BOX:
            selectedEnv = None
        else:
            # TODO: Update the text box with the environment information
            pass

        self.parent.algoWidget.algoConfig.setEnvironment(selectedEnv)
        self.parent.startButtonEnablerDisabler()


    def changeWorkspaceHandler(self):
        """ Creates a directory selection dialog for the user to change the workspace """
        filepath = self.fileDialog.getExistingDirectory(caption=GUI_SELECT_WORKSPACE)
        self.currWorkspaceBox.setText(str(filepath))