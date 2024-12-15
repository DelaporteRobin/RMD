# -*- coding: utf-8 -*-


import os
import sys
import pyfiglet
import copy

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
from typing import Iterable


import colorama


#IMPORT RMD MODULES
import config

from utils.RMD_EXRMaster import RMD_EXR
from utils.RMD_Logging import RMD_LOG

from styles.theme_file import *





class DirectoryTree_DIR(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if os.path.isfile(path)==False]

class DirectoryTree_FILES(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if os.path.isfile(path)==True]




class RMD_APP(App, RMD_LOG, RMD_EXR):

	CSS_PATH = ["styles/layout.tcss"]
	def __init__(self):

		super().__init__()

		self.color_dictionnary = self.theme_variables


		self.program_log_dictionnary = {}
		self.program_log_dictionnary_cache = {}


		self.font_title = "ansi_shadow"

		




		self.input_path = Path("/")
		self.output_path = Path("/")








	def compose(self) -> ComposeResult:
		yield Header(show_clock=True) 


		with Horizontal(id="horizontal_container_main"):
			with VerticalScroll(id="verticalscroll_leftcolumn_main"):
				self.label_title = Label(pyfiglet.figlet_format("RMD %s"%str(config.VERSION), font=self.font_title))
				yield self.label_title


				with Collapsible(title="INPUT OUTPUT FOLDER", id="collapsible_input_output"):
					self.input_drive_path = Input(placeholder="Root path", id="input_drive_path")
					yield self.input_drive_path
					with Horizontal(id="horizontal_inputoutput_container"):

						with VerticalScroll(id="vertical_input_container"):
							self.label_input_folder = Label("")
							yield self.label_input_folder

							self.directorytree_input = DirectoryTree_DIR(self.input_path,id="directorytree_input")
							self.directorytree_input.border_title = "Input Folder"
							yield self.directorytree_input

						with VerticalScroll(id="vertical_output_container"):
							self.label_output_folder = Label("")
							yield self.label_output_folder

							self.directorytree_output = DirectoryTree_DIR(self.input_path,id="directorytree_output")
							self.directorytree_output.border_title = "Output Folder"
							yield self.directorytree_output

				with Horizontal(id = "horizontal_denoisesettings_container"):
					with VerticalScroll(id="vertical_checksequence_container"):
						yield Button("CHECK INPUT SEQUENCE", id="button_checkinput")



			with VerticalScroll(id="verticalscroll_rightcolumn_main"):
				self.listview_log = ListView(id="listview_log")
				yield self.listview_log








	def on_mount(self) -> None:

		#display all colors in theme

		
		for line in config.WELCOME.splitlines():
			self.display_notification_function(line, False)
		
		

		self.display_success_function("TUI Built successfully")


		#loading themes
		for theme in theme_registry:
			self.register_theme(theme)
		#apply the theme specified in config file
		self.theme = "downtown"






	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "button_checkinput":

			#self.check_input_sequence_function()
			#START THE FUNCTION AS A THREAD?

			self.thread_check_input = threading.Thread(target=self.check_input_sequence_function, args=())
			self.thread_check_input.start()



	def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
		if event.control.id == "directorytree_input":
			self.input_path = str(event.path)

			self.display_message_function("", time=False)
			self.display_message_function("Input Path : %s"%self.input_path)
			#self.static_input_sequence.update(self.directorytree_input)

			#get the name of the last folder of the path
			self.output_path = os.path.join(os.path.dirname(self.input_path), "output_denoise")
			self.display_message_function("Auto Output Path : %s"%self.output_path)

			self.label_input_folder.update(self.input_path)
			self.label_output_folder.update(self.output_path)

			#create an output path from the input sequence path
		if event.control.id == "directorytree_output":
			self.output_path = str(event.path)
			self.label_output_folder.update(self.output_path)

			self.display_message_function("Output Path : %s"%self.output_path)


	def on_input_submitted(self, event: Input.Submitted) -> None:
		if event.control.id == "input_drive_path":
			if os.path.isdir(self.input_drive_path.value)==True:
				self.directorytree_input.path = self.input_drive_path.value
				self.directorytree_output.path = self.input_drive_path.value
				self.display_message_function("Starting path changed : %s"%self.input_drive_path.value)
			else:
				self.display_error_function("This folder path isn't valid")

		
			




if __name__ == "__main__":
	App = RMD_APP()
	App.run()

