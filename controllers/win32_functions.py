
# ===============WIN32 CONTROL FUNCTIONS===============
# == actions


import sys
import ctypes
import win32api, win32con, win32gui


# needed variables
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

opened_windows_names = []
# functions
def get_opened_windows_list():
	global opened_windows_names
	EnumWindows(EnumWindowsProc(foreach_window), 0)
	return opened_windows_names
	
# this is passed as argument when we call EnumWindows, fills titles array with current opened windows names
def foreach_window(hwnd, lParam):
	global opened_windows_names
	if IsWindowVisible(hwnd):
		length = GetWindowTextLength(hwnd)
		buff = ctypes.create_unicode_buffer(length + 1)
		GetWindowText(hwnd, buff, length + 1)
		if buff.value != "":
			opened_windows_names.append(buff.value)
		
	return True

# do alt+tab to hwnd window
def bring_window_to_top(hwnd):
	win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
	win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

# minimizes hwnd window
def minimize_window(hwnd):
	win32gui.CloseWindow(hwnd)

# closes hwnd window
def close_window(hwnd):
	win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

# return current window hwnd
def get_current_window_hwnd():
	return win32gui.GetForegroundWindow()
	
# returns current window name
def get_current_window_name():
	hwnd = get_current_window_hwnd()
	length = GetWindowTextLength(hwnd)
	buff = ctypes.create_unicode_buffer(length + 1)
	GetWindowText(hwnd, buff, length + 1)
	#print("buff.value: "+buff.value.encode('latin1'))
	return buff.value
	#return unicode(win32gui.GetWindowText(win32gui.GetForegroundWindow()), errors="ignore")
