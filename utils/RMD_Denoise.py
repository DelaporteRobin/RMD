# -*- coding: utf-8 -*-



import os
import sys
import json
import OpenEXR
import traceback
import pyfiglet


from textual.app import App, ComposeResult
from textual.widgets import Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.screen import Screen 
from textual import events
from textual import work
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual import on


from config import *





class RMD_DENOISE:
	def denoise_function(self):



		self.display_notification_function("CALLING DENOISE FUNCTION")
		self.display_notification_function(pyfiglet.figlet_format("RMD DENOISE", font=ASCII_FONT_TERMINAL), False)


		for sequence_name, sequence_data in self.FINAL_SEQUENCE_DICTIONNARY.items():
			if os.path.isfile(os.path.join(os.getcwd(), "config/config_%s.json"%sequence_name)):
				self.display_success_function("CONFIG FOUND FOR %s"%sequence_name)
			else:
				self.display_error_function("CONFIG NOT FOUND FOR %s"%sequence_name)
				continue


			self.display_notification_function("LAUNCHING DENOISE TASK FOR %s"%sequence_name.upper())
			try:
				os.system('"%s/bin/denoise_batch.exe" -j %s' % (PIXAR_PATH, os.path.join(os.getcwd(), "config/config_%s.json"%sequence_name)))
			except Exception as e:
				self.display_error_function("Impossible to call denoising process")
				self.display_error_function("e")
			else:
				self.display_success_function("Task done")

