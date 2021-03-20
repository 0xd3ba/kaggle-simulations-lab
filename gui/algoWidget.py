# This module takes care of creating the algorithm layout for the application

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QComboBox,
    QLabel,
    QSpinBox,
    QDoubleSpinBox
)

# Custom module imports
from gui.dialogWidgets import LayerConfigDialog    # Window module for layer configuration
import config.algoConfig as acfg                   # Custom algorithm configuration module


# Placeholder text constants
PLACEHOLDER_ALGO_BOX  = '-- Select your Algorithm --'
PLACEHOLDER_OPTIM_BOX = '-- Select your Optimizer --'

# GUI related contstants
GUI_LABEL_LEARNRATE     = 'Learning Rate'
GUI_LABEL_NUM_LAYERS    = 'Number of Layers'
GUI_LABEL_NUM_EPOCHS    = 'Training Epochs'
GUI_LABEL_MODEL_UPDATE  = 'Model Update Interval'
GUI_BUTTON_CONFIG_LAYER = 'Configure'
GUI_LEARNRATE_PRECISION = 9
GUI_LEARNRATE_STEP      = 1e-9


class AlgoWidget(QWidget):
    """ Class responsible for building the Algorithm configuration subcomponent of the GUI """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent                # Store a reference to the parent container
        self.algoConfig = acfg.AlgoConfig() # Create an instance for storing algorithm configuration info
        self.algoMap = acfg.ALGO_MAP        # Store a local mapping of the algorithms
        self.optimMap = acfg.OPTIM_LIST     # Store a local mapping of the optimizers

        self.mainLayout = QGridLayout(self) # Create the layout -- Grid layout

        self.createAlgoListBox()            # Create the algorithm selection box
        self.createOptimListBox()           # Create the optimizer selection box
        self.createLearnRate()              # Create the learning rate spinbox along with label
        self.createNumLayers()              # Create the number of layers widgets
        self.createNumEpochs()              # Create the epoch selection widgets
        self.createModelUpdateInterval()    # Create the update interval widgets


    def createAlgoListBox(self):
        """ Creates the list box widget for algorithm selection and adds it to the layout """
        self.algoListBox = QComboBox()

        self.algoListBox.addItem(PLACEHOLDER_ALGO_BOX)
        for algo in self.algoMap.keys():
            self.algoListBox.addItem(algo)

        # Connect it to the event handler for enabling/disabling Start button
        self.algoListBox.currentTextChanged.connect(self.listItemChangedHandler)

        # Add the widget to the layout
        self.mainLayout.addWidget(self.algoListBox, 0, 0, 1, 4)


    def createOptimListBox(self):
        """ Creates the list box widget for optimizer selection and adds it to the layout """
        self.optimListBox = QComboBox()

        self.optimListBox.addItem(PLACEHOLDER_OPTIM_BOX)
        for opt in self.optimMap:
            self.optimListBox.addItem(opt)

        # Connect it to the event handler for enabling/disabling Start button
        self.optimListBox.currentTextChanged.connect(self.listItemChangedHandler)

        self.mainLayout.addWidget(self.optimListBox, 1, 0, 1, 4)


    def createLearnRate(self):
        """ Creates the spinbox widget for learning rate and adds it to layout (along with label) """
        self.learnRateBox = QDoubleSpinBox()
        self.learnRateLabel = QLabel(GUI_LABEL_LEARNRATE)

        # So that we don't allow setting negative learning rates
        # Set decimal precision to GUI_LEARNRATE_PRECISION
        # Set the update step to be GUI_LEARNRATE_STEP
        self.learnRateBox.setMinimum(0.0)
        self.learnRateBox.setDecimals(GUI_LEARNRATE_PRECISION)
        self.learnRateBox.setSingleStep(GUI_LEARNRATE_STEP)

        # Connect it to it's respective handler
        self.learnRateBox.valueChanged.connect(self.learnRateHandler)

        self.mainLayout.addWidget(self.learnRateBox, 2, 1, 1, 3)
        self.mainLayout.addWidget(self.learnRateLabel, 2, 0, 1, 1)


    def createNumLayers(self):
        """ Creates the appropriate widgets for setting number of layers """
        self.numLayersLabel = QLabel(GUI_LABEL_NUM_LAYERS)
        self.numLayersBox = QSpinBox()
        self.numLayersConfigButton = QPushButton(GUI_BUTTON_CONFIG_LAYER)
        
        self.numLayersBox.setMinimum(1)     # Set the minimum number of hidden layers to 1

        # Connect the handlers corresponding to the config button and the spinbox
        self.numLayersBox.valueChanged.connect(self.numLayersHandler)
        self.numLayersConfigButton.clicked.connect(self.configLayersHandler)

        self.mainLayout.addWidget(self.numLayersLabel, 4, 0, 1, 1)
        self.mainLayout.addWidget(self.numLayersBox, 4, 1, 1, 2)
        self.mainLayout.addWidget(self.numLayersConfigButton, 4, 3, 1, 1)


    def createNumEpochs(self):
        """ Creates the appropriate widgets of setting up the total number of epochs """
        self.numEpochsLabel = QLabel(GUI_LABEL_NUM_EPOCHS)
        self.numEpochsBox = QSpinBox()

        self.numEpochsBox.setMinimum(1)     # Set the minimum number of training epochs to 1
        self.numEpochsBox.setMaximum(1e8)   # Set the maximum number of training epochs

        # Connect the handler for change in epochs value
        self.numEpochsBox.valueChanged.connect(self.numEpochsHandler)

        self.mainLayout.addWidget(self.numEpochsLabel, 6, 0, 1, 1)
        self.mainLayout.addWidget(self.numEpochsBox, 6, 1, 1, 3)


    def createModelUpdateInterval(self):
        """ Creates the appropriate widgets for setting up the model update interval """
        self.modelUpdateLabel = QLabel(GUI_LABEL_MODEL_UPDATE)
        self.modelUpdateBox = QSpinBox()


        self.modelUpdateBox.setMinimum(1)   # Set the minimum number of interval to 1

        # Connect it to its respective handler
        self.modelUpdateBox.valueChanged.connect(self.intervalUpdateHandler)

        self.mainLayout.addWidget(self.modelUpdateLabel, 7, 0, 1, 1)
        self.mainLayout.addWidget(self.modelUpdateBox, 7, 1, 1, 3)


    # *****************************************
    # Below methods contains the control logic
    # for handling events that originated from
    # interacting with this subcomponent of GUI
    # *****************************************

    def listItemChangedHandler(self, itemText):
        """ Responsible to updating values and enabling/disabling the start button in the parent container """

        # Enable/Disable the button only when the items in the algorithm box and optimizer
        # box are not the placeholder items
        currAlgoText = self.algoListBox.currentText()
        currOptimText = self.optimListBox.currentText()

        # Update the values accordingly
        if currAlgoText == PLACEHOLDER_ALGO_BOX:
            currAlgoText = None

        if currOptimText == PLACEHOLDER_OPTIM_BOX:
            currOptimText = None


        self.algoConfig.setAlgorithm(currAlgoText)
        self.algoConfig.setOptimizer(currOptimText)

        # Enable/Disable the start button accordingly
        self.parent.startButtonEnablerDisabler()


    def learnRateHandler(self, learnRate):
        """ Handler for updating the change in learning rate """
        self.algoConfig.setLearningRate(learnRate)


    def numLayersHandler(self, numLayers):
        """ Handler for updating the change in the number of layers """
        self.algoConfig.setNumLayers(numLayers)

        # Reset the values in algorithm configuration
        self.algoConfig.setLayerList(units=None,
                                     activations=None)


    def configLayersHandler(self):
        """ Creates a new dialog that asks the user for layer configuration """
        numLayers = self.numLayersBox.value()
        self.configDialog = LayerConfigDialog(self.parent, self, numLayers)
        self.configDialog.exec_()


    def numEpochsHandler(self, numEpochs):
        """ Handler for updating the change in the number of epochs """
        self.algoConfig.setNumEpochs(numEpochs)


    def intervalUpdateHandler(self, interval):
        """ Handler for updating the change in the model update interval """
        self.algoConfig.setUpdateInterval(interval)