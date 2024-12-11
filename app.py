# -*- coding: utf-8 -*-


import os
import sys
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

import threading
from pathlib import Path
from datetime import datetime
from pyfiglet import Figlet
from time import sleep
from termcolor import *


import colorama


#IMPORT RMD MODULES
import config
from utils.RMD_Logging import RMD_LOG




class RMD_APP(App, RMD_LOG):

	CSS_PATH = ["styles/layout.tcss"]
	def __init__(self):

		super().__init__()

		self.color_dictionnary = self.theme_variables


		self.font_title = "ansi_shadow"

		


		



		self.input_path = Path("/")
		self.output_path = Path("/")








	def compose(self) -> ComposeResult:
		yield Header(show_clock=True) 


		with Horizontal(id="horizontal_container_main"):
			with VerticalScroll(id="verticalscroll_leftcolumn_main"):
				self.label_title = Label(pyfiglet.figlet_format("RMD %s"%str(config.VERSION), font=self.font_title))
				yield self.label_title


			with VerticalScroll(id="verticalscroll_rightcolumn_main"):
				self.listview_log = ListView(id="listview_log")
				yield self.listview_log



	def on_mount(self) -> None:

		#display all colors in theme
		for line in config.WELCOME.splitlines():
			self.display_notification_function(line, False)


		self.display_success_function("TUI Built successfully")

		
			




if __name__ == "__main__":
	App = RMD_APP()
	App.run()

