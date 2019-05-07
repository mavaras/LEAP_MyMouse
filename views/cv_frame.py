# -*- coding: utf-8 -*-

# ===============CV_FRAME CLASS===============
# == Real time frame display
# == leap_controller fingers


import time
import numpy as np
from gvariables import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from views.gui_qtdesigner import *
import cv2


class Cv_Frame:
    main_window = None

    def __init__(self, main_window):
        # global cv_frame_XY, cv_frame_XZ, main_window

        self.main_window = main_window
        self.frame_XY = np.zeros((540, 640, 3), np.uint8)  # XZ frame
        self.frame_XZ = np.zeros((540, 640, 3), np.uint8)  # XZ frame

        # show_frame each second
        time.sleep(1)
        self.timer = QtCore.QTimer(main_window)
        self.timer.timeout.connect(self.show_frame)
        self.timer.start(1)

    # load frame (image) into label
    def show_frame(self):
        # self.frame_XY = gvariables.listener.cv_frame_XY
        # self.frame_XZ = gvariables.listener.cv_frame_XZ
        aux_frame_XY = cv2.resize(np.array(self.frame_XY), None,
                                  fx=.7, fy=.7, interpolation=cv2.INTER_CUBIC)
        aux_frame_XZ = cv2.resize(np.array(self.frame_XZ), None,
                                  fx=.7, fy=.7, interpolation=cv2.INTER_CUBIC)

        height1, width1, size1 = aux_frame_XY.shape
        height2, width2, size2 = aux_frame_XZ.shape
        step1 = aux_frame_XY.size/height2
        step2 = aux_frame_XZ.size/height2
        qformat1 = QImage.Format_RGBA8888 if size1 == 4 else QImage.Format_RGB888
        qformat2 = QImage.Format_RGBA8888 if size2 == 4 else QImage.Format_RGB888
        aux_frame_XY = QImage(aux_frame_XY, width1, height1, step1, qformat1)
        aux_frame_XZ = QImage(aux_frame_XZ, width2, height2, step2, qformat2)

        self.main_window.label_frame_XY.setPixmap(QtGui.QPixmap.fromImage(aux_frame_XY))
        self.main_window.label_frame_XY.setContentsMargins(0, 0, 0, 0)
        self.main_window.label_frame_XZ.setPixmap(QtGui.QPixmap.fromImage(aux_frame_XZ))
        self.main_window.label_frame_XZ.setContentsMargins(0, 0, 0, 0)

    @pyqtSlot(np.ndarray)
    def set_frame_XY(self, frameXY):
        self.frame_XY = frameXY

    @pyqtSlot(np.ndarray)
    def set_frame_XZ(self, frameXZ):
        self.frame_XZ = frameXZ
