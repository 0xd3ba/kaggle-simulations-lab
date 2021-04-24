# This module contains worker threads to start the training process
import time
from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

# Custom module imports
import utils.trainer as trainer
from utils.dispatcher import dispatcher


# Signals for the worker threads
class WorkerSignals(QObject):
    """ Signals for a running worker thread """
    finished_signal = pyqtSignal()              # Sent when execution of worker is done
    tensorboard_signal = pyqtSignal(str)        # Sent when the directory is created and command needs to be updated
    progress_signal = pyqtSignal(float)         # Sent when the progress bar needs an update
    textbox_training_signal = pyqtSignal(dict)  # Sent when the training information textbox needs an update
    textbox_showndown_signal = pyqtSignal(dict) # Sent when the training information textbox needs to update


# Worker-Thread class that is responsible for training
class Worker(QObject):
    """ A worker thread that is spawned when Train is clicked """

    def __init__(self, config_data):
        super().__init__()
        self.config_data = config_data
        self.signals = WorkerSignals()
        self.active = True

    def stop(self):
        """ Sets the stopping variable which stops the training loop """
        self.active = False

    def is_active(self):
        """ Returns the status of the worker thread -- whether it is active or not """
        return self.active

    def update_progress_bar(self, percent):
        """ Emits the signal that updates the progress bar on the GUI """
        self.signals.progress_signal.emit(percent)

    def update_textbox_training(self, data):
        """ Emits the signal that updates the textbox on the GUI """
        self.signals.textbox_training_signal.emit(data)

    def update_textbox_showdown(self, data):
        """ Emits the signal that updates the textbox on the GUI """
        self.signals.textbox_showndown_signal.emit(data)

    def update_tensorboard_cmd(self, log_dir):
        """ Emits the signal that updates the tensorboard command on the GUI """
        self.signals.tensorboard_signal.emit(log_dir)

    def run(self):
        """ Entry point of the thread. Control is passed to dispatcher with its reference """
        dispatcher(self.config_data, self)

        # Execution has been finished -- Emit the signal marking the end of execution
        self.signals.finished_signal.emit()
