# -*- coding: utf-8 -*-

# ===============SETTINGS===============
# == vscroll pitch angle and speed
# == mouse movement speed and invertion
# == startup folder


from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QComboBox, QDialog, QButtonGroup, QPushButton, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton
)
from views.gui_qtdesigner import *


class Settings(QDialog):
    """ this class represents the general settings window"""

    def __init__(self, parent):
        super(Settings, self).__init__(parent)
        self.parent = parent

        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon("res/icons/leapmymouse.png"))

        self.resize(500, 150)
        self.setFixedSize(self.size())

        layout = QGridLayout()
        self.label_1 = QLabel()
        self.label_1.setText("label1")

        hbox = QHBoxLayout()
        self.label_2 = QLabel()
        self.label_2.setText("Startup folder")
        self.startup_textarea = QLineEdit()
        self.startup_textarea.setText(parent.configuration.startup_path)
        self.startup_textarea.setFocus(False)
        self.button_startup_folder = QPushButton()
        self.button_startup_folder.setText("Set")
        self.button_startup_folder.setStyleSheet(
            """
            image: none;
            color: black;
            padding-top: 0px;
            padding-bottom: 0px;
            padding-left: 7px;
            padding-right: 7px;
            """
        )
        self.button_startup_folder.clicked.connect(self.set_startup_folder)
        hbox.addWidget(self.label_2)
        hbox.addWidget(self.startup_textarea)
        hbox.addWidget(self.button_startup_folder)

        hbox2 = QHBoxLayout()
        self.label_3 = QLabel()
        self.label_3.setText("Vertical scroll up/down angles")
        self.combo_box1 = QComboBox()
        self.combo_box1.addItem("47 -13 (default)")
        self.combo_box1.addItem("52 -18")
        self.combo_box1.addItem("57 -23")
        self.combo_box1.currentIndexChanged["int"].connect(self.combo_box1_changed)
        hbox2.addWidget(self.label_3)
        hbox2.addWidget(self.combo_box1)

        hbox5 = QHBoxLayout()
        self.label_5 = QLabel()
        self.label_5.setText("Vscroll speed")
        self.combo_box3 = QComboBox()
        self.combo_box3.addItem("slower")
        self.combo_box3.addItem("slow")
        self.combo_box3.addItem("normal (default)")
        self.combo_box3.addItem("fast")
        self.combo_box3.addItem("faster")
        self.combo_box3.currentIndexChanged["int"].connect(self.combo_box3_changed)
        hbox5.addWidget(self.label_5)
        hbox5.addWidget(self.combo_box3)

        hbox3 = QHBoxLayout()
        self.label_4 = QLabel()
        self.label_4.setText("Invert mouse")
        rb_group = QButtonGroup(self)
        self.radiobutton_yes = QRadioButton()
        self.radiobutton_no = QRadioButton()
        self.radiobutton_yes.setText("Yes")
        self.radiobutton_no.setText("No")
        self.radiobutton_no.setChecked(True)
        self.radiobutton_yes.toggled.connect(lambda: self.radiobutton_ch("yes"))
        self.radiobutton_no.toggled.connect(lambda: self.radiobutton_ch("no"))
        rb_group.addButton(self.radiobutton_yes)
        rb_group.addButton(self.radiobutton_no)
        hbox3.addWidget(self.label_4, 20)
        hbox3.addWidget(self.radiobutton_yes, 10)
        hbox3.addWidget(self.radiobutton_no, 10)

        hbox4 = QHBoxLayout()
        self.label_4 = QLabel()
        self.label_4.setText("Mouse movement speed")
        self.combo_box2 = QComboBox()
        self.combo_box2.addItem("slow")
        self.combo_box2.addItem("normal (default)")
        self.combo_box2.addItem("fast")
        self.combo_box2.currentIndexChanged["int"].connect(self.combo_box2_changed)
        hbox4.addWidget(self.label_4)
        hbox4.addWidget(self.combo_box2)

        layout.addLayout(hbox, 1, 0)
        layout.setRowStretch(10, 0)
        layout.addLayout(hbox2, 2, 0)
        layout.addLayout(hbox3, 4, 0)
        layout.addLayout(hbox4, 5, 0)
        layout.addLayout(hbox5, 6, 0)

        self.setLayout(layout)

    def set_startup_folder(self):
        """ saves the path to the startup folder"""
        self.parent.configuration.startup_path = str(self.startup_textarea.text())

    def combo_box1_changed(self):
        """ vscroll angles combobox changed"""

        self.parent._print("vscroll angles changed")

        self.parent.configuration.basic.vscroll_angles = self.combo_box1.currentText()

    def combo_box2_changed(self):
        """ cursor speed combobox changed"""

        self.parent._print("cursor speed changed")
        dic = {"slow": 0.8,
               "normal (default)": 1,
               "fast": 1.3}
        self.parent.configuration.basic.mouse_vel = dic.get(str(self.combo_box2.currentText()))

    def combo_box3_changed(self):
        """ vscroll speed combobox changed"""

        self.parent._print("vscroll speed changed")
        dic = {"slower": "18/8",
               "slow": "25/15",
               "normal (default)": "30/20",
               "fast": "40/30",
               "faster": "50/40"}
        self.parent.configuration.basic.vscroll_vel = dic.get(str(self.combo_box3.currentText()))

    def radiobutton_ch(self, what):
        """ enables/disables mouse invertion when controlling

        :param what: yes or no
        """

        self.parent._print("mouse invert changed")
        self.parent.configuration.basic.invert_mouse = "yes" if what == "yes" else "no"
