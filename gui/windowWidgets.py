# This module contains classes for custom window widget creation

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QDialog,
    QGridLayout,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QMessageBox
)

# Some useful window constants
GUI_WDW_MIN_WIDTH  = 400
GUI_WDW_MIN_HEIGHT = 600
GUI_WDW_MAX_WIDTH  = 540
GUI_WDW_MAX_HEIGHT = 900

GUI_TITLE_MAIN = 'Kaggle Simulations Lab'
