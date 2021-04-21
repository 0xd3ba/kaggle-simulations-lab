# This module contains custom dialog widgets for the GUI
import os
import pyperclip
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QPushButton,
    QLabel,
    QSpinBox,
    QComboBox,
    QDialogButtonBox,
    QTextBrowser,
    QProgressBar,
    QMessageBox,
    QLineEdit,
)

# Custom module imports
import config.algorithmsConfig as acfg         # Module containing algorithm configuration information
import config.windowConfig as winw             # Module containing window configuration information
import utils.dispatcher as udispatch           # Module containing the dispatcher

# Constants for dialog titles
import utils.nn

DIALOG_TITLE_LAYER_CFG = 'Configure the Hidden Layers'
DIALOG_TITLE_TRAINING  = 'Training the agent ...'
DIALOG_TITLE_ERROR_MSG = 'Error(s) have occurred'

# Constant for dialog textbox
DIALOG_TEXTBOX_TRAIN_CONFIG = 'Starting TensorBoard server ...'

# Constant for tensorboard
# The command needs to be appended with the log-directory
DIALOG_TENSORBOARD_LABEL = 'Execute the command on terminal to start TensorBoard server '
DIALOG_TENSORBOARD_CMD = 'tensorboard --logdir '
DIALOG_TENSORBOARD_COPY = 'Copy Command'

# Constants for LayerConfigDialog
LAYER_CONFIG_NUNITS_LABEL = 'Number of Units'
LAYER_CONFIG_ACTIV_LABEL  = 'Activation Function'

LAYER_CONFIG_MIN_UNITS    = 1
LAYER_CONFIG_MAX_UNITS    = 2048

# Constants for GUI buttons
GUI_BUTTON_CANCEL = 'Cancel'
GUI_BUTTON_CLOSE  = 'Close'


class ErrorDialog(QMessageBox):
    """ Class for displaying error messages, if any """

    def __init__(self, parent, messageList):
        super().__init__(parent)

        self.setWindowTitle(DIALOG_TITLE_ERROR_MSG)
        self.setStandardButtons(QMessageBox.Ok)         # Only OK button is needed
        self.setIcon(QMessageBox.Critical)              # Set the icon to critical icon

        # Order the messages in the list and combine them to a single string
        messages = [f'{i+1}. {msg}' for i, msg in enumerate(messageList)]
        messages = '\n\n'.join(messages)

        # Finally set the message on the dialog
        self.setText(messages)


class LayerConfigDialog(QDialog):
    """ Class for the window responsible for setting up the individual layer configurations """

    def __init__(self, mainParent, algoWidget, numLayers, *args, **kwargs):
        super().__init__(mainParent)

        self.setWindowTitle(DIALOG_TITLE_LAYER_CFG)
        self.setMinimumWidth(winw.GUI_WDW_MIN_WIDTH)
        self.setMaximumWidth(winw.GUI_WDW_MAX_WIDTH)

        self.algoWidget = algoWidget                # Store a reference to the algorithm configuration widget
        self.mainLayout = QGridLayout()             # Create the main layout for this window -- Grid Layout
        self.lyrUnits = [None] * numLayers          # Create the list to store the number of units in each layer
        self.lyrActiv = [None] * numLayers          # Create the list to store the activation used in each layer
        self.activList = utils.nn.ACTIV_MAP.keys()  # Store a reference to the list of activations supported
        self.numLayers = numLayers                  # Store the number of hidden layers

        self.createLayerWidgets(numLayers)          # Create the widgets corresponding to the layers and their activations
        self.createOptionButtons()                  # Create the OK/Cancel button for saving the changes

        self.setLayout(self.mainLayout)


    def createLayerWidgets(self, numLayers):
        """ Creates numLayers number of list boxes for hidden units and activations """
        self.numUnitsLabel = QLabel(LAYER_CONFIG_NUNITS_LABEL)
        self.activLabel = QLabel(LAYER_CONFIG_ACTIV_LABEL)

        self.mainLayout.addWidget(self.numUnitsLabel, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.activLabel, 0, 2, 1, 2)

        prevUnits, prevActvs = self.algoWidget.algoConfig.getLayerList()

        # Now add the widgets corresponding to number of units and activations
        for i in range(numLayers):

            numUnitsBox = QSpinBox()
            activListBox = QComboBox()

            # Add in the activations to the activation list box
            for activation in self.activList:
                activListBox.addItem(activation)

            numUnitsBox.setMinimum(LAYER_CONFIG_MIN_UNITS)      # Set the minimum value for the number of hidden units
            numUnitsBox.setMaximum(LAYER_CONFIG_MAX_UNITS)      # Set the maximum value for the number of hidden units

            # Get the values stored in algoConfig (if not None)
            # and set their values in the corresponding widgets here
            if prevUnits is not None:
                numUnitsBox.setValue(prevUnits[i])
                activListBox.setCurrentText(prevActvs[i])       # (prevUnits != None) automatically implies this

            # Save their references
            self.lyrUnits[i] = numUnitsBox
            self.lyrActiv[i] = activListBox

            # Add them to the dialog widget
            self.mainLayout.addWidget(numUnitsBox, i+1, 0, 1, 2)
            self.mainLayout.addWidget(activListBox, i+1, 2, 1, 2)


    def createOptionButtons(self):
        """ Creates the OK/Cancel buttons for the configuration dialog """
        self.optionBtn = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Connect the OK button with the handler to save the information in the algorithm configuration
        # instance (stored in AlgoWidget). No need to connect the cancel button as the default values
        # are already set to None
        self.optionBtn.accepted.connect(self.configOkHandler)
        self.optionBtn.rejected.connect(self.configCancelHandler)

        self.mainLayout.addWidget(self.optionBtn, self.numLayers+1, 0, 1, 4)


    # *****************************************
    # Below methods contains the control logic
    # for handling events that originated from
    # interacting with this subcomponent of GUI
    # *****************************************

    def configOkHandler(self):
        """ Saves the information of the layer configuration in the AlgoConfig instance """
        # Extract the values currently stored in the widgets
        layerUnits = [unitBox.value() for unitBox in self.lyrUnits]
        layerActiv = [activBox.currentText() for activBox in self.lyrActiv]

        # Update the values in the algorithm confifuration instance
        self.algoWidget.algoConfig.setLayerList(units=layerUnits,
                                                activations=layerActiv)
        self.close()


    def configCancelHandler(self):
        """ Responsible for simply closing the dialog """
        self.close()



class TrainingDialog(QDialog):
    """ Class responsible for creating the (animated) algorithm training dialog """

    def __init__(self, mainParent, config, *args, **kwargs):
        super().__init__(mainParent)

        self.setWindowTitle(DIALOG_TITLE_TRAINING)
        self.setMinimumWidth(winw.GUI_WDW_MIN_WIDTH)
        self.setMaximumWidth(winw.GUI_WDW_MAX_WIDTH)

        self.parent = mainParent                    # Store a reference to the main parent widget
        self.config = config                        # The configuration information for the current training session
        self.mainLayout = QGridLayout()             # Create the main layout for this window -- Grid Layout

        self.createTensorBoardLinkBox()             # List box corresponding to tensorboard server link
        self.createConfigInfoTextBox()              # Textbox corresponding to displaying current algorithm config.
        self.createTrainingInfoTextBox()            # Textbox corresponding to displaying tensorboard links and all
        self.createProgressBar()                    # Progress bar to track the training progress so far
        self.createOptionButtons()                  # Option buttons to cancel the training

        self.setLayout(self.mainLayout)


    def _writeConfigInfo(self):
        """ Writes the configuration information to the left text box """
        fmt_config = [
            '<html><head/><body>',  # Opening tag
            None,                   # 1. Workspace directory
            None,                   # 2. The title of the competition
            None,                   # 3. Algorithm that is being used
            None,                   # 4. Number of layers
            None,                   # 5. Layer configuration (units per-layer and activations)
            None,                   # 6. Optimizer that is being used
            None,                   # 7. Learning rate
            None,                   # 8. Number of training epochs
            None,                   # 9. How often is the best model updated, i.e. model update interval
            '</body></html>'        # Closing tag
        ]

        fmt_config[1] = f'<p> <b>Workspace: </b> {self.config[acfg.KEY_WORKSPACE]} </p>'
        fmt_config[2] = f'<p> <b>Environment: </b> {self.config[acfg.KEY_ENVIRONMENT]} </p>'
        fmt_config[3] = f'<p> <b>Algorithm: </b> {self.config[acfg.KEY_ALGO]} </p>'
        fmt_config[4] = f'<p> <b>Number of (hidden) Layers: </b> {self.config[acfg.KEY_NUM_LAYERS]} </p>'
        fmt_config[5] = '\n'.join([
            f'({units}, {activ}) <br/>' for units, activ in zip(self.config[acfg.KEY_UNITS_LIST],
                                                                self.config[acfg.KEY_ACTIV_LIST])
        ]) + '<p></p>'

        fmt_config[6] = f'<p> <b>Optimizer: </b> {self.config[acfg.KEY_OPTIM]} </p>'
        fmt_config[7] = f'<p> <b>Learning Rate: </b> {self.config[acfg.KEY_LEARN_RATE]} </p>'
        fmt_config[8] = f'<p> <b>Training Epochs: </b> {self.config[acfg.KEY_NUM_EPISODES]} </p>'
        fmt_config[9] = f'<p> <b>Update Interval: </b> {self.config[acfg.KEY_UPDATE_INT]} </p>'

        fmt_config_str = '\n'.join(fmt_config)
        self.configInfoTextBox.setText(fmt_config_str)


    def createTensorBoardLinkBox(self):
        """ Creates the box that contains the tensorboard server link """
        workspace_dir = self.config[acfg.KEY_WORKSPACE]
        log_dir = os.path.join(workspace_dir, udispatch.LOG_DIR)
        tboard_cmd = DIALOG_TENSORBOARD_CMD + log_dir

        # For monospaced font in the command
        font = QFont()
        font.setFamily("Monospace")
        font.setFixedPitch(True)

        # Create the widgets for label and the command
        self.tboardLabel = QLabel(DIALOG_TENSORBOARD_LABEL)
        self.tboardCmd = QLineEdit()
        self.tboardCopyButton = QPushButton(DIALOG_TENSORBOARD_COPY)

        self.tboardCopyButton.clicked.connect(self.tensorBoardCopyCommand)

        # Set the widget to be read-only and update the text with the tensorboard command
        self.tboardCmd.setReadOnly(True)
        self.tboardCmd.setPlaceholderText(tboard_cmd)
        self.tboardCmd.setFont(font)

        # TODO: Add a button for copying the link to clipboard

        # Finally add them to the main layout
        self.mainLayout.addWidget(self.tboardLabel, 0, 0, 1, 4)
        self.mainLayout.addWidget(self.tboardCmd, 1, 0, 1, 3)
        self.mainLayout.addWidget(self.tboardCopyButton, 1, 3, 1, 1)



    def createConfigInfoTextBox(self):
        """ Creates the textbox widget that displays the algorithm training information """
        self.configInfoTextBox = QTextBrowser()
        self._writeConfigInfo()

        self.mainLayout.addWidget(self.configInfoTextBox, 2, 0, 1, 2)


    def createTrainingInfoTextBox(self):
        """ Creates the textbox widget that displays the statistics of the training """
        self.trainingInfoTextBox = QTextBrowser()
        self.trainingInfoTextBox.setText(DIALOG_TEXTBOX_TRAIN_CONFIG)
        self.trainingInfoTextBox.setOpenExternalLinks(True)

        self.mainLayout.addWidget(self.trainingInfoTextBox, 2, 2, 1, 2)


    def createProgressBar(self):
        """ Creates the progress bar that keeps track of the epochs completed so far """
        self.progressBar = QProgressBar()
        self.mainLayout.addWidget(self.progressBar, 3, 0, 1, 4)


    def createOptionButtons(self):
        """ Creates the buttons Close and Cancel and adds them to this widget """
        self.closeBtn = QPushButton(GUI_BUTTON_CLOSE)
        self.cancelBtn = QPushButton(GUI_BUTTON_CANCEL)

        self.closeBtn.clicked.connect(self.closeButtonClicked)
        self.cancelBtn.clicked.connect(self.cancelButtonClicked)

        # Initially close button is disabled. It's enabled only when training is complete
        # When training completes, the cancel button gets disabled
        self.closeBtn.setEnabled(False)

        self.mainLayout.addWidget(self.cancelBtn, 4, 3, 1, 1)
        self.mainLayout.addWidget(self.closeBtn, 4, 2, 1, 1)

    # *****************************************
    # Below methods contains the control logic
    # for handling events that originated from
    # interacting with this subcomponent of GUI
    # *****************************************

    def closeButtonClicked(self):
        """ Does nothing but closes the window """
        # TODO: Stop TensorBoard server process that was forked
        self.close()

    def cancelButtonClicked(self):
        """ Stops the algorithm, saves the model, stops tensorboard and closes """
        #TODO: Do the above mentioned stuff
        self.close()

    def tensorBoardCopyCommand(self):
        """ Copies the provided command of tensorboard into clipboard """
        pyperclip.copy(self.tboardCmd.text())