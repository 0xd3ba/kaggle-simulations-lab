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
import environments.baseEnvironment as baseenv     # Custom Base environment


# Placeholder text constants
PLACEHOLDER_ENV_BOX   = '-- Select your Environment --'

# GUI related contstants
GUI_BUTTON_WORKSPACE = 'Change Workspace'
GUI_SELECT_WORKSPACE = 'Select Workspace'


class MiscWidget(QWidget):
    """ Class responsible for building the misc. information subcomponent of the GUI """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent
        self.envMap = ecfg.ENV_MAP
        self._baseEnv = baseenv.BaseEnvironment()

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

        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setText(self._baseEnv.getDescription())

        self.mainLayout.addWidget(self.textBrowser, 1, 0, 1, 4)


    def createEnvListBox(self):
        """ Creates the list boxes corresponding to selection of environments """
        self.envListBox = QComboBox()

        self.envListBox.addItem(PLACEHOLDER_ENV_BOX)
        for env in self.envMap.keys():
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
            self.textBrowser.setText(self._baseEnv.getDescription())    # Reset the textbox with default description
        else:
            # Update the textbox with the description of the environment
            self.textBrowser.setText(self.envMap[selectedEnv]().getDescription())

        self.parent.algoWidget.algoConfig.setEnvironment(selectedEnv)
        self.parent.startButtonEnablerDisabler()


    def changeWorkspaceHandler(self):
        """ Creates a directory selection dialog for the user to change the workspace """
        filepath = self.fileDialog.getExistingDirectory(caption=GUI_SELECT_WORKSPACE)
        self.currWorkspaceBox.setText(str(filepath))