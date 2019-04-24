# -*- coding: utf-8 -*-

# ===============CONFIGURATION===============
# == class and subclasses


import linecache
from _print import _print


# CLASS CONTAINING CONFIGURATION DATA
class Conf:
    file_name = ""
    file_date = ""
    file_path = ""

    def __init__(self):
        self.basic = self.Basic()
        self.extra = self.Extra()

    def load_conf(self, conf):
        """ loads given configuration file into this object
        :param conf: file
        """
        # conf info
        self.file_name = conf.readline()
        self.file_path = conf.readline()
        self.file_date = conf.readline()

        # basic conf
        self.basic.mm = linecache.getline(str(conf.name), 6).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.lclick = linecache.getline(str(conf.name), 7).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.rclick = linecache.getline(str(conf.name), 8).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.vscroll = linecache.getline(str(conf.name), 9).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.hscroll = linecache.getline(str(conf.name), 10).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.grabb = linecache.getline(str(conf.name), 11).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.changew = linecache.getline(str(conf.name), 12).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.closew = linecache.getline(str(conf.name), 13).split(":")[1].replace("\n", "").replace("\r", "")
        self.basic.minimizew = linecache.getline(str(conf.name), 14).split(":")[1].replace("\n", "").replace("\r", "")

        # extra conf
        """self.basic.mm = linecache.getline(str(conf.name), 6)
        self.basic.lclick = linecache.getline(str(conf.name), 7)
        self.basic.rclick = linecache.getline(str(conf.name), 8)"""
        print("->" + str(self.basic.closew))
        print("Content of configuration file " + str(conf.name) + ":")
        for line in conf:
            print("    " + str(line)),

    def check(self):
        """ checks if configurations is right, that is,
        if same gesture isn't assigned to multiple actions
        :return: true if all is ok, false if not
        """
        return (len(self.basic.__dict__.values()) == len(set(self.basic.__dict__.values())) and \
                len(self.extra.__dict__.values()) == len(set(self.extra.__dict__.values())))

    # classes for both configuration types
    class Basic:
        def __init__(self):
            # default comboboxes values (GUI)
            self.mm = 1
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

    class Extra():
        # TODO: include this features

        def __init__(self):
            self.show_desktop = "D"
            self.show_explorer = "X"
            self.open_calc = "default"
            self.open_texteditor = "default"
            self.open_console = "default"
            self.open_browser = "default"

            self.copy = "C"
            self.cut = "W"
            self.paste = ""

            self.open_custom_1 = "empty"
            self.open_custom_2 = "empty"
            self.open_custom_3 = "empty"
            self.open_custom_4 = "empty"

        def get_conf(self):
            """ prints configuration attributes"""
            aux = ("Extra Conf->\n"
                   + "show_desktop:" + str(self.show_desktop) + "\n"
                   + "show_explorer:" + str(self.show_explorer) + "\n"
                   + "open_calc:" + str(self.open_calc) + "\n"
                   + "open_texteditor:" + str(self.open_texteditor) + "\n"
                   + "copy:" + str(self.open_copy) + "\n"
                   + "cut:" + str(self.open_cut) + "\n"
                   + "paste:" + str(self.open_paste) + "\n\n"
                   )
            return aux
