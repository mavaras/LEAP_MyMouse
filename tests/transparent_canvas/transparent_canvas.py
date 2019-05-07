import sys
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from tcgui import *
import win32api
import Leap
from constants import *
import math
import win32api, win32con, win32gui


# calculates distance between two given points
def distance(x, y, x2, y2):
    dx = x - x2
    dy = y - y2
    return math.sqrt(dx * dx + dy * dy)


class leap_listener(Leap.Listener):
    def on_init(self, controller):
        print("on_init")
        self.flag = False
        self.fingers_pos = [[0, 0, 0] for c in range(5)]

    def on_connect(self, controller):
        print("conected")

    def on_frame(self, controller):
        canvas.clear()
        frame = controller.frame()
        global canvas
        for hand in frame.hands:
            if hand.is_right:
                # scrolling
                """pitch = hand.direction.pitch * Leap.RAD_TO_DEG
                if pitch < -2:
                    print("scroll down")
                    cx, cy = win32api.GetCursorPos()
                    vel = -int(40-((90-abs(pitch))/3))
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, cx, cy, vel, 0)

                elif pitch > 42:
                    print("scroll up")
                    cx, cy = win32api.GetCursorPos()
                    vel = int(30-((90-pitch)/3))
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, cx, cy, vel, 0)"""
                f2 = hand.fingers[1]
                f3 = hand.fingers[2]

                f_pos = f2.tip_position
                if not self.flag:
                    x = f_pos.x
                    y = LEAP_H - f_pos.y
                    z = f_pos.z
                    x = x + LEAP_W / 2
                    x = (W * x) / LEAP_W
                    y = (H * y) / LEAP_H

                z = 20

                if not self.flag and abs(f2.tip_velocity.z) < 200 and distance(self.fingers_pos[1][0],
                                                                               self.fingers_pos[1][1], x, y) > 1:
                    # perform mouse movement
                    canvas.add_to_path(x, y, z)
                    win32api.SetCursorPos((int(x), int(y)))
                    self.fingers_pos[1] = (x, y, f2.tip_position.z)
                else:
                    canvas.add_to_path(self.fingers_pos[1][0], self.fingers_pos[1][1], z)
                """
                #print(f3.tip_velocity.y)
                if abs(f3.tip_velocity.y) > 300 and f3.tip_velocity.y < 0 and abs(f2.tip_velocity.y) < 60:
                    if not self.flag:
                        print("click")
                        self.flag = True
                        cx, cy = win32api.GetCursorPos()
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, cx, cy, 0, 0)
                        time.sleep(.2)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, cx, cy, 0, 0)
                else:
                    if self.flag:
                        self.flag = False"""

                for finger in hand.fingers:

                    start_click_movement = 280
                    end_click_movement = 30

                    # print(abs(finger.tip_velocity.z))
                    # if finger 1 and negative Z movement and icreased Z finger velocity and not inside this
                    if finger.type == 1 and hand.palm_velocity.z < 0 and abs(
                            finger.tip_velocity.z) > start_click_movement and not self.flag:
                        # perform mouse click
                        print("click")
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, int(x), int(y), 0, 0)
                        # time.sleep(.2)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, int(x), int(y), 0, 0)
                        self.flag = True  # this is for not to move cursor when we moving finger to do click

                    # when click movement is near to reach its end
                    elif abs(finger.tip_velocity.z) < end_click_movement:
                        self.flag = False

                canvas.draw_path()


# GUI code begins here
# canvas object
class Widget_canvas(QWidget):
    path = QPainterPath()

    def __init__(self, parent):
        print("canvas init")
        super(Widget_canvas, self).__init__(parent)

    def clear(self):
        aux = QPainterPath()
        self.path = aux

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            global exit
            exit = True
            self.close()
            sys.exit()

    def paintEvent(self, event):
        canvas = QtGui.QPainter(self)
        pen = QPen()

        # drawing grid
        pen.setWidth(1.4)
        pen.setColor(Qt.black)
        canvas.setPen(pen)
        interval = 40
        for c in range(interval, canvas_w, interval):
            for j in range(interval, canvas_h, interval):
                canvas.drawLine(c, 0, c, canvas_h)
                canvas.drawLine(0, j, canvas_w, j)

        pen.setWidth(3.4)
        pen.setColor(Qt.red)
        canvas.setPen(pen)
        canvas.drawPath(self.path)

    def draw_path(self):
        self.update()

    def add_to_path(self, x, y, radius):
        self.path.addEllipse(QtCore.QRectF(x, y, radius, radius))


"""class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self, *args, **kwargs):
		QtGui.QMainWindow.__init__(self, *args, **kwargs)
		self.setWindowFlags(Qt.FramelessWindowHint)
		#self.setWindowOpacity(0)
		
		self.widget_canvas = canvas
		self.setupUi(self)

	# collection of key events binded to GUI
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Q:
			main_window.close()
			sys.exit()
"""
if __name__ == "__main__":
    listener = leap_listener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    # keeping Leap Motion working from background
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    app = QtGui.QApplication([])
    canvas = Widget_canvas(None)
    canvas_h = win32api.GetSystemMetrics(1)
    canvas_w = win32api.GetSystemMetrics(0)
    print("screen resolution: " + str(canvas_w) + " " + str(canvas_h))

    canvas.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    canvas.setAttribute(Qt.WA_TranslucentBackground)
    canvas.showFullScreen()

    app.exec_()

    """main_window = MainWindow()
    main_window.show()"""
