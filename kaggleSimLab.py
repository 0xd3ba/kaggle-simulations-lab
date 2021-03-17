# Kaggle Simulations Lab -- Experiment with a wide variety of Reinforcement-Learning agents
#                           for Kaggle simulation competitions

import sys
from PyQt5.QtWidgets    import QApplication

# Custom module import for GUI of the application
from gui.kaggleSimLabUI import KaggleSimLabUI


if __name__ == '__main__':
    kaggleSimLabApp = QApplication(sys.argv)
    kaggleSimLabGui = KaggleSimLabUI()

    kaggleSimLabApp.setStyle('Fusion')      # For consistent look across various platforms
    kaggleSimLabGui.show()                  # Display the GUI of the application
    kaggleSimLabApp.exec_()                 # Start the execution loop
