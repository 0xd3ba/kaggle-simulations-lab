# Kaggle Simulations Lab -- Experiment with a wide variety of Reinforcement-Learning agents
#                           for Kaggle simulation competitions

import sys
from PyQt5.QtWidgets import QApplication

# Custom module import for GUI of the application
from gui.kaggleSimLabUI import KaggleSimLabUI
from config.environmentConfig import registerEnvironments


if __name__ == '__main__':

    # The first step is to register supported environments
    registerEnvironments()

    kaggleSimLabApp = QApplication(sys.argv)
    kaggleSimLabGui = KaggleSimLabUI()

    kaggleSimLabApp.setStyle('Fusion')      # For consistent look across various platforms
    kaggleSimLabGui.show()                  # Display the GUI of the application
    kaggleSimLabApp.exec_()                 # Start the execution loop
