import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore

class BrightnessControl(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Brightness Control')
        self.setWindowIcon(QtGui.QIcon(self.resource_path('images/brightness-icon.png')))

        self.brightness_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.brightness_slider.setMinimum(20)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(50)
        self.brightness_slider.valueChanged.connect(self.update_brightness_label)

        self.brightness_label = QtWidgets.QLabel('50%', self)

        self.language_combo = QtWidgets.QComboBox(self)
        self.language_combo.addItem('English')
        self.language_combo.addItem('Polski')
        self.language_combo.currentIndexChanged.connect(self.change_language)

        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon(self.resource_path('images/brightness-icon.png')))
        self.tray_icon.activated.connect(self.tray_icon_activated)

        self.exit_action = QtWidgets.QAction("Exit", self)
        self.exit_action.triggered.connect(QtWidgets.qApp.quit)

        self.tray_menu = QtWidgets.QMenu(self)
        self.tray_menu.addAction(self.exit_action)
        self.tray_icon.setContextMenu(self.tray_menu)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.brightness_slider)
        layout.addWidget(self.brightness_label)
        layout.addWidget(self.language_combo)
        self.setLayout(layout)

        self.tray_icon.show()

    def update_brightness_label(self, value):
        self.brightness_label.setText(f'{value}%')

    def change_language(self, index):
        if index == 0:
            self.setWindowTitle('Brightness Control')
        else:
            self.setWindowTitle('Podświetlenie ekranu')

    def tray_icon_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.show()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               "Do you want to minimize to tray instead of exiting?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            event.ignore()
            self.hide()
        else:
            event.accept()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = BrightnessControl()
    ex.show()
    sys.exit(app.exec_())
