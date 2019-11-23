# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class OSHandle:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_opened_windows_list(self):
        pass
    
    @abstractmethod
    def foreach_window(self):
        pass

    @abstractmethod
    def bring_window_to_top(self):
        pass

    @abstractmethod
    def minimize_window(self):
        pass

    @abstractmethod
    def close_window(self):
        pass

    @abstractmethod
    def get_current_window_hwnd(self):
        pass

    @abstractmethod
    def get_current_window_name(self):
        pass

    @abstractmethod
    def create_shortcut(self):
        pass

    @abstractmethod
    def remove_shortcut(self):
        pass