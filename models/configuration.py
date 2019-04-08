# -*- coding: utf-8 -*-

# ===============CONFIGURATION===============
# == class and subclasses


import sys
import linecache


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

        print("Content of configuration file " + str(conf.name) + ":")
        for line in conf:
            print("    " + str(line)),

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
            self.closew = "X"
            self.minimizew = "T"

        def get_conf(self):
            """ prints configuration attributes"""
            aux = ("Basic Conf:\n"
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
            self.open_calc = "default"
            self.open_texteditor = "default"
            self.open_console = "default"
            self.open_browser = "default"

            self.open_custom_1 = "empty"
            self.open_custom_2 = "empty"
            self.open_custom_3 = "empty"
            self.open_custom_4 = "empty"

        def get_conf(self):
            """ prints configuration attributes"""
            aux = ("Extra Conf:\n"
                   + str(self.open_calc) + "\n"
                   + str(self.open_texteditor) + "\n"
                   + str(self.open_console) + "\n"
                   + str(self.open_browser) + "\n"
                   + str(self.open_custom_1) + "\n"
                   + str(self.open_custom_2) + "\n"
                   + str(self.open_custom_3) + "\n"
                   + str(self.open_custom_4) + "\n\n"
                   )
            return aux
