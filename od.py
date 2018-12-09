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


def sliding_label(parent, text, h_idx):
    label = QtWidgets.QLabel(parent)
    label.setText("<font color='White'>%s</font>" % text)
    f = label.font()
    f.setBold(True)
    f.setPointSize(25)
    label.setFont(f)
    label.setWordWrap(True)
    width = label.fontMetrics().boundingRect(label.text()).width()
    height = label.fontMetrics().boundingRect(label.text()).height()
    print(width, height)
    label.show()
    animation = QtCore.QPropertyAnimation(label, "geometry".encode())
    animation.setDuration(6000)
    animation.setKeyValueAt(0, QtCore.QRect(1920, h_idx, width, height))
    animation.setKeyValueAt(1, QtCore.QRect(0 - width, h_idx, width, height))
    return animation, height


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TransparentWindow()

    pushButton = QtWidgets.QPushButton(window)
    pushButton.setText("Finished")
    pushButton.clicked.connect(app.quit)

    qr = pushButton.frameGeometry()
    cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    pushButton.move(qr.topLeft())
    h_idx = 10
    a1, h1 = sliding_label(window, "3333", h_idx)
    h_idx += h1 + 2
    a2, h2 = sliding_label(window, '5555ddddddddddddddddddddddddddddddd55', h_idx)
    h_idx += h2 + 2
    a3, h3 = sliding_label(window, 'それは無理ですよね馬鹿変態うるさい知らない', h_idx)
    h_idx += h3 + 2
    a4, h4 = sliding_label(window, '义和团起山东不到三月先扒龙王庙再用大炮轰他娘知止而后有静静而后能定定而后能安安而后能虑虑而后能得敢同恶鬼争高下不向霸王让寸分', h_idx)
    a1.start()
    a2.start()
    a3.start()
    a4.start()


    # Run the application
    #window.showFullScreen()
    window.showMaximized()
    sys.exit(app.exec_())
