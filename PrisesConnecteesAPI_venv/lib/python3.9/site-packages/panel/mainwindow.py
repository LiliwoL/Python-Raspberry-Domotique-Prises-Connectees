import sys
import yaml
import os
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
from PyQt5.uic import loadUiType


# load the gui.ui file designed using QT designer
Ui_MainWindow, QMainWindow = loadUiType('panel/panel.ui')

# GUI Class to load the control panel ui
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # setup UI
        self.setupUi(self)
        self.load_config()
        self.show()

    def load_config(self):
        with open('status.yaml') as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            status = yaml.load(file, Loader=yaml.FullLoader)
            pins = status['pins']
            print(pins)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
