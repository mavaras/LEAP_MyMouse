# -*- coding: utf-8 -*-

# ===============CONFIGURATION===============
# == class and subclasses


import sys


# CLASS CONTAINING CONFIGURATION DATA
class Conf():
	file_name = ""
	file_date = ""
	file_path = ""

	def __init__(self):
		self.basic = self.Basic()
		self.extra = self.Extra()

	# this loads conf configuration file into system
	def load_conf(self, conf):
		# conf info
		self.file_name = conf.readline()
		self.file_path = conf.readline()
		self.file_date = conf.readline()

		# basic conf
		self.basic.mm = linecache.getline(str(conf.name), 6)
		self.basic.lclick = linecache.getline(str(conf.name), 7)
		self.basic.rclick = linecache.getline(str(conf.name), 8)
		self.basic.vscroll = linecache.getline(str(conf.name), 9)
		self.basic.hscroll = linecache.getline(str(conf.name), 10)
		self.basic.grabb = linecache.getline(str(conf.name), 11)
		self.basic.changew = linecache.getline(str(conf.name), 12)
		self.basic.closew = linecache.getline(str(conf.name), 13)
		self.basic.minimizew = linecache.getline(str(conf.name), 14)

		# extra conf
		"""self.basic.mm = linecache.getline(str(conf.name), 6)
		self.basic.lclick = linecache.getline(str(conf.name), 7)
		self.basic.rclick = linecache.getline(str(conf.name), 8)"""
		
		print("Content of configuration file "+str(conf.name)+":")
		for line in conf:
			print(line),

	# classes for both configuration types
	class Basic():
		def __init__(self):
			self.mm = 1
			self.lclick = "default"
			self.rclick = "default"
			self.hscroll = "default"
			self.vscroll = "default"
			self.grabb = "default"
			self.changew = "default"
			self.closew = "default"
			self.minimizew = "default"

		def get_conf(self):
			aux = ("Basic Conf:\n"
				  +str(self.mm)+"\n"
				  +str(self.lclick)+"\n"
				  +str(self.rclick)+"\n"
				  +str(self.vscroll)+"\n"
				  +str(self.hscroll)+"\n"
				  +str(self.grabb)+"\n"
				  +str(self.changew)+"\n"
				  +str(self.closew)+"\n"
				  +str(self.minimizew)+"\n"
			)
			return aux			
			
	class Extra():
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
			aux = ("Extra Conf:\n"
				  +str(self.open_calc)+"\n"
				  +str(self.open_texteditor)+"\n"
				  +str(self.open_console)+"\n"
				  +str(self.open_browser)+"\n"
				  +str(self.open_custom_1)+"\n"
				  +str(self.open_custom_2)+"\n"
				  +str(self.open_custom_3)+"\n"
				  +str(self.open_custom_4)+"\n"
			)
			return aux
