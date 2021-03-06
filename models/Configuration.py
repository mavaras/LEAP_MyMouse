# -*- coding: utf-8 -*-

# ===============CONFIGURATION===============
# == class and subclasses
# == clase abstract patron command


from abc import ABCMeta, abstractmethod


class Conf:
    """ This CLASS contains configuration file info and
    configuration data, structured as follows:
    -> basic configuration: basic actions on mouse and windows
    -> extra configuration: some not so useful, additional, features
    """

    __metaclass__ = ABCMeta

    startup_path = ""

    profile_name = "none"
    file_name = ""
    file_date = ""
    file_path = ""

    def __init__(self):
        self.basic = self.Basic()
        self.extra = self.Extra()

    @abstractmethod
    def load_conf(self, conf):
        """ abstract method related to which method we have to load the configuration into system
        .txt file, database, web etc.
        """

        pass

    def check(self):
        """ checks if configurations is right, that is,
        if same gesture isn't assigned to multiple actions

        :return: true if all is ok, false if not
        """

        print(len(self.basic.__dict__.values())),
        print(len(set(self.basic.__dict__.values()))),
        print(len(self.extra.__dict__.values())),
        print(len(set(self.extra.__dict__.values())))
        return (len(self.basic.__dict__.values()) == len(set(self.basic.__dict__.values()))+1 and \
                len(self.extra.__dict__.values()) == len(set(self.extra.__dict__.values())))

    # classes for both configuration types
    class Basic:
        def __init__(self):
            self.invert_mouse = "no"
            self.mouse_vel = 1
            self.vscroll_angles = "-13/47"
            self.vscroll_vel = "30/20"

            # default comboboxes values (GUI)
            self.mm = "1"
            self.lclick = "click_planem"
            self.rclick = "rclick_f2down"
            self.hscroll = "default"
            self.vscroll = "5_fingers_UD"
            self.grabb = "default"
            self.changew = "90_and_swipe"
            self.closew = "T"
            self.minimizew = "V"

        def get_conf(self):
            """ prints configuration attributes"""

            aux = ("Basic Conf->\n"
                   + "mm:" + str(self.mm) + "\n"
                   + "lclick:" + str(self.lclick) + "\n"
                   + "rclick:" + str(self.rclick) + "\n"
                   + "vscroll:" + str(self.vscroll) + "\n"
                   + "hscroll:" + str(self.hscroll) + "\n"
                   + "grabb:" + str(self.grabb) + "\n"
                   + "changew:" + str(self.changew) + "\n"
                   + "closew:" + str(self.closew) + "\n"
                   + "minimizew:" + str(self.minimizew) + "\n"
                   )
            return aux

    class Extra:
        # TODO: include this features

        def __init__(self):
            self.show_desktop = "D"
            self.show_explorer = "X"

            self.copy = "C"
            self.cut = "W"
            self.paste = "L"

        def get_conf(self):
            """ prints configuration attributes"""

            aux = ("Extra Conf->\n"
                   + "show_desktop:" + str(self.show_desktop) + "\n"
                   + "show_explorer:" + str(self.show_explorer) + "\n"
                   + "copy:" + str(self.copy) + "\n"
                   + "cut:" + str(self.cut) + "\n"
                   + "paste:" + str(self.paste) + "\n\n"
                   )
            return aux
