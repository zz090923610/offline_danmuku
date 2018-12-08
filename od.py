import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class TransparentWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.3)
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))
        painter.drawRect(self.rect())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # Create the main window
    window = TransparentWindow()

    # Create the button
    pushButton = QtWidgets.QPushButton(window)
    pushButton.setGeometry(QtCore.QRect(240, 190, 90, 31))
    pushButton.setText("Finished")
    pushButton.clicked.connect(app.quit)

    # Center the button
    qr = pushButton.frameGeometry()
    cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    pushButton.move(qr.topLeft())

    # Run the application
    window.showFullScreen()
    sys.exit(app.exec_())
