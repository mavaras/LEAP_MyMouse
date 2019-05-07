# -*- coding: utf-8 -*-

# ===============LEAP API CONTROLLER===============
# == Leap interactions
# == frame representation
# == events
# == sends signals to view


# basic modules imports
import time
import numpy as np

# aux modules imports
import cv2
from collections import deque
from pynput.keyboard import Key, Controller
from PyQt4.QtCore import QObject, pyqtSignal

# Leap Motion API
import lib.Leap as Leap

# own package imports
from _print import _print
from aux_functions import *
from win32_functions import *
from key_handle import *
from mouse import Mouse
from gvariables import *
import gvariables

cv_frame_XY = np.zeros((540, 640, 3), np.uint8)
cv_frame_XZ = np.zeros((540, 640, 3), np.uint8)


# CLASS defining a single Point
class Point:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

    def convert_to(self, where_W, where_H):
        """ method to translate parent point to given location

        :param where_W: width
        :param where_H: height
        """
        self.y = where_H - abs(self.y)  # Y invertion (conflict with NN)

        self.x = (W * self.x) / where_W
        self.y = (H * self.y) / where_H


# CLASS LEAP API
class leap_listener(Leap.Listener):
    frame = 0
    capture_frame = False

    # QObject class with those things to send to gui.py through signals
    class LeapStatus(QObject):
        leap_connected = False
        sgn_leap_connected = pyqtSignal(bool)
        sgn_cv_frame_XY = pyqtSignal(np.ndarray)
        sgn_cv_frame_XZ = pyqtSignal(np.ndarray)

        def __init__(self):
            QObject.__init__(self)

        def emit_leap_connected(self, val):
            self.sgn_leap_connected.emit(val)

        def emit_cv_frame_XY(self, frame):
            self.sgn_cv_frame_XY.emit(frame)

        def emit_cv_frame_XZ(self, frame):
            self.sgn_cv_frame_XZ.emit(frame)

    def clear_variables(self):
        """ resets to defaults all relevant leap_listener variables"""
        self.gesture = [[] * 5 for c in range(600)]
        self.c = 0
        self.tail_points = []
        for c in range(0, 5):
            aux = deque([], 18)
            self.tail_points.append(aux)

    def on_init(self, controller):
        """ (Leap API) like __init__ method"""
        self.LEAP_W = 320
        self.LEAP_H = 200

        self.cv_frame_XY = np.zeros((540, 640, 3), np.uint8)  # XY frame
        self.cv_frame_XZ = np.zeros((540, 640, 3), np.uint8)  # XZ frame

        self.frame = controller.frame()
        self.status = self.LeapStatus()
        self.mouse = Mouse(0, 0, 1, 1, 1, 5, False)
        self.capture_frame = False
        self.recording = False

        self.vscrolling = True
        self.hscrolling = False
        self.plane_mode = False
        self.deep_mode = False

        # this all temporary variables, just for testing
        p = []
        lim_points = 600
        self.gesture = [[] * 5 for c in range(lim_points)]
        self.c = 0  # contador gesture points
        self.d01 = 0
        self.on_frame_c = 0  # contador pitch average (not used)
        self.lim_points = 400

        self.hand_vel = 0
        self.fingers_pos = [[0, 0, 0] for c in range(5)]
        self.fingers_vel = [[-1] for c in range(5)]
        self.tail_points = []
        for c in range(5):
            aux = deque([], 18)
            self.tail_points.append(aux)

        print("initialized")

    @property
    def leap_status(self):
        return self.status.leap_connected

    def on_connect(self, controller):
        """ (Leap API) Leap device is connected"""
        print("connected")

        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

        self.status.leap_connected = True
        self.status.emit_leap_connected(True)

        time.sleep(.5)

    # gvariables.main_window.change_leap_status(True)  # label

    def on_focus_lost(self, controller):
        """ (Leap API) we are using Leap Motion from outside MainWindow"""
        print("Unfocused")
        controller.add_listener(gvariables.listener)

    def on_disconnect(self, controller):
        """ (Leap API) Leap device is disconnected"""
        print("disconnected")
        self.status.leap_connected = False
        self.status.emit_leap_connected(False)

    # gvariables.main_window.change_leap_status(False)

    def on_exit(self, controller):
        """ (Leap API) leap_listener is destroyed"""
        print("exited")

    def leap_to_screen(self, leap_x, leap_y):
        """ translates given Leap coordinates to screen ones

        :param leap_x: Leap Motion X coordinate
        :param leap_y: Leap Motion Y coordinate
        """

        x = -self.LEAP_W/2 if int(leap_x) < -self.LEAP_W/2 else leap_x

        # y inversion
        y = self.LEAP_H - leap_y
        y += 80

        x += self.LEAP_W/2
        x = abs(((W * 1.2) * x)/self.LEAP_W)
        y = (H * 1.2 * y)//self.LEAP_H

        return int(x), int(y)

    def stop_control(self):
        """ Stops mouse control"""

        self.mouse.active = False

    def start_control(self):
        """ Enables mouse control"""

        self.mouse.active = True

    def on_frame(self, controller):
        """ (Leap API) main leap_listener method.
        loops through each frame captured by Leap Motion device
        -> opencv representation handling
        -> complex gestures
        -> simple gestures + actions
        """

        self.frame = controller.frame()
        frame = self.frame

        # opencv canvas
        cv_frame_loc_XY = np.zeros((540, 640, 3), np.uint8)  # XY frame
        cv_frame_loc_XZ = np.zeros((540, 640, 3), np.uint8)  # XZ frame

        if len(frame.hands) == 2 or \
                (len(frame.hands) == 1 and (len(frame.fingers.extended()) == 0 or \
                                            len(frame.fingers.extended()) == 1 and frame.fingers.extended()[
                                                0].type == 0)):
            # two hands if frame
            self.can_record = True
            cv2.putText(cv_frame_loc_XY, "Two hands in frame",
                        (190, H/2 - 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.circle(cv_frame_loc_XY, (H/4 + 50, W/6 - 50), 100, [255, 0, 0], 1)
            cv2.putText(cv_frame_loc_XZ, "Two hands in frame",
                        (190, H/2 - 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.circle(cv_frame_loc_XZ, (H/4 + 50, W/6 - 50), 100, [255, 0, 0], 1)
        else:
            self.can_record = False

        for hand in frame.hands:
            if hand.is_right:
                self.hand_vel = max(abs(hand.palm_velocity[0]),
                                    abs(hand.palm_velocity[1]),
                                    abs(hand.palm_velocity[2]))

                cv2.putText(cv_frame_loc_XY, "X to Y representation (vertical plane)",
                            (50, 540 - 70), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(cv_frame_loc_XZ, "X to Z representation (horizontal plane)",
                            (50, 540 - 70), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 255, 255), 1, cv2.LINE_AA)

                # one hand into frame
                if self.mouse.active and not self.recording:

                    """ CURSOR MOVEMENT SECTION"""
                    # TODO:
                    #   -> perform coords translation
                    #   -> add movement velocity ?
                    if not self.mouse.switch_mode:
                        mm_finger = gvariables.configuration.basic.mm
                        fx, fy = hand.fingers[mm_finger].tip_position.x, \
                                 hand.fingers[mm_finger].tip_position.y
                        sx, sy = self.leap_to_screen(fx, fy)

                        self.mouse.xdir = 1 if sx > W / 2 else -1
                        self.mouse.ydir = 1 if abs(sy) < H / 2 else -1

                        win32api.SetCursorPos((
                            # int(abs(self.fingers_pos[mm_finger][0])),   # x
                            # int(abs(self.fingers_pos[mm_finger][1]))    # y
                            sx, sy
                        ))

                        # updating mouse object position
                        self.mouse.x = int(abs(self.fingers_pos[mm_finger][0]))
                        self.mouse.y = int(abs(self.fingers_pos[mm_finger][1]))

                    # INTERACTION modes
                    if self.deep_mode:
                        finger1 = hand.fingers[1]
                        f1_pos = finger1.tip_position
                        """print(f1_pos.z)
                        
                        x, y = self.leap_to_screen(f1_pos.x, f1_pos.y)
                        
                        # mouse movement:
                        self.mouse.xdir = 1 if x > W/2 else -1
                        self.mouse.ydir = 1 if abs(y) < H/2 else -1
                        win32api.SetCursorPos((int(abs(x)+self.mouse.xdir),
                                               int(abs(y))+self.mouse.ydir))
                        self.mouse.x, self.mouse.y = int(abs(x)), int(abs(y))"""

                    elif self.plane_mode:
                        f0 = hand.fingers[0]
                        f1 = hand.fingers[1]
                        f2 = hand.fingers[2]
                        dist_0_1 = distance(Point(f1.tip_position.x, f1.tip_position.z, -1),
                                            Point(f0.tip_position.x, f0.tip_position.z,
                                                  -1))  # this works better on XZ plane
                        dist_1_2 = distance_3d(f1.tip_position.x, f1.tip_position.y, f1.tip_position.z,
                                               f2.tip_position.x, f2.tip_position.y, f2.tip_position.z)

                        roll = abs(hand.palm_normal.roll * Leap.RAD_TO_DEG)
                        yaw = hand.direction.yaw * Leap.RAD_TO_DEG
                        pitch = hand.direction.pitch * Leap.RAD_TO_DEG

                        """ SWITCH WINDOWS SECTION"""
                        # TODO:
                        #   -> utf-8 / latin-2
                        #   -> improve swipe
                        # angle between X and Y (Z rotations)
                        if roll > 50:
                            # we are into switch mode

                            if not self.mouse.switch_mode:
                                print("into of SwitchMode")
                                hold("alt")
                                press("tab")

                                self.mouse.switch_mode = True

                            direction = int(yaw / abs(yaw))
                            if hand.palm_velocity.x > 150 and not self.mouse.switching:
                                self.mouse.switching = True
                                # aux = get_current_window_name()
                                if direction == 1:
                                    print("right SWIPE")
                                    press("right_arrow")
                                    # pressHoldRelease2(["alt", "tab", "right_arrow"], 1)
                                    """if curr_window_index == len(opened_windows_names) - 1:
                                    curr_window_index = 0
                                    name = opened_windows_names[curr_window_index+1]"""
                                else:
                                    print("left SWIPE")
                                    press("left_arrow")
                                    """if curr_window_index == 1:  # always Start it's the first one in list(0) (Windows only?)
                                    curr_window_index = len(opened_windows_names)-1
                                    name = opened_windows_names[curr_window_index-1]"""

                                # bring_window_to_top(win32gui.FindWindow(None, name))
                                time.sleep(.4)
                            else:
                                self.mouse.switching = False

                        else:
                            if self.mouse.switch_mode:
                                print("out of SwitchMode")
                                release("alt")
                                self.mouse.switch_mode = False
                                self.mouse.switching = False

                            # powrpointt
                            f_frontmost = frame.fingers.extended().frontmost.type
                            if len(frame.fingers.extended()) == 5 and "PowerPoint" in get_current_window_name():
                                direction = int(yaw / abs(yaw))
                                if f1.tip_velocity.x > 200 and not self.mouse.switching:
                                    self.mouse.switching = True
                                    if direction == 1:
                                        print("RIGHT swipe")
                                        press("right_arrow")
                                    else:
                                        print("LEFT swipe")
                                        press("left_arrow")

                                else:
                                    if f1.tip_velocity.x < 30:
                                        self.mouse.switching = False

                            if self.vscrolling:
                                """ VSCROLL SECTION"""
                                # TODO:
                                #   -> choose speed
                                #   -> speed increasing with angle
                                if "UD" in gvariables.configuration.basic.vscroll:
                                    n_fingers = [int(c) for c in gvariables.configuration.basic.vscroll
                                                 if c.isdigit()][0]
                                    if len(frame.fingers.extended()) == n_fingers:
                                        # angle between Z and Y (X rotations)
                                        pitch = hand.direction.pitch * Leap.RAD_TO_DEG
                                        if pitch < -13:
                                            print("vscroll down")
                                            vel = -int(40 - ((90 - abs(pitch)) / 3) + 17)
                                            self.mouse.vscroll(vel)

                                        elif pitch > 47:
                                            print("vscroll up")
                                            vel = int(30 - ((90 - pitch) / 3) + 17)
                                            self.mouse.vscroll(vel)

                                else:
                                    n_fingers = [int(c) for c in gvariables.configuration.basic.vscroll
                                                 if c.isdigit()][0]
                                    print(yaw)
                                    if len(frame.fingers.extended()) == n_fingers:
                                        if yaw < -30:
                                            vel = -int(40 - ((90 - abs(pitch)) / 3) + 17)
                                            self.mouse.vscroll(vel)

                                        elif yaw > 9:
                                            vel = int(30 - ((90 - pitch) / 3) + 17)
                                            self.mouse.vscroll(vel)

                                # horizontal scroll ??
                                # angle between Z and X (Y rotations)
                                roll = hand.direction.roll * Leap.RAD_TO_DEG
                                keyboard = Controller()
                                if roll < -50:
                                    """print("hscroll down")
                                    keyboard.press(Key.ctrl)
                                    keyboard.press("s")"""

                                elif roll > 50:
                                    """print("hscroll up")
                                    cx, cy = win32api.GetCursorPos()
                                    vel = int(30-((90-pitch)/3))
                                    win32api.mouse_event(win32con.EVENTF_WHEEL, cx, cy, vel, 0)"""

                            """ GRAB SECTION"""
                            # TODO:
                            #   -> add
                            #       -> f2 down
                            #       -> f2 and f3 down
                            #       -> 45 degrees yaw
                            #   -> same as planem click?
                            if dist_1_2 < 5.8:
                                if not self.mouse.left_clicked and not self.mouse.left_pressed:
                                    print("grabbed")
                                    self.mouse.grabbing = True
                                    cx, cy = win32api.GetCursorPos()
                                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,
                                                         cx, cy, 0, 0)
                                    self.mouse.left_pressed = True
                            else:
                                if self.mouse.left_pressed:
                                    print("ungrabbed")
                                    self.mouse.grabbing = False
                                    cx, cy = win32api.GetCursorPos()
                                    # time.sleep(.2)
                                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,
                                                         cx, cy, 0, 0)
                                    self.mouse.left_pressed = False

                            """ LEFT CLICK SECTION"""
                            # TODO:
                            #   -> add
                            if not self.mouse.switching:
                                # lclick plane_mode
                                # for keep performance when hand pitch (X rotations) >>
                                if gvariables.configuration.basic.lclick == "click_planem":

                                    lim = 80 - 15 * abs(pitch) // 35
                                    lim -= 2 if self.mouse.ydir == -1 else 0
                                    # print(str(dist_0_1) + " " + str(lim))
                                    if dist_0_1 < lim:
                                        if not self.mouse.left_clicked and \
                                           not self.mouse.left_pressed and \
                                           not self.mouse.grabbing:
                                            print("click")
                                            self.mouse.left_clicked = True
                                            self.mouse.lclick()
                                    else:
                                        if self.mouse.left_clicked:
                                            self.mouse.left_clicked = False

                                # lclick deep_mode
                                elif gvariables.configuration.basic.lclick == "click_deepm":
                                    if abs(f1.tip_velocity.y) > 300 and \
                                        f1.tip_velocity.y < 0 and \
                                        abs(f1.tip_velocity.y) < 60:
                                        if not self.mouse.left_clicked:
                                            print("click")
                                            self.mouse.left_clicked = True
                                            self.mouse.lclick()
                                    else:
                                        if self.mouse.left_clicked:
                                            self.mouse.left_clicked = False

                                # lclick f1_down
                                elif gvariables.configuration.basic.lclick == "click_f2down":
                                    if f2.tip_velocity.y < -90 and \
                                       abs(f0.tip_velocity.y) < 30:
                                        if not self.mouse.left_clicked:
                                            print("click")
                                            self.mouse.left_clicked = True
                                            self.mouse.lclick()
                                    else:
                                        if self.mouse.left_clicked:
                                            self.mouse.left_clicked = False

                                elif gvariables.configuration.basic.lclick == "click_f1down":
                                    if abs(f1.tip_velocity.y) > 300 and \
                                       f1.tip_velocity.y < 0 and \
                                       abs(f0.tip_velocity.y) < 60:
                                        if not self.mouse.left_clicked:
                                            print("click")
                                            self.mouse.left_clicked = True
                                            self.mouse.lclick()
                                    else:
                                        if self.mouse.left_clicked:
                                            self.mouse.left_clicked = False

                                """ RIGHT CLICK SECTION"""
                                # TODO:
                                #   -> add
                                if gvariables.configuration.basic.rclick == "rclick_f2down":
                                    if f2.tip_velocity.y < -90 and \
                                       abs(f1.tip_velocity.y) < 30 and \
                                       not self.mouse.right_clicked and \
                                       not self.mouse.left_clicked:
                                        print("rclick")
                                        self.mouse.right_clicked = True
                                        self.mouse.rclick()
                                    else:
                                        if self.mouse.right_clicked:
                                            self.mouse.right_clicked = False

                                elif gvariables.configuration.basic.rclick == "rclick_f1down":
                                    if f1.tip_velocity.y < -90 and \
                                       abs(f2.tip_velocity.y) < 30 and \
                                       not self.mouse.right_clicked and \
                                       not self.mouse.left_clicked:
                                        print("rclick")
                                        self.mouse.right_clicked = True
                                        self.mouse.rclick()
                                    else:
                                        if self.mouse.right_clicked:
                                            self.mouse.right_clicked = False

                for finger in hand.fingers:
                    self.fingers_vel[finger.type] = max(abs(finger.tip_velocity.x), abs(finger.tip_velocity.y),
                                                        abs(finger.tip_velocity.z))
                    fx, fy, fz = finger.tip_position.x, finger.tip_position.y, finger.tip_position.z
                    sx, sy = self.leap_to_screen(fx, fy)

                    if distance(Point(sx, sy, -1), Point(self.fingers_pos[finger.type][0],
                                                         self.fingers_pos[finger.type][1], -1)) > 3:
                        self.fingers_pos[finger.type] = (sx, sy, fz)

                    """ OPENCV DRAWING SECTION"""
                    # TODO:
                    #   -> different appearances
                    cv2.circle(cv_frame_loc_XY, (int(fx) + 250, int(H/2 - abs(fy))), 11, [255, 255, 255], 1)
                    if finger.type != 0:
                        cv2.line(cv_frame_loc_XY,
                                 (int(fx) + 250, int(H/2 - abs(fy))),
                                 (int(hand.fingers[finger.type - 1].tip_position.x) + 250,
                                  int(H/2 - abs(hand.fingers[finger.type - 1].tip_position.y))),
                                 (255, 255, 255), 1)
                        cv2.line(cv_frame_loc_XZ,
                                 (int(fx) + 250, int(sign(fz) * fz) + 220),
                                 (int(hand.fingers[finger.type - 1].tip_position.x) + 250,
                                  int(220 + abs(hand.fingers[finger.type - 1].tip_position.z))),
                                 (255, 255, 255), 1)

                    self.tail_points[finger.type].append(
                        (int(fx) + 250, int(H/2 - abs(fy)),
                         220 + sign(fz) * int(abs(fz)))
                    )

                    for point in self.tail_points[finger.type]:
                        cv2.circle(cv_frame_loc_XY, (int(point[0]), int(point[1])), 6, [205, 205, 205], 1)
                        cv2.circle(cv_frame_loc_XZ, (int(point[0]), int(point[2])), 6, [205, 205, 205], 1)

                    if len(self.tail_points) == 10:
                        self.tail_points[finger.type].popleft()

                    """ GESTURE RECORDING SECTION"""
                    if self.capture_frame:
                        # print(str(finger.type)+" "+str(finger.tip_position))
                        if finger.type == 1: print(str(fx) + " " + str(fy))
                        self.gesture[finger.type].append(Point(fx, fy, -1))
                        self.gesture[finger.type][len(self.gesture[finger.type]) - 1].convert_to(W / 2, H / 2)
                    # self.c += 1

                    if len(
                            frame.hands) == 1 and finger.type == gvariables.configuration.basic.mm and self.mouse.active and not self.mouse.switch_mode:
                        pass

                    self.on_frame_c += 1

        # global cv_frame_XY, cv_frame_XZ
        self.cv_frame_XY = cv_frame_loc_XY
        self.cv_frame_XZ = cv_frame_loc_XZ
        self.status.emit_cv_frame_XY(self.cv_frame_XY)
        self.status.emit_cv_frame_XZ(self.cv_frame_XZ)
