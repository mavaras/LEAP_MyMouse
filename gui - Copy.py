# ===============GUI CLASSES===============
# == Canvas
# == MainWindow
# == leap_controller frames

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PCRecognizer import *
from gui_qtdesigner import *
from gvariables import *
import cv2
import time
import sys
import os
import leap_controller
import gvariables
from gvariables import *

listener = gvariables.listener
points = []


# CANVAS CLASS
class Widget_canvas(QWidget):
    lp = Point(0, 0, -1)
    np = Point(0, 0, -1)
    path_points_0 = QPainterPath()
    path_points_1 = QPainterPath()
    path_points_2 = QPainterPath()
    path_points_3 = QPainterPath()
    path_points_4 = QPainterPath()
    canvas = None
    pen_color = Qt.black

    def __init__(self, parent):
        super(Widget_canvas, self).__init__(parent)

    def clear(self):
        aux = QPainterPath()
        self.path_points_0 = aux
        aux = QPainterPath()
        self.path_points_1 = aux
        aux = QPainterPath()
        self.path_points_2 = aux
        aux = QPainterPath()
        self.path_points_3 = aux
        aux = QPainterPath()
        self.path_points_4 = aux
        aux = QPainterPath()
        self.update()

    def paintEvent(self, event):
        canvas = QtGui.QPainter(self)
        pen = QPen()

        # drawing grid
        pen.setWidth(1.4)
        pen.setColor(Qt.black)
        canvas.setPen(pen)
        interval = 20
        for c in range(interval, canvas_width, interval):
            for j in range(interval, canvas_height, interval):
                canvas.drawLine(c, 0, c, canvas_height)
                canvas.drawLine(0, j, canvas_width, j)

        # finger 0 path
        pen.setWidth(2.4)
        pen.setColor(Qt.red)
        canvas.setPen(pen)
        canvas.drawPath(self.path_points_0)

        # finger 1 path
        pen.setColor(Qt.black)
        canvas.setPen(pen)
        canvas.drawPath(self.path_points_1)

        # finger 2 path
        pen.setColor(Qt.blue)
        canvas.setPen(pen)
        canvas.drawPath(self.path_points_2)

        # finger 3 path
        pen.setColor(Qt.green)
        canvas.setPen(pen)
        canvas.drawPath(self.path_points_3)

        # finger 4 path
        pen.setColor(Qt.yellow)
        canvas.setPen(pen)
        canvas.drawPath(self.path_points_4)

    def mousePressEvent(self, event):
        print("click")
        x = event.x()
        y = event.y()
        print("start point: (" + str(x) + "," + str(y) + ")")
        # self.path.moveTo(e.pos())
        self.path_points_1.addEllipse(QtCore.QRectF(x, y, 16, 16))
        global stroke_id, points
        stroke_id += 1
        points.append(Point(x, y, stroke_id))
        self.lp.x, self.lp.y = x, y

    def mouseMoveEvent(self, event):
        # self.path.lineTo(event.pos())
        x = event.x()
        y = event.y()
        self.np = Point(x, y, -1)
        if distance(self.lp, self.np) > 5:
            self.path_points_1.addEllipse(QtCore.QRectF(x, y, 8, 8))
            global stroke_id, points
            points.append(Point(x, y, stroke_id))
            self.lp.x, self.lp.y = x, y
            self.update()

    def mouseReleaseEvent(self, event):
        print("release")
        print("end point: (" + str(event.x()) + "," + str(event.y()) + ")")


# CV FRAME CLASS (Configuration Tab)
class Cv_Frame:
    main_window = None

    def __init__(self, main_window):
        # global cv_frame_XY, cv_frame_XZ, main_window

        self.main_window = main_window
        # show_frame each second
        self.timer = QtCore.QTimer(main_window)
        self.timer.timeout.connect(self.show_frame)
        self.timer.start(1)

    # load frame (image) into label
    def show_frame(self):
        frame_XY = leap_controller.cv_frame_XY
        frame_XZ = leap_controller.cv_frame_XZ
        frame_XY = cv2.resize(frame_XY, None, fx=.7, fy=.7, interpolation=cv2.INTER_CUBIC)
        frame_XZ = cv2.resize(frame_XZ, None, fx=.7, fy=.7, interpolation=cv2.INTER_CUBIC)

        height1, width1, size1 = frame_XY.shape
        height2, width2, size2 = frame_XZ.shape
        step1 = frame_XY.size / height2
        step2 = frame_XZ.size / height2
        qformat1 = QImage.Format_RGBA8888 if size1 == 4 else QImage.Format_RGB888
        qformat2 = QImage.Format_RGBA8888 if size2 == 4 else QImage.Format_RGB888
        frame_XY = QImage(frame_XY, width1, height1, step1, qformat1)
        frame_XZ = QImage(frame_XZ, width2, height2, step2, qformat2)

        self.main_window.label_frame_XY.setPixmap(QtGui.QPixmap.fromImage(frame_XY))
        self.main_window.label_frame_XY.setContentsMargins(0, 0, 0, 0)
        self.main_window.label_frame_XZ.setPixmap(QtGui.QPixmap.fromImage(frame_XZ))
        self.main_window.label_frame_XZ.setContentsMargins(0, 0, 0, 0)


# MAIN WINDOW CLASS
class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    # last and new points for propper drawing
    lp = Point(0, 0, -1)
    np = Point(0, 0, -1)
    n_of_fingers = 1

    # this array stores all combo_boxes with its options with its associated gesture
    cb_action_gesture = {}

    # flag
    opened = False

    def __init__(self, *args, **kwargs):
        QtGui.QMainWindow.__init__(self, *args, **kwargs)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowOpacity(0)
        self.opened = True

        self.systray = QSystemTrayIcon(QIcon("res/icon.ico"), self)
        self.set_notification_area()

        self.setupUi(self)

    # making app icon appear into notification area
    def set_notification_area(self):
        self.systray.show()
        self.systray.showMessage("PCRecognizer",
                                 "App working",
                                 QSystemTrayIcon.Warning)
        # right click options
        self.systray_menu = QMenu(self)
        self.hide_systray = self.systray_menu.addAction("Opt. 1")
        self.systray.setContextMenu(self.systray_menu)

    # specific widget initialization and positioning
    def initUI(self):
        print("initUI")
        # canvas setup
        self.widget_canvas = Widget_canvas(self.tab_canvas)  # linking widget_canvas to tab1
        self.widget_canvas.move(20, 20)
        self.widget_canvas.resize(canvas_width, canvas_height)

        # configuration tab
        self.button_save_conf.clicked.connect(self.save_conf)

        # text edits setup
        self.button_load_text.clicked.connect(self.load_text_B)
        self.text_edit.setReadOnly(True)
        self.text_edit_2.setReadOnly(True)
        self.combo_box.currentIndexChanged["int"].connect(self.combo_box_nfingers_selection_changed)

        # label_leap_status default value
        self.change_leap_status(False)

        # Tab2 cv_frame representation
        self.cvF = Cv_Frame(self)

        # TAB2 - CONFIGURATION TAB
        # action-gesture comboboxes
        connect_func = lambda: self.combo_box_actiongesture_changed(self.combo_box_mm)
        self.combo_box_mm.currentIndexChanged["int"].connect(connect_func)

        self.combo_box_click.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed(self.combo_box_click))
        self.cb_action_gesture[self.combo_box_click] = {0: "click_plane", 1: "click_deep"}
        self.combo_box_rclick.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed(self.combo_box_rclick))
        self.cb_action_gesture[self.combo_box_rclick] = {0: "rclick_plane", 1: "rclick_deep"}
        self.combo_box_minimizew.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed(self.combo_box_minimizew))
        self.cb_action_gesture[self.combo_box_minimizew] = {0: "minimize_1", 1: "minimize_2"}
        self.combo_box_closew.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed(self.combo_box_closew))
        self.cb_action_gesture[self.combo_box_closew] = {0: "closew_1", 1: "closew_2"}

        # help buttons
        self.set_gesture_gif("res/gifs/no_gesture.gif")
        self.label_gesture_gif.setLayout(QtGui.QHBoxLayout())

        help_img = "res/eye.png"
        # we pass view_gesture() method the help button associated combo box
        self.button_help_click.clicked.connect(lambda: self.view_gesture(self.combo_box_click))
        self.button_help_click.setIcon(QIcon(help_img))
        self.button_help_click.setIconSize(QSize(24, 24))
        self.button_help_click.setMask(QtGui.QRegion(self.button_help_click.rect(),
                                                     QtGui.QRegion.Ellipse))
        self.button_help_rclick.clicked.connect(lambda: self.view_gesture(self.combo_box_rclick))
        self.button_help_rclick.setIcon(QIcon(help_img))
        self.button_help_rclick.setIconSize(QSize(24, 24))
        self.button_help_rclick.setMask(QtGui.QRegion(self.button_help_rclick.rect(),
                                                      QtGui.QRegion.Ellipse))

        # TAB3
        """self.combo_box_gestures.currentIndexChanged["int"].connect(self.combo_box_gestures_selection_changed)
        self.set_gesture_gif("gifs/click_plane.gif")
        self.label_gesture_gif.setLayout(QtGui.QHBoxLayout())"""

        # MENUBAR
        self.menubar_file_loadconf.triggered.connect(self.load_conf)
        self.menubar_file_saveconf.triggered.connect(self.save_conf)

    # this two functions are about loading text from text_edit and converting it to points array
    def to_point(self, text):
        parts = text.split(",")
        return int(float(parts[0][1:])), int(float(parts[1][:-1]))

    def load_text_B(self):
        text = str(self.text_edit.toPlainText())
        arr = text.split("\n")

        loaded_points = []  # containing new read points
        for c in range(2, len(arr) - 1):
            x, y = self.to_point(arr[c])
            loaded_points.append(Point(x, y, -1))

        pc = Point_cloud("loaded_points", loaded_points);
        self.widget_canvas.path = QPainterPath()  # clear canvas
        self.update()
        pc.draw_on_canvas()  # drawing loaded stroke
        global points
        points = loaded_points  # allowing "F"

    # save configuration to file
    def save_conf(self):
        print("save_conf()")
        fname = QFileDialog.getSaveFileName(self, "Save Configuration", "c:\\", "(*.txt)")
        if fname:
            f = open(fname, "w+")

            configuration = gvariables.configuration
            configuration.file_name = str(QFileInfo(fname).fileName())
            configuration.file_path = str(QFileInfo(fname).path())
            configuration.file_date = time.ctime(os.path.getctime(fname))

            f.write(configuration.file_name + "\n" + configuration.file_path + "\n" + configuration.file_date + "\n\n")
            f.write(configuration.basic.get_conf())
            f.write("\n")
            f.write(configuration.extra.get_conf())
            f.close()

    # load configuration to app
    def load_conf(self):
        print("load_conf()")
        fname = QFileDialog.getOpenFileName(self, "Save Configuration", "c:\\", "(*.txt)")
        if fname:
            f = open(fname, "r")
            configuration.load_conf(f)
            f.close()

    # Leap status label
    def change_leap_status(self, conn):
        if conn:
            self.label_leap_status.setText("CONNECTED")
            self.label_leap_status.setStyleSheet("QLabel {color: green;}")
        else:
            self.label_leap_status.setText("DISCONNECTED")
            self.label_leap_status.setStyleSheet("QLabel {color: red;}")

    # collection of key events binded to GUI
    def keyPressEvent(self, event):
        global points
        if event.key() == QtCore.Qt.Key_Q:
            self.exit_app()

        elif event.key() == QtCore.Qt.Key_W:  # app interraction example/test
            handle = win32gui.FindWindow(None, r"Reproductor multimedia VLC")
            # win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)
            win32gui.CloseWindow(handle)

        elif event.key() == QtCore.Qt.Key_S:
            gvariables.listener.mouse.active = True if not gvariables.listener.mouse.active else False

        elif event.key() == QtCore.Qt.Key_Y:
            print("Y pressed")
            keyboard = Controller()
            keyboard.press(Key.cmd)
            keyboard.press("d")
            keyboard.release("d")
            keyboard.release(Key.cmd)

        elif event.key() == QtCore.Qt.Key_F:  # start stroke recognition
            if self.n_of_fingers == 1:
                pc = Point_cloud("f3", points, Point(W / 4, H / 4 + 50, -1))
                # pc.draw_on_canvas()    normalized pc
                result = recognize_stroke(points)
                gesture_match(result.name)

                str_accum = "Last/Current gesture points array\n\n"
                for c in range(0, len(points)):
                    str_accum += "(" + str(points[c].x) + "," + str(points[c].y) + ")"
                    if c != len(points) - 1:
                        str_accum += "\n"

                print_score(result)
                self.text_edit.setText(str_accum)

            elif self.n_of_fingers == -1:
                results = []
                for c in range(0, 5):
                    results.append(recognize_stroke(gvariables.listener.gesture[c]))
                    gesture_match(results[len(results) - 1].name)

                results_names = []
                results_names = [res.name for res in results]
                print(results_names)
                if len(set(results_names)) <= 1:
                    print_score(results[1])
                else:
                    print("inconsistent matches of each finger")

            # reseting values, clearing arrays
            gvariables.stroke_id = 0
            points = []
            gvariables.listener.clear_variables()

        elif event.key() == QtCore.Qt.Key_C:  # clear canvas
            print("clear")
            self.widget_canvas.clear()
            self.label_score.setText("")

        elif event.key() == QtCore.Qt.Key_G and sys.argv[1] != "-thread":
            # global points
            if self.n_of_fingers == 1:  # recordin only 1 finger(indice)
                print("1 finger recording mode")
                if gvariables.listener.capture_frame:  # 2nd "G" press
                    print("record captured")
                    gvariables.listener.capture_frame = False
                    pc = Point_cloud("f1", gvariables.listener.gesture[1]).draw_on_canvas()

                    # getting finger_1 points
                    points = gvariables.listener.gesture[1]  # this allows "F" to work with mouse and hand stroke
                    gvariables.listener.c = 0

                else:  # 1st "G" press
                    print("recording")
                    self.label_count.setText("4")  # countdown after getting gesture
                    # this is like a thread with no wait
                    QtCore.QTimer.singleShot(1000, lambda: self.updateLabel(self.label_count))

            elif self.n_of_fingers == -1:  # recording ALL fingers
                print("all fingers recording mode")
                aux = -100
                if gvariables.listener.capture_frame:
                    print("record captured")
                    gvariables.listener.capture_frame = False
                    for c in range(0, 5):
                        pc = Point_cloud("f" + str(c), gvariables.listener.gesture[c], Point(W / 4 + aux, H / 4, -1))
                        pc.draw_on_canvas()
                        aux += 50

                    points = gvariables.listener.gesture[1]  # just for testing

                else:  # 1st "G" press
                    print("recording")
                    self.label_count.setText("4")  # countdown after getting gesture
                    # this is like a thread with no wait
                    QtCore.QTimer.singleShot(1000, lambda: self.updateLabel(self.label_count))

    def combo_box_nfingers_selection_changed(self):
        print("selection changed" + str(self.combo_box.currentIndex()))
        if self.combo_box.currentIndex() == 0:
            self.n_of_fingers = 1
        elif self.combo_box.currentIndex() == 1:
            self.n_of_fingers = -1

        self.setFocus()  # getting focus back on main_window

    # handling all Configuration tab combo_box changes
    def combo_box_actiongesture_changed(self, combo_box_name):
        print("action-gesture changed" + str(combo_box_name.currentIndex()))
        if combo_box_name == "combo_box_lclick":
            if combo_box_name.currentIndex() == 0:
                configuration.lclick = "click_planem"
            elif combo_box_name.currentIndex() == 1:
                configuration.lclick = "click_deepm"

        elif combo_box_name == "combo_box_rclick":
            pass
        elif combo_box_name == "combo_box_mm":
            configuration.basic.mm = combo_box_name.currentIndex()
            pass
        elif combo_box_name == "combo_box_minimizew":
            pass
        elif combo_box_name == "combo_box_closew":
            pass
        elif combo_box_name == "combo_box_changew":
            pass
        elif combo_box_name == "combo_box_vscroll":
            pass
        elif combo_box_name == "combo_box_hscroll":
            pass
        elif combo_box_name == "combo_box_grabb":
            pass

        self.setFocus()

    def combo_box_gestures_selection_changed(self):
        print("selection changed" + str(self.combo_box_gestures.currentIndex()))
        if self.combo_box_gestures.currentIndex() == 0:
            self.set_gesture_gif("res/gifs/click_plane.gif")
        elif self.combo_box_gestures.currentIndex() == 1:
            self.set_gesture_gif("res/gifs/grabb_plane.gif")
        elif self.combo_box_gestures.currentIndex() == 2:
            self.set_gesture_gif("res/gifs/scroll.gif")

        self.setFocus()

    def view_gesture(self, combo_box):
        print("view gesture: " + str(combo_box.currentIndex()))
        print(self.cb_action_gesture.get(combo_box).get(combo_box.currentIndex()))

        self.set_gesture_gif(
            "res/gifs/" + str(self.cb_action_gesture.get(combo_box).get(combo_box.currentIndex())) + ".gif")
        self.label_gesture_gif.setLayout(QtGui.QHBoxLayout())

    # Leap status label CONNECTED or DISCONNECTED
    def set_label_leap_status(self, img):
        img, _, _ = load_image(img)
        self.label_leap_status.setPixmap(QPixmap.fromImage(img))

    # Gestures tab gif of each predefined gesture
    def set_gesture_gif(self, gif):
        try:
            giff = QtGui.QMovie(gif)
            self.label_gesture_gif.setMovie(giff)
            giff.start()

        except:
            print("provided gif doesnt exist")

    # countdown label
    def updateLabel(self, label):
        # change the following line to retrieve the new voltage from the device
        t = int(label.text()) - 1
        if t == 0:
            label.setText("")
            while (gvariables.listener.hand_vel < 300 or gvariables.listener.fingers_vel[4] < 100):
                pass

            gvariables.listener.capture_frame = True
            return

        label.setText(str(t))
        QtCore.QTimer.singleShot(1000, lambda: self.updateLabel(label))

    # exits applications, closes all windows
    def exit_app(self):
        print("exiting...")
        self.close()
        sys.exit()
        self.opened = False

# various functions


# this function recognize one SINGLE stroke (if ALL fingers, one by one)
def recognize_stroke(points):
    print("recognizing stroke")
    aux = []
    aux.append(points)
    result = PCRecognizer().recognize(aux)

    return result


# this shows final score of current stroke (red label on canvas)
def print_score(result):
    score = "Result: matched with " + result.name + " about " + str(round(result.score, 2))
    gvariables.main_window.label_score.setStyleSheet("color: red")
    gvariables.main_window.label_score.setText(str(score))
    gvariables.main_window.text_edit_2.append("\n" + str(score))


# handling gesture stroke match actions
def gesture_match(gesture_name):
    if gesture_name == "T":
        print("T gesture")
        if sys.argv[1] == "-thread":
            # handle = win32gui.FindWindow(None, r"Reproductor multimedia VLC")
            """hwnd = get_current_window_hwnd()
            minimize_window(hwnd)"""

    elif gesture_name == "V":
        print("V gesture")
    elif gesture_name == "LEFT":
        print("LEFT gesture")
    elif gesture_name == "RIGHT":
        print("RIGHT gesture")
    print("")


"""
def start_gui(main_window):
	main_window = main_window


main_windoww = MainWindow()

main_windoww.initUI()
main_windoww.show()"""
