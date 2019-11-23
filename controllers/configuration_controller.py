# -*- coding: utf-8 -*-

from controllers.utils import *


class Controller:
    """ this class handles all the view events and interacts with the model (Configuration)"""

    def __init__(self, view, listener, model):
        view.setFixedSize(view.size())
        view.statusBar().setVisible(False)
        view.show()
        view.controller = self
        view.configuration = model

        self.cb_action_gesture = {}

        self.view = view
        self.listener = listener

    def start_stop_control(self):
        """ this handles the click event to "Start Control" or "Stop Control" into notification
        area icon
        """

        if not self.listener.status.leap_connected:
            self.view.button_stop.setChecked(True)
            self.view.button_start.setChecked(False)
            self.view.show_popup("Problem Detected",
                                 "Leap Motion error",
                                 "Leap Motion device is not connected")
        else:
            if self.view.configuration.check():
                if not self.listener.mouse.active:
                    self.listener.mouse.active = True
                    self.view.button_stop.setChecked(False)
                    self.view.button_stop.setEnabled(True)
                    self.view.button_start.setChecked(True)

                else:
                    self.listener.mouse.active = False
                    self.view.button_start.setChecked(False)
                    self.view.button_start.setEnabled(True)
                    self.view.button_stop.setChecked(True)

            else:
                self.view.show_popup("Problem Detected",
                                     "Configuration error",
                                     "You have same gesture assigned to multiple actions in your configuration")

    def save_conf_file(self, fname):
        """ writes and saves the given file with the configuration info

        :param fname: file path and name to be saved to
        """

        f = open(fname, "w+")

        self.view.configuration.file_name = str(fname.split("/")[-1])
        self.view.configuration.file_path = str("/".join(str(fname).split("/")[:-1]))
        self.view.configuration.file_date = time.ctime(os.path.getctime(fname))

        f.write(self.view.configuration.profile_name + "\n" +
                self.view.configuration.file_name + "\n" +
                self.view.configuration.file_path + "\n" +
                self.view.configuration.file_date + "\n\n")
        f.write(self.view.configuration.basic.get_conf())
        f.write("\n")
        f.write(self.view.configuration.extra.get_conf())
        f.close()

    def load_conf_file(self, fname):
        """ loads content of fname configuration file into Configuration object"""

        f = open(fname, "r")
        self.view.configuration.load_conf(f)
        f.close()

    def load_conf(self):
        """ loads given configuration object into SYSTEM
        updates comboboxes and GUI elements
        using cb_action_gesture array
        """

        self.view.combo_box_mm.setCurrentIndex(int(self.view.configuration.basic.mm))

        self.view.combo_box_click.setCurrentIndex(
            get_dict_key(self.view.cb_action_gesture[self.view.combo_box_click], self.view.configuration.basic.lclick)
        )

        self.view.combo_box_rclick.setCurrentIndex(
            get_dict_key(self.view.cb_action_gesture[self.view.combo_box_rclick], self.view.configuration.basic.rclick)
        )

        self.view.combo_box_minimizew.setCurrentIndex(
            get_dict_key(self.view.cb_action_gesture[self.view.combo_box_minimizew], self.view.configuration.basic.minimizew)
        )

        self.view.combo_box_closew.setCurrentIndex(
            get_dict_key(self.view.cb_action_gesture[self.view.combo_box_closew], self.view.configuration.basic.closew)
        )

        self.view.combo_box_changew.setCurrentIndex(
            get_dict_key(self.view.cb_action_gesture[self.view.combo_box_changew], self.view.configuration.basic.changew)
        )

        self.view.combo_box_vscroll.setCurrentIndex(
            get_dict_key(self.view.cb_action_gesture[self.view.combo_box_vscroll], self.view.configuration.basic.vscroll)
        )

        self.view.combo_box_hscroll.setCurrentIndex(
            get_dict_key(self.view.cb_action_gesture[self.view.combo_box_hscroll], self.view.configuration.basic.hscroll)
        )

    def set_profile_name(self, name):
        """ changes the configuration profile name to the new one given by the user"""

        self.view.label_conf_file.setText(name)
        self.view.configuration.profile_name = str(name)
        self.update_file(str(self.view.configuration.file_path)+"/"+str(self.view.configuration.file_name),
                         0,
                         self.view.configuration.profile_name)

    def update_file(self, fname, line, replace):
        """ updates a given file name in the given file with the given content

        :param fname: file path and name to be saved to
        :param line: which line to be updated
        :param replace: new content
        """

        with open(fname, "r") as file:
            file_content = file.readlines()

        file_content[line] = replace + str("\n")
        with open(fname, "w") as file:
            file.writelines(file_content)

    def combo_box_actiongesture_changed(self, combo_box_name):
        """ collection of key events binded to GUI (configuration tab comboboxes)

        :param combo_box_name: changed combobox variable name
        """

        if combo_box_name == "combo_box_click":
            print("lclick changed" + str(self.view.combo_box_click.currentIndex()))
            self.view.configuration.basic.lclick = self.view.cb_action_gesture[self.view.combo_box_click] \
                .get(self.view.combo_box_click.currentIndex())

        elif combo_box_name == "combo_box_rclick":
            print("rclick changed")
            self.view.configuration.basic.rclick = self.view.cb_action_gesture[self.view.combo_box_rclick] \
                .get(self.view.combo_box_rclick.currentIndex())

        elif combo_box_name == "combo_box_mm":
            self.view.configuration.basic.mm = self.view.combo_box_mm.currentIndex()

        elif combo_box_name == "combo_box_minimizew":
            self.view.configuration.basic.minimizew = self.view.cb_action_gesture[self.view.combo_box_minimizew] \
                .get(self.view.combo_box_minimizew.currentIndex())

        elif combo_box_name == "combo_box_closew":
            self.view.configuration.basic.closew = self.view.cb_action_gesture[self.view.combo_box_closew] \
                .get(self.view.combo_box_closew.currentIndex())

        elif combo_box_name == "combo_box_changew":
            self.view.configuration.basic.changew = self.view.cb_action_gesture[self.view.combo_box_changew] \
                .get(self.view.combo_box_changew.currentIndex())

        elif combo_box_name == "combo_box_vscroll":
            self.view.configuration.basic.vscroll = self.view.cb_action_gesture[self.view.combo_box_vscroll] \
                .get(self.view.combo_box_vscroll.currentIndex())

        elif combo_box_name == "combo_box_hscroll":
            self.view.configuration.basic.hscroll = self.view.cb_action_gesture[self.view.combo_box_hscroll] \
                .get(self.view.combo_box_hscroll.currentIndex())

        elif combo_box_name == "combo_box_grabb":
            self.view.configuration.basic.grabb = self.view.cb_action_gesture[self.view.combo_box_grabb] \
                .get(self.view.combo_box_grabb.currentIndex())

        elif combo_box_name == "combo_box_showdesktop":
            self.view.configuration.extra.show_desktop = self.view.cb_action_gesture[self.view.combo_box_showdesktop] \
                .get(self.view.combo_box_showdesktop.currentIndex())

        elif combo_box_name == "combo_box_openfexplorer":
            self.view.configuration.extra.show_explorer = self.view.cb_action_gesture[self.view.combo_box_openfexplorer] \
                .get(self.view.combo_box_openfexplorer.currentIndex())

        elif combo_box_name == "combo_box_copy":
            self.view.configuration.extra.copy = self.view.cb_action_gesture[self.view.combo_box_copy] \
                .get(self.view.combo_box_copy.currentIndex())

        elif combo_box_name == "combo_box_paste":
            self.view.configuration.extra.paste = self.view.cb_action_gesture[self.view.combo_box_paste] \
                .get(self.view.combo_box_paste.currentIndex())

        elif combo_box_name == "combo_box_cut":
            self.view.configuration.extra.cut = self.view.cb_action_gesture[self.view.combo_box_cut] \
                .get(self.view.combo_box_cut.currentIndex())

        self.view.setFocus()
