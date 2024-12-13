# -*- coding: utf-8 -*-

import os 
import sys
import pyfiglet
import colorama
import json
import OpenEXR
import Levenshtein

from termcolor import *
from time import sleep



from textual.app import App, ComposeResult
from textual.widgets import Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.screen import Screen 
from textual import events
from textual import work
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual import on




class RMD_EXR():



	"""
	def check_input_sequence_function(self):
		with self.suspend():

			self.display_notification_function("Checking input sequence")
			self.display_notification_function(self.input_path)

			for item in os.listdir(self.input_path):
				if os.path.isfile(os.path.join(self.input_path,item))==True:
					self.display_message_function(item)


			os.system("pause")
	"""


	#AS A THREAD
	def check_input_sequence_function(self):
		try:
			self.call_from_thread(self.display_notification_function, "CHECKING INPUT SEQUENCE")
			self.call_from_thread(self.display_notification_function, self.input_path)

			#get the content in the input path
			for item in os.listdir(self.input_path):
				if os.path.isfile(os.path.join(self.input_path,item))==True:
					self.call_from_thread(self.display_message_function, "  %s"%item, False)
		except Exception as e:
			self.call_from_thread(self.display_error_function, e)
