# -*- coding: utf-8 -*-


import os
import sys
import pyfiglet
import copy
import json

from textual.app import App, ComposeResult
from textual.widgets import Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.screen import Screen 
from textual import events
from textual import work
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual import on

from textual_plotext import PlotextPlot

import threading
from pathlib import Path
from datetime import datetime
from pyfiglet import Figlet
from time import sleep
from termcolor import *
from typing import Iterable


import colorama


#IMPORT RMD MODULES
from config import *
import config

from utils.RMD_EXRMaster import RMD_EXR
from utils.RMD_Logging import RMD_LOG
from utils.RMD_Config import RMD_CONFIG
from utils.RMD_Denoise import RMD_DENOISE

from styles.theme_file import *





class DirectoryTree_DIR(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if os.path.isfile(path)==False]

class DirectoryTree_FILES(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if os.path.isfile(path)==True]




class RMD_APP(App, RMD_LOG, RMD_EXR, RMD_CONFIG, RMD_DENOISE):

	CSS_PATH = ["styles/layout.tcss"]
	def __init__(self):

		super().__init__()

		self.color_dictionnary = self.theme_variables


		self.program_log_dictionnary = {}
		self.program_log_dictionnary_cache = {}


		self.font_title = "ansi_shadow"

		


		self.SEQUENCE_SIZE = 0
		self.SEQUENCE_LENGTH = 0
		self.SEQUENCE_SIMILARITY = {}
		self.SEQUENCE_SKIP_FRAMES = []
		self.SEQUENCE_FRAME_LIST = []
		self.SEQUENCE_FRAME_INDEX_LIST = []
		self.SEQUENCE_FRAME_SIZE_LIST = []
		self.FINAL_SEQUENCE_DICTIONNARY = {}

		self.CONFIG_LIST = []
		self.COMBINED_SEQUENCE_LIST = []
		self.ALPHA_SEQUENCE_LIST = []

		self.COMPRESSION_MODE = "DWAB_COMPRESSION"






		self.input_path = Path("/")
		self.output_path = Path("/")








	def compose(self) -> ComposeResult:
		yield Header(show_clock=True) 


		with Horizontal(id="horizontal_container_main"):
			with VerticalScroll(id="verticalscroll_leftcolumn_main"):
				self.label_title = Label(pyfiglet.figlet_format("RMD %s"%str(config.VERSION), font=ASCII_FONT_LOBBY), id="label_title")
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


				with Collapsible(title = "RENDERMAN PRO SERVER PATH", id="collapsible_rendermanproserver"):
					
					self.input_proserverpath = Input(placeholder = "Renderman ProServer path")
					yield self.input_proserverpath

					yield Button("Automatic ProServer Search", id="button_proserver")

				yield Button("CHECK INPUT SEQUENCE", id="button_checkinput")
				#yield Button("TEST", id="button_test")

				self.listview_sequence = ListView(id="listview_sequence")
				yield self.listview_sequence
				self.listview_sequence.border_title = "Sequence List"

				with Horizontal(id="horizontal_denoisesettings_container"):
					with Vertical(id="vertical_channelcontainer"):
						self.selectionlist_channels = SelectionList(id="selectionlist_channels")
						yield self.selectionlist_channels
						self.selectionlist_channels.border_title = "Channel List"
					with Vertical(id="vertical_denoisesettingscontainer"):



						self.listview_compression = ListView(id="listview_compression")
						yield self.listview_compression
						self.listview_compression.border_title = "Compression Mode List"


						yield Button("DENOISE", id="button_denoise")
				





			with VerticalScroll(id="verticalscroll_rightcolumn_main"):

				self.plotext_size = PlotextPlot(id="plotext_size")
				yield self.plotext_size

				self.plotext_size.visible = False
				self.plotext_size.styles.height = 0

				self.listview_log = ListView(id="listview_log")
				yield self.listview_log








	def on_mount(self) -> None:

		#display all colors in theme

		
		for line in config.WELCOME.splitlines():
			self.display_notification_function(line, False)


		for compression_mode in COMPRESSION_ALGORYTHM:
			self.listview_compression.append(ListItem(Label(compression_mode)))

		self.listview_compression.index = 0



		self.load_personnal_settings_function()


		self.display_success_function("TUI Built successfully")


		#loading themes
		for theme in THEME_REGISTRY:
			self.register_theme(theme)
		#apply the theme specified in config file
		self.theme = "abyss"










	def on_button_pressed(self, event: Button.Pressed) -> None:

		if event.button.id == "button_proserver":
			self.find_renderman_proserver_function()


		if event.button.id == "button_checkinput":

			#self.check_input_sequence_function()
			#START THE FUNCTION AS A THREAD?

			self.thread_check_input = threading.Thread(target=self.check_input_sequence_function, daemon=True,args=())
			self.thread_check_input.start()

			#self.thread_check_if_alive = threading.Thread(target=self.check_thread_alive_function, daemon=True, args=(self.thread_check_input))


		if event.button.id == "button_test":
			self.update_plotext(["bonjour","bonsoir"], [10, 20])


		if event.button.id == "button_denoise":
			"""

			self.thread_create_config = threading.Thread(target=self.create_config_function, daemon=True,args=())
			self.thread_create_config.start()
			"""
			with self.suspend():

				"""
				DENOISING STEPS
				(if checked)

				- denoise

				compress render
					- create alpha copy
					- use combine script from renderman

				remove useless channels from final sequence
				"""
				self.create_config_function()
				#self.create_alpha_copy_function()





	def on_collapsible_expanded(self, event: Collapsible.Expanded) -> None:

		#set a default color (white?)
		color = "white"
		#get the primary color of the current theme
		for theme in THEME_REGISTRY:
			if theme.name == self.theme:
				color = theme.primary
				self.display_message_function(color)
		value = self.query_one("#%s"%event.control.id)
		value.styles.border = ("vkey",color)
	

	def on_collapsible_collapsed(self, event: Collapsible.Collapsed) -> None:
		color = "white"
		#get the primary color of the current theme
		for theme in THEME_REGISTRY:
			if theme.name == self.theme:
				color = theme.background
				self.display_message_function(color)
		value = self.query_one("#%s"%event.control.id)
		value.styles.border = ("hkey", color)



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


	def on_selection_list_selection_toggled(self, event: SelectionList.SelectionToggled) -> None:
		if event.control.id == "selectionlist_channels":
			#self.display_message_function(event.selection_index)
			#update the value in the channel dictionnary for that sequence
			sequence_name = list(self.FINAL_SEQUENCE_DICTIONNARY.keys())[self.listview_sequence.index]
			sequence_data = self.FINAL_SEQUENCE_DICTIONNARY[sequence_name]

			channel_list = sequence_data["CHANNEL_LIST"]
			channel_list[event.selection_index] = (channel_list[event.selection_index][0], not channel_list[event.selection_index][1])

			sequence_data["CHANNEL_LIST"] = channel_list
			self.FINAL_SEQUENCE_DICTIONNARY[sequence_name] = sequence_data



	def on_list_view_selected(self, event: ListView.Selected) -> None:
		if event.control.id == "listview_compression":
			self.display_message_function("Compression mode changed : %s"%list(COMPRESSION_ALGORYTHM.keys())[self.listview_compression.index])

			user_config = {}

			if os.path.isfile(os.path.join(os.getcwd(), "config/user_config.json"))==True:
				#load user config
				try:
					with open(os.path.join(os.getcwd(), "config/user_config.json"), "r") as read_file:
						user_config = json.load(read_file)
				except Exception as e:
					self.display_error_function("Impossible to load user config")
					self.display_error_function(e)
				
			

			user_config["COMPRESSION_MODE"] = list(COMPRESSION_ALGORYTHM.keys())[self.listview_compression.index]

			#save the new config
			try:
				with open(os.path.join(os.getcwd(), "config/user_config.json"), "w") as save_file:
					json.dump(user_config, save_file, indent=4)
			except Exception as e:
				self.display_error_function("Impossible to save config file")
				self.display_error_function(e)
			

		if event.control.id == "listview_sequence":
			sequence_data = self.FINAL_SEQUENCE_DICTIONNARY[list(self.FINAL_SEQUENCE_DICTIONNARY.keys())[self.listview_sequence.index]]

			try:
				self.update_plotext(sequence_data["FRAME_INDEX_LIST"], sequence_data["FRAME_SIZE_LIST"])
			except Exception as e:
				tb = traceback.format_exc()  # Retourne l'exception complète sous forme de chaîne

				# Extraire l'information sur la dernière ligne où l'erreur s'est produite
				last_traceback = traceback.extract_tb(e.__traceback__)[-1]
				file_name = last_traceback.filename
				line_number = last_traceback.lineno
				line_content = last_traceback.line
				
				self.display_error_function("Error happened while updating plotext")
				self.display_error_function("%s\n%s\n%s"%(file_name, line_number, line_content), False)
				#self.update_plotext(self.FINAL_SEQUENCE_DICTIONNARY["FRAME_INDEX_LIST"], self.FINAL_SEQUENCE_DICTIONNARY["FRAME_SIZE_LIST"])
			else:
				self.display_success_function("Plotext updated")

			try:
				#clear selection list
				self.selectionlist_channels.clear_options()

		
				for channel in sequence_data["CHANNEL_LIST"]:
				#add new channels to selection list
					self.selectionlist_channels.add_option((channel[0], channel[0], channel[1]))
			except Exception as e:
				self.display_error_function("Error happened while updating channel list")
				self.display_error_function(e)
			else:
				self.display_success_function("Channels list updated")


	def update_plotext(self, title, number):
		self.plotext_size.visible = True 
		self.plotext_size.styles.height = "30%"
		self.listview_log.styles.height = "70%"

		self.display_message_function("called")
		
		self.plt = self.query_one("#plotext_size").plt
		self.plt.clear_data()
		self.plt.bar(title,number)
		self.plt.xlim(min(title),max(title)*1.5)
		self.plt.ylim(0,max(number)*1.5)
		self.plt.show()

		self.plotext_size.refresh()

		self.display_message_function("done")



	def update_sequencelist(self):
		#clear the sequence list
		self.listview_sequence.clear()


	
		for sequence_name in self.FINAL_SEQUENCE_DICTIONNARY:
			self.listview_sequence.append(ListItem(Label(sequence_name)))
		
		
			




if __name__ == "__main__":
	App = RMD_APP()
	App.run()

