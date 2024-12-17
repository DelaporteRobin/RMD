# -*- coding: utf-8 -*-



import os
import sys
import json
import OpenEXR


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






class RMD_CONFIG():



	def create_config_function(self):
		
		if self.FINAL_SEQUENCE_DICTIONNARY == {}:
			self.call_from_thread(self.display_error_function, "Sequence dictionnary is empty")
			return 

		if (os.path.isdir(self.input_path)==False) or (os.path.isdir(self.output_path)==False):
			self.call_from_thread(self.display_error_function("Input or Output path not existing"))
			return


		try:
			#check if all required aovs are in the file
			for required_aov in AOV_REQUIRED:
				self.call_from_thread(self.display_message_function, required_aov)
		except Exception as e:
			self.call_from_thread(self.display_error_function, e)