# This module takes care of creating the main GUI for the application


from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFrame
)

# Custom module imports related to creating the subcomponents of the GUI and their functioning
import config.envConfig as ecfg
import config.windowConfig as wdw

from gui.dialogWidgets import TrainingDialog
from gui.algoWidget import AlgoWidget
from gui.miscWidget import MiscWidget


# Some useful constants
GUI_BUTTON_START = 'Start Training'


class KaggleSimLabUI(QMainWindow):
    """ The main class for the GUI """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the title of the window and the min/max dimensions
        self.setWindowTitle(wdw.GUI_TITLE_MAIN)
        self.setMinimumSize(QSize(wdw.GUI_WDW_MIN_WIDTH, wdw.GUI_WDW_MIN_HEIGHT))
        self.setMaximumSize(QSize(wdw.GUI_WDW_MAX_WIDTH, wdw.GUI_WDW_MAX_HEIGHT))

        # Create the button for starting the training and connect it to its handler
        # Set its initial state to False because the user needs to select valid entries
        # from the algorithm and the optimizer box
        self.startButton = QPushButton(GUI_BUTTON_START)
        self.startButton.setEnabled(False)
        self.startButton.clicked.connect(self.startButtonEventHandler)

        # Create the widget that'll host the other layouts
        self.mainWidget = QWidget()

        # Create the main layout -- vertical partitioning
        # Create the panel for misc. information (user directory ... etc)
        # Create the panel for algorithm selection and hyperparameters
        self.mainLayout = QVBoxLayout()
        self.miscWidget = MiscWidget(self)
        self.algoWidget = AlgoWidget(self)

        # Create a horizontal partitioning divider
        self.horzLine = QFrame()
        self.horzLine.setFrameShape(QFrame.HLine)
        self.horzLine.setFrameShadow(QFrame.Sunken)

        # Add the created layouts/widgets in order
        self.mainLayout.addWidget(self.miscWidget)
        self.mainLayout.addWidget(self.horzLine)
        self.mainLayout.addWidget(self.algoWidget)
        self.mainLayout.addWidget(self.startButton)

        # Finally add the layout to the the main widget and add it to the
        # main window of the GUI
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)


    def startButtonEnablerDisabler(self):
        """ Responsible for enabling/disabling the start button """
        currEnviron = self.algoWidget.algoConfig.getEnvironment()
        currOptim = self.algoWidget.algoConfig.getOptimizer()
        currAlgo = self.algoWidget.algoConfig.getAlgorithm()

        # The getter methods return None if the items are placeholders
        # The last check is to ensure we only enable the start button only if we support that environment
        if currOptim and currAlgo and currEnviron and currEnviron in ecfg.ENV_SUPPORTED:
            self.startButton.setEnabled(True)
        else:
            self.startButton.setEnabled(False)


    def startButtonEventHandler(self):
        """ Event handler for the 'Start' button. Creates a new dialog and starts the training loop """

        # First bundle the configuration data of the algorithm
        # Then update the None values (happens when events are not triggered) with their defaults
        configData = self.algoWidget.algoConfig.getConfigData()
        configData = self.algoWidget.algoConfig.checkAndUpdateConfigData(configData)

        self.trainDialog = TrainingDialog(self, configData)
        self.trainDialog.exec_()

        # Execution of the main widget pauses until the dialog is closed
        # Once training is done or is cancelled, execution resumes