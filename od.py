import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from get_danmuku import danmuku_xml_to_dict, find_ge_idx


class TransparentWindow(QtWidgets.QMainWindow):
    def __init__(self, display_geo=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if display_geo is None:
            display_geo = {}
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.display_geo = display_geo

    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0)
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))
        painter.drawRect(self.rect())


class DanmukuLabel(QtWidgets.QLabel):
    def __init__(self, desc_dict, *__args):
        super().__init__(*__args)
        # {'stime': 1.418, 'font_size': 25, 'font_color': '0xa0ee00', 'text': '来窒息了'}
        f = self.font()
        self.show_time = desc_dict['stime']
        text = desc_dict["text"]
        font_size = desc_dict["font_size"]
        font_color = desc_dict["font_color"]
        self.setText("%s   " % text)  # do setText twice, first is to get real width with 3 more spaces.
        f.setPointSize(font_size)
        self.setFont(f)
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(30)
        effect.setColor(QColor("#000000"))
        effect.setOffset(0, 0)
        self.setGraphicsEffect(effect)
        self.danmuku_width = self.fontMetrics().boundingRect(self.text()).width()
        self.danmuku_height = self.fontMetrics().boundingRect(self.text()).height()
        self.setText("<font color='%s'>%s</font>" % (font_color, text))  # second time we set color here.
        self.animation = QtCore.QPropertyAnimation(self, "geometry".encode())

    def setup_animation(self, desc_dict):
        duration = desc_dict['duration']
        w_idx_0 = desc_dict['0']['w_idx']
        h_idx_0 = desc_dict['0']['h_idx']
        w_idx_1 = desc_dict['1']['w_idx']
        h_idx_1 = desc_dict['1']['h_idx']
        self.animation.setDuration(duration)
        self.animation.setKeyValueAt(0, QtCore.QRect(w_idx_0, h_idx_0, self.danmuku_width, self.danmuku_height))
        self.animation.setKeyValueAt(1, QtCore.QRect(w_idx_1, h_idx_1, self.danmuku_width, self.danmuku_height))

    def start_animation(self):
        self.animation.start()


class DanmukuManager:
    def __init__(self, xml_path, parent, display_geo=None):
        if display_geo is None:
            display_geo = {}
        self.gui_parent = parent
        self.display_geo = display_geo
        self.danmuku_list = danmuku_xml_to_dict(xml_path)  ########
        self.danmuku_obj_list = []  #########
        self.current_time = 0  #########
        self.start_time = time.time()
        self.current_idx = 0  #########
        self.timer_interval = 100
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.timer_interval)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_danmuku)
        self.route_height = 30
        self.route_offset = 5
        self.danmuku_routes = [0] * int(self.display_geo['height'] / self.route_height - 1)
        self.speed = 0.23272727272727273
        self.duration = display_geo['width'] / self.speed



    def register_danmuku_route(self, danmuku_qlabel, route_idx):
        occupy_until = self.current_time + danmuku_qlabel.danmuku_width * self.duration / (
                danmuku_qlabel.danmuku_width + self.display_geo['width'])
        self.danmuku_routes[route_idx] = occupy_until
        return self.route_height * route_idx + self.route_offset

    def get_danmuku_route(self):
        for idx in range(len(self.danmuku_routes)):
            if self.current_time >= self.danmuku_routes[idx]:
                return idx
        return 0

    def update_danmuku(self):
        self.current_time = (time.time() - self.start_time) * 1000
        if self.current_idx >= len(self.danmuku_list):
            if len(self.danmuku_obj_list) == 0:
                self.stop()
        else:
            while self.current_time / 1000 > self.danmuku_list[self.current_idx]['stime']:
                print('add', self.current_time / 1000, self.danmuku_list[self.current_idx]['stime'],
                      self.danmuku_list[self.current_idx]['text'])
                danmuku_label = DanmukuLabel(self.danmuku_list[self.current_idx], self.gui_parent)
                danmuku_label.show()

                route_idx = self.get_danmuku_route()
                route_h_idx = self.register_danmuku_route(danmuku_label, route_idx)

                danmuku_label.setup_animation(
                    {'duration': self.duration, '0': {'w_idx': self.display_geo['width'], 'h_idx': route_h_idx},
                     '1': {'w_idx': 0 - danmuku_label.danmuku_width, 'h_idx': route_h_idx}})
                danmuku_label.start_animation()
                self.danmuku_obj_list.append(danmuku_label)
                self.current_idx += 1
                if self.current_idx >= len(self.danmuku_list):
                    break
        while len(self.danmuku_obj_list):
            try:
                item_show_time = self.danmuku_obj_list[0].show_time
                if self.current_time / 1000 > item_show_time + self.duration / 1000:
                    useless_danmuku_label = self.danmuku_obj_list.pop(0)
                    print('del', self.current_time / 1000, useless_danmuku_label.show_time)
                    useless_danmuku_label.deleteLater()
                else:
                    break
            except:
                break

    def seek(self, to):
        self.current_time = to
        self.current_idx = find_ge_idx(self.danmuku_list, self.current_time)
        self.start_time = time.time() - to

    def play(self):
        self.timer.start()

    def pause(self):
        self.timer.stop()

    def stop(self):
        print("STOP")
        self.timer.stop()
        self.current_time = 0
        self.current_idx = 0

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    geo = QtWidgets.QApplication.desktop().screenGeometry()
    height = geo.height()
    width = geo.width()
    window = TransparentWindow(display_geo={'width': width, 'height': height})

    a = DanmukuManager(sys.argv[1], window,
                       window.display_geo)
    if len(sys.argv) > 2:
        a.seek(int(sys.argv[2]))
    a.play()

    # ctrl
    quit_button = QtWidgets.QPushButton(window)
    quit_button.setText("Quit")
    quit_button.clicked.connect(app.quit)

    pos = QtWidgets.QDesktopWidget().availableGeometry().bottomRight()
    pos.setX(pos.x() - quit_button.frameSize().width())
    pos.setY(pos.y() - quit_button.frameSize().height())
    quit_button.move(pos)
    # Run the application
    window.showFullScreen()
    print(window.frameSize())
    # window.showMaximized()
    sys.exit(app.exec_())
