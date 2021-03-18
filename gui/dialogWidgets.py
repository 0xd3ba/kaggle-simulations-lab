# This module contains custom dialog widgets for the GUI

from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QPushButton,
    QLabel,
    QSpinBox,
    QComboBox,
    QDialogButtonBox,
    QTextBrowser,
    QProgressBar
)

# Custom module imports
import config.algoConfig as acfg               # Module containing algorithm configuration information
import config.windowConfig as winw             # Module containing window configuration information


# Constants for dialog titles
DIALOG_TITLE_LAYER_CFG = 'Configure the Hidden Layers'
DIALOG_TITLE_TRAINING  = 'Training the agent ...'

# Constants for LayerConfigDialog
LAYER_CONFIG_NUNITS_LABEL = 'Number of Units'
LAYER_CONFIG_ACTIV_LABEL  = 'Activation Function'

LAYER_CONFIG_MIN_UNITS    = 1
LAYER_CONFIG_MAX_UNITS    = 2048

# Constants for GUI buttons
GUI_BUTTON_CANCEL = 'Cancel'
GUI_BUTTON_CLOSE  = 'Close'


class LayerConfigDialog(QDialog):
    """ Class for the window responsible for setting up the individual layer configurations """

    def __init__(self, mainParent, algoWidget, numLayers, *args, **kwargs):
        super().__init__(mainParent)

        self.setWindowTitle(DIALOG_TITLE_LAYER_CFG)
        self.setMinimumWidth(winw.GUI_WDW_MIN_WIDTH)
        self.setMaximumWidth(winw.GUI_WDW_MAX_WIDTH)

        self.algoWidget = algoWidget        # Store a reference to the algorithm configuration widget
        self.mainLayout = QGridLayout()     # Create the main layout for this window -- Grid Layout
        self.lyrUnits = [None] * numLayers  # Create the list to store the number of units in each layer
        self.lyrActiv = [None] * numLayers  # Create the list to store the activation used in each layer
        self.activList = acfg.ACTIV_LIST    # Store a reference to the list of activations supported
        self.numLayers = numLayers          # Store the number of hidden layers

        self.createLayerWidgets(numLayers)  # Create the widgets corresponding to the layers and their activations
        self.createOptionButtons()          # Create the OK/Cancel button for saving the changes

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

        self.createConfigInfoTextBox()               # Textbox corresponding to displaying current algorithm config.
        self.createTrainingInfoTextBox()            # Textbox corresponding to displaying tensorboard links and all
        self.createProgressBar()                    # Progress bar to track the training progress so far
        self.createOptionButtons()                  # Option buttons to cancel the training

        self.setLayout(self.mainLayout)


    def _writeConfigInfo(self):
        """ Writes the configuration information to the left text box """
        #TODO: Write the confifuration information
        pass


    def createConfigInfoTextBox(self):
        """ Creates the textbox widget that displays the algorithm training information """
        self.algoInfoTextBox = QTextBrowser()
        self._writeConfigInfo()

        self.mainLayout.addWidget(self.algoInfoTextBox, 0, 0, 1, 2)


    def createTrainingInfoTextBox(self):
        """ Creates the textbox widget that displays the statistics of the training """
        self.trainingInfoTextBox = QTextBrowser()
        # self.trainingInfoTextBox.setText('')

        self.mainLayout.addWidget(self.trainingInfoTextBox, 0, 2, 1, 2)


    def createProgressBar(self):
        """ Creates the progress bar that keeps track of the epochs completed so far """
        self.progressBar = QProgressBar()
        self.mainLayout.addWidget(self.progressBar, 1, 0, 1, 4)


    def createOptionButtons(self):
        """ Creates the buttons Close and Cancel and adds them to this widget """
        self.closeBtn = QPushButton(GUI_BUTTON_CLOSE)
        self.cancelBtn = QPushButton(GUI_BUTTON_CANCEL)

        self.closeBtn.clicked.connect(self.closeButtonClicked)
        self.cancelBtn.clicked.connect(self.cancelButtonClicked)

        # Initially close button is disabled. It's enabled only when training is complete
        # When training completes, the cancel button gets disabled
        self.closeBtn.setEnabled(False)

        self.mainLayout.addWidget(self.cancelBtn, 2, 3, 1, 1)
        self.mainLayout.addWidget(self.closeBtn, 2, 2, 1, 1)

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