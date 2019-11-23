import ctypes
import time
import os
from controllers.OSHandle import OSHandle
import pyautogui
import Xlib.display
import gi                         #Import gi pageage
gi.require_version('Wnck','3.0')
from gi.repository import Wnck    #Import Wnck module


class LinuxHandle(OSHandle):  # not used right now

    def lclick(self, x, y):
        """ performs a left click on the mouse

        :param x: mouse X coordinate
        :param y: mouse Y coordinate
        """
        
        pyautogui.click(clicks=1, x=x, y=y, interval=.2)

    def rclick(self, x, y):
        """ performs a right click on the mouse

        :param x: mouse X coordinate
        :param y: mouse Y coordinate
        """
        
        pyautogui.click(button="right", clicks=1, x=x, y=y, interval=.2)

    def vscroll(self, x, y, vel):
        """ performs a vertical scroll on the mouse

        :param x: mouse X coordinate
        :param y: mouse Y coordinate
        :param vel: > 0 up, < 0 down
        """

        pyautogui.scroll(vel, x, y)  # this is not tested !

    def get_opened_windows_list(self):
        """ returns an array with all opened windows titles"""
        '''
        display = Xlib.display.Display()
        screen = display.screen()
        root = screen.root
        tree = root.query_tree()
        wins = tree.children

        print(list(dict.fromkeys([win.get_wm_name() for win in wins if win.get_wm_name() not in [None, '']])))
        # this will be problematic
        return list(dict.fromkeys([win.get_wm_name() for win in wins if win.get_wm_name() not in [None, '']]))
        '''

        screen = Wnck.Screen.get_default()
        screen.force_update()
        opened_windows = screen.get_windows()
        return [w.get_name() for w in opened_windows]
        for w in windows:
            print(w.get_name())


    def foreach_window(self, hwnd, lParam):
        pass

    def bring_window_to_top(self, hwnd):
        """ bring to front hwnd window

        :param hwnd: Window handle
        """

        hwnd.unminimize()

    def minimize_window(self, hwnd):
        """ minimizes hwnd window

        :param hwnd: Window handle
        """

        hwnd.minimize()

    def close_window(self, hwnd):
        """ closes hwnd window

        :param hwnd: Window handle
        """

        hwnd.close(1)

    def get_current_window_hwnd(self):
        """ return current window hwnd

        :return: window handle
        """

        screen = Wnck.Screen.get_default()
        screen.force_update()
        opened_windows = screen.get_windows()
        return [w for w in opened_windows if w.is_active()][0]

    def get_current_window_name(self):
        """ returns currently on top window name

        :return: window name
        """

        screen = Wnck.Screen.get_default()
        screen.force_update()
        opened_windows = screen.get_windows()
        return [w.get_name() for w in opened_windows if w.is_active()][0]

    def create_shortcut(self, startup_path):
        """ copies the .exe file to the startup folder"""

        startup = startup_path
        path = os.path.join(startup, "shortcut.lnk")
        target = os.path.dirname(os.path.dirname(__file__))+str("\LEAP_MyMouse_.exe")
        icon = os.path.dirname(os.path.dirname(__file__))+str("\\res\icons\leapmymouse.png")

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.IconLocation = icon
        shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
        shortcut.save()

    def remove_shortcut(self, startup_path):
        """ removes the .exe file from the startup folder"""

        os.remove(startup_path)