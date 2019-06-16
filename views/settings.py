"""
Settings window
-> vscroll pitch angle
-> startup folder
"""

import os

from PyQt4.QtGui import *
from views.gui_qtdesigner import *

from _print import _print
from gvariables import gv


class Settings(QDialog):
    def __init__(self, parent):
        super(Settings, self).__init__(parent)

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
        self.startup_textarea.setText(
            str(os.path.expanduser("~"))+"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
        )
        self.startup_textarea.setFocus(False)
        hbox.addWidget(self.label_2)
        hbox.addWidget(self.startup_textarea)

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

        hbox3 = QHBoxLayout()
        self.label_4 = QLabel()
        self.label_4.setText("Invert mouse")
        rb_group = QtGui.QButtonGroup(self)
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

        layout.addLayout(hbox, 1, 0)
        layout.setRowStretch(10, 0)
        layout.addLayout(hbox2, 2, 0)
        layout.addLayout(hbox3, 4, 0)

        self.setLayout(layout)

    def combo_box1_changed(self):
        """ vscroll angles combobox changed"""

        _print("vscroll angles changed")

        gv.configuration.basic.vscroll_angles = self.combo_box1.currentText()

    def radiobutton_ch(self, what):
        """ enables/disables mouse invertion when controlling

        :param what: yes or no
        """

        _print("mouse invert changed")

        if what == "yes":
            gv.configuration.basic.invert_mouse = True
        else:
            gv.configuration.basic.invert_mouse = False


