import importlib.util 
import os
import sys



package_list = ["pathlib", "json", "textual", "pyfiglet", "datetime", "termcolor", "Imath", "asciichartpy", "plotext", "threading", "json", "colorama", "OpenEXR", "subprocess", "time", "numpy"]


print("Checking packages...")

for package in package_list:
	spec = importlib.util.find_spec(package)
	if spec == None:
		print("INSTALLING %s"%package)
		os.system("python -m pip install %s"%package)



from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.screen import Screen 
from textual import events
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual import on


from DenoiserJson import DenoiseCore
from datetime import datetime
from pyfiglet import Figlet 
from time import sleep
from datetime import datetime
from termcolor import *

import copy
import Imath
import asciichartpy as acp
import plotext as plt
import threading

import json 
import colorama
import OpenEXR
colorama.init()








class RMD_Application(App[None], DenoiseCore):
	
	CSS_PATH = [os.path.join(os.getcwd(),"data/style/style_global.tcss"), os.path.join(os.getcwd(), "data/style/style_v2.tcss")]






	def __init__(self):
		super().__init__()

		self.font_title = Figlet(font="bloody")
		self.font_subtitle = Figlet(font="digital")


		#create an instance of the denoise core class
		"""
		try:
			self.dt = DenoiseCore()
		except:
			print(colored("Impossible to load module", "red"))
			return
		"""
		#print(os.getcwd())
		self.config_path = os.path.join(os.getcwd(),"data/final_config.json")

		#get the path of the current drive root
		self.starting_path = Path("/")

		self.program_log = []
		self.old_log = []

		self.program_path = os.getcwd()

		self.sequence_path = None
		self.output_path = None

		self.exr_list = []
		self.required_aov = None
		self.input_channel_list = []
		self.channel_selection_name = []
		self.channel_selection = []

		self.min_frame = "1001"
		self.max_frame = "1010"
		

		self.compression_mode_list = {
			"DWAB_COMPRESSION":Imath.Compression.DWAB_COMPRESSION,
			"RLE_COMPRESSION":Imath.Compression.RLE_COMPRESSION,
			"ZIP_COMPRESSION":Imath.Compression.ZIP_COMPRESSION,
			"ZIPS_COMPRESSION":Imath.Compression.ZIPS_COMPRESSION,
			"PIZ_COMPRESSION":Imath.Compression.PIZ_COMPRESSION,
			"PXR24_COMPRESSION":Imath.Compression.PXR24_COMPRESSION,
			"B44_COMPRESSION":Imath.Compression.B44_COMPRESSION,
			"B44A_COMPRESSION":Imath.Compression.B44A_COMPRESSION,
			"DWAA_COMPRESSION":Imath.Compression.DWAA_COMPRESSION,
			"DWAB_COMPRESSION": Imath.Compression.DWAB_COMPRESSION,	
		}
		self.compression_mode = "ZIPS_COMPRESSION"

		self.settings = {
			"CrossFrame":True,
			"CombineFinalRenders":True,
			"CompressAfterRender":True,
			"RemoveDenoiseChannels":True,
		}
		self.data = {
			"DenoiseStart":None,
			"DenoiseEnd":None,
			"DenoiseTime":None,
			"CombinedSequenceTime":None,
			"CombinedSequence": None,
			"CombinedSequenceData": None,
			"CombinedWithoutUseless":None
		}

		





	def load_settings_function(self):
		try:
			with open(os.path.join(os.getcwd(), "data/RMD_Config.json"), "r") as read_file:
				self.config = json.load(read_file)
		except:
			self.display_error_function("Impossible to open settings file")
			self.config = self.create_settings_function()
			self.display_message_function("Settings created")
		else:
			self.display_message_function("Settings loaded")

	def save_log_function(self, line):
		with open(os.path.join(os.getcwd(), "data/log.dll"), "a") as save_file:
			save_file.write(line)

	def display_notification_function(self, message):
		self.notify(message, severity="warningcls", timeout=5)
		print(colored(message, "cyan"))
		self.program_log.append("[%s] - STATUS : %s"%(str(datetime.now()), message))
		self.save_log_function("[%s] - STATUS : %s\n"%(str(datetime.now()), message))

	def display_error_function(self, message):
		self.notify(message, severity="Error", timeout=5)
		print(colored(message, "red"))
		self.program_log.append("[%s] - ERROR : %s"%(str(datetime.now()), message))
		self.save_log_function("[%s] - ERROR : %s\n"%(str(datetime.now()), message))

	def display_success_function(self, message):
		self.notify(message, timeout=5)
		print(colored(message, "white"))
		self.program_log.append("[%s] - MESSAGE : %s"%(str(datetime.now()), message))
		self.save_log_function("[%s] - MESSAGE : %s\n"%(str(datetime.now()), message))

	def display_message_function(self, message):
		self.notify(message, severity = "information", timeout=5)
		print(colored(message, "green"))
		self.program_log.append("[%s] - SUCCESS : %s"%(str(datetime.now()), message))
		self.save_log_function("[%s] - SUCCESS : %s\n"%(str(datetime.now()), message))


	def create_settings_function(self):
		config = {
			"RendermanPath": "C:/Program Files/Pixar/RenderManProServer-25.2",
			"RequiredAOV": [
				"Ci",
				"sampleCount",
				"mse",
				"albedo",
				"albedo_var",
				"albedo_mse",
				"diffuse",
				"diffuse_mse",
				"specular",
				"specular_mse",
				"zfiltered",
				"zfiltered_var",
				"normal",
				"normal_var",
				"normal_mse",
				"forward",
				"backward",
				"a",
			],
			"DodgeList":[],
			"AOVToRemove": [
				"albedo_var",
				"mse",
				"sampleCount",
				"albedo",
				"albedo_var",
				"albedo_mse",
				"diffuse_mse",
				"specular_mse",
				"zfiltered",
				"zfiltered_var",
				"normal_var",
				"normal_mse"
			],
			"DenoisePasses" : ["albedo", "color", "specular", "diffuse"],
			"DenoiseKeywords": {
				"a": ["a"],
				"albedo":["albedo", "albedo_var", "albedo_mse"],
				"diffuse": ["diffuse","Diffuse","diffuse_mse","normal","forward","backward"],
				"specular": ["specular","Specular", "specular_mse"],
				"color": ["beauty","Ci","subsurface","glass","Glass","transmissive"],
				"sampleCount":["sampleCount"],
				"mse": ["mse"],
				"zfiltered": ["zfiltered"],
				"zfiltered_var": ["zfiltered_var"],
				"normal_var":["normal_var"],
				"normal_mse":["normal_mse"],
			}
		}
		try:
			with open(os.path.join(os.getcwd(), "data/RMD_Config.json"), "w") as save_file:
				json.dump(config, save_file, indent=4)
		except:
			self.display_error_function("Impossible to export settings")
			return None
		else:
			self.display_message_function("Settings exported")
			return config



	


	def compose(self) -> ComposeResult:
		yield Header(show_clock=True)



		with Horizontal(classes="main_application_container"):
			with VerticalScroll(classes="main_leftcolumn", id="main_leftcolumn"):
				yield Label(self.font_title.renderText("RMD Core"), classes="main_title")

				with Collapsible(classes="collapse_left_top", title="Input/Output", collapsed=True):
					
					with Horizontal(classes="input_output_container"):
						with VerticalScroll(classes="input_container"):
							self.explorer_input_sequence = DirectoryTree(self.starting_path, id="input_explorer", classes="dir_explorer_t1")
							self.explorer_input_sequence.border_title = "Input sequence folder"
							self.static_input_sequence = Static()
							yield self.explorer_input_sequence
							yield self.static_input_sequence

						with VerticalScroll(classes="output_container"):
							self.explorer_output_sequence = DirectoryTree(self.starting_path, id="output_explorer", classes="dir_explorer_t1")
							self.explorer_output_sequence.border_title = "Output sequence folder"
							self.static_output_sequence = Static()

						
							yield self.explorer_output_sequence
							yield self.static_output_sequence

					"""
					with Horizontal(classes="input_output_container"):
						with Vertical(classes="input_container"):
							self.explorer_input_sequence = DirectoryTree(self.starting_path, id="input_explorer", classes="dir_explorer_t1")
							self.explorer_input_sequence.border_title = "Input sequence folder"
							self.static_input_sequence = Static()

						with Vertical(classes="output_container"):
							self.explorer_output_sequence = DirectoryTree(self.starting_path, id="output_explorer", classes="dir_explorer_t1")
							self.explorer_output_sequence.border_title = "Output sequence folder"
							self.static_output_sequence = Static()

					yield self.explorer_input_sequence
					yield self.static_input_sequence
					
					
					yield self.explorer_output_sequence
					yield self.static_output_sequence
					"""


				with Collapsible(classes="collapse_left_bot", title="Denoiser Settings", collapsed=True):
					self.frame_range_checkbox = Checkbox("Frame range", value=False, id="frame_range_checkbox")
					yield self.frame_range_checkbox
					with Horizontal(classes="container_range"):
						self.starting_frame_input = Input(disabled=True,placeholder="Starting frame", type="integer", value=self.min_frame, classes="input_range", id="min_frame")
						self.ending_frame_input = Input(disabled=True,placeholder="Ending frame", type="integer", value=self.max_frame, classes="input_range", id="max_frame")	
						yield self.starting_frame_input
						yield self.ending_frame_input
					with Horizontal(classes="container_t2"):
						with Vertical(classes="container_channel_list"):

							


							yield Button("Check input sequence", classes="button_t1", id="button_input_check")
							#self.static_input_channels = Static("INPUT CHANNELS", classes="indicator_t1")
							self.selection_input_channels = SelectionList(id = "channel_list")


							#yield self.static_input_channels
							yield self.selection_input_channels

						with VerticalScroll(classes="main_container_denoise_settings"):
							
							
							yield Checkbox("Crossframe",True, id="CrossFrame")
							yield Checkbox("Combine Renders",True, id="CombineFinalRenders")
							yield Checkbox("Remove channels",True, id="RemoveDenoiseChannels")
								
						


							self.compression_selection_list = OptionList(id="selection_compression_mode")
							for key in self.compression_mode_list.keys():
								if key == self.compression_mode:
									self.compression_selection_list.add_option(Option(key,))
								self.compression_selection_list.add_option(Option(key))
								
							yield self.compression_selection_list
							self.compression_selection_list.highlighted = 1
							self.compression_selection_list.action_select()

							yield Button("Custom compress", id="only_compress_button")
							yield Button("Combine output content", id="only_combine_button")
							yield Button("Reinject alpha", id="reinject_alpha_button")

					
					yield Button("LAUNCH DENOISE", classes="button_t1", id="button_launch_denoiser")
					#yield Button("Remove", classes="remove_button", id="remove_button")



			with VerticalScroll(classes="main_rightcolumn"):
				#with Collapsible(title="LOGS"):
	
				self.main_page_log = Log(classes="log_t1")
				yield self.main_page_log

				"""
				with Collapsible(title="STATS"):
					self.stats_log = Log(classes="log_t2")
					yield self.stats_log
				"""
				

			"""
			with Collapsible(collapsed=False):
				self.main_page_log = Log(classes="log_t1")
				yield self.main_page_log
			with Collapsible(collapsed=True):
				self.log_stats = Log(classes="log_t2")
				yield self.log_stats
			"""



		self.load_settings_function()
		self.required_aov = self.config["RequiredAOV"]

		self.listen_thread = threading.Thread(target=self.thread_function, args=(), daemon=True)
		self.listen_thread.start()


	def on_mount(self) -> None:
		self.title = "RMD - By Quazar"







	def thread_function(self):
		self.notify("Observer launched", timeout=3)
		while True:
			if self.old_log != self.program_log:
				self.main_page_log.clear()
				self.main_page_log.write_lines(self.program_log)
				
				#use copy to udpate old log list value
				self.old_log = copy.copy(self.program_log)


			sleep(2)



	def on_input_changed(self, event:Input.Changed) -> None:
		if event.input.id == "min_frame":
			if str(self.query_one("#min_frame").value).isdigit() == False:
				self.min_frame = 0
			else:
				self.min_frame = self.query_one("#min_frame").value


		if event.input.id == "max_frame":
			if str(self.query_one("#max_frame").value).isdigit() == False:
				#self.display_message_function(str(self.query_one("#max_frame")))
				self.max_frame = 0
			else:
				self.max_frame = self.query_one("#max_frame").value

		#self.display_message_function("%s / %s"%(self.min_frame, self.max_frame))


	def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
		if event.control.id == "input_explorer":
			self.sequence_path = str(event.path)
			self.static_input_sequence.update("INPUT SEQUENCE : %s"%(self.sequence_path))
		if event.control.id == "output_explorer":
			self.output_path = str(event.path)
			self.static_output_sequence.update("OUTPUT PATH : %s"%(self.output_path))






	def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
		value = self.query_one("#%s"%event.checkbox.id).value
		#self.display_message_function("%s : %s"%(event.checkbox.id, str(value)))
		if event.checkbox.id == "frame_range_checkbox":
			self.display_message_function(str(value))
			self.starting_frame_input.disabled = not value
			self.ending_frame_input.disabled = not value
			
		else:
			self.settings[event.checkbox.id] = value


		if event.checkbox.id == "CrossFrame":
			#get the value of the checkbox
			value = self.query_one("#%s"%event.checkbox.id).value 
			self.display_message_function("Crossframe switched to : %s"%value)
			self.settings["CrossFrame"] = value



	def on_option_list_option_selected (self, event: OptionList.OptionMessage) -> None:
		if event.option_list.id == "selection_compression_mode":
			#self.display_message_function(str(event.option_index))
			self.compression_mode = list(self.compression_mode_list.keys())[event.option_index]
			self.display_message_function(self.compression_mode)



			
	def on_button_pressed(self, event: Button.Pressed) -> None:




		if event.button.id == "button_input_check":
			

			#self.check_input_sequence_function()



			
			if (self.sequence_path != None) or (self.output_path != None):


				
			
				self.input_channel_list, size_informations, size_dictionnary = self.check_input_function()

				self.display_message_function("%s\n%s"%(self.font_subtitle.renderText("\nAverage frame size"), "%s\n"%str(size_informations["Average"])))

				if "LowSizeFiles" in size_dictionnary:
					self.display_error_function(self.font_subtitle.renderText("LOW SIZE FILES DETECTED "))
					for key, value in size_informations["LowSizeFiles"].items():
						self.display_message_function("%s : %s" % (key, value))
				else:
					self.display_message_function("No low size frames detected")
				if "NoSizeFiles" in size_dictionnary:
					self.display_error_function(self.font_subtitle.renderText("0 SIZE FILES DETECTED "))
					for key, value in size_informations["NoSizeFiles"].items():
						self.display_message_function("%s : %s" % (key, value))
				else:
					self.display_message_function("No 0 size frames detected")



				
				if self.input_channel_list == False:
					self.display_error_function("Impossible to read channels in file")
				else:
					
				
					self.program_log.append(acp.plot(list(size_dictionnary.values())))
					
					self.selection_input_channels.clear_options()
					for i in range(len(self.input_channel_list)):
						#self.display_message_function(channel_list[i])
						value = [self.input_channel_list[i], i]
						self.selection_input_channels.add_option(Selection(self.input_channel_list[i],i))
						#self.selection_input_channels.add_options((channel_list[i], i))
			else:
				self.display_error_function("You have to define input path!")
			




		if event.button.id == "remove_button":
			self.clean_output_folder_function()






		if event.button.id == "button_launch_denoiser":
			if (self.sequence_path != None) or (self.output_path != None):
				
				self.channel_selection = self.query_one("#channel_list").selected

				self.channel_selection_name = []
				self.alpha_sequence_list = []
				self.combined_sequence_list = []

				for item in self.channel_selection:
					self.channel_selection_name.append(self.input_channel_list[item])
				#generate the json config from the input path


				if (self.sequence_path == None) or (self.output_path == None) or (os.path.isdir(self.output_path)==False) or (os.path.isdir(self.sequence_path)==False):
					self.display_error_function("You must define input and output folder!")
					return
				value = self.create_config_function()

				#return


				if os.path.isdir(value)==True:
					self.display_message_function("Launching denoising process")
					sleep(2)

				if value != False:
					#CALL DENOISE FUNCTION
					#display global informations about denoising process
					self.display_message_function("Denoising Informations : \nInput Path : %s\nOutput Path: %s"%(self.sequence_path, self.output_path))
					with self.suspend():
						try:
							print(colored("LAUNCHING DENOISER", "magenta"))
							os.system('"%s/bin/denoise_batch.exe" -j %s'%(self.config["RendermanPath"], self.config_path))
						except:
							print(colored("Impossible to launch denoise"), "red")
							sleep(2)


						
					
					self.display_message_function("Denoising done")
					

					if self.settings["CombineFinalRenders"] ==True:
						self.create_alpha_copy_function()
						#CALL COMBINE EXR FUNCTION
						self.combine_exr_function()
						

						if self.settings["RemoveDenoiseChannels"] == True:
							self.remove_useless_channels_function()
						self.combine_alpha_with_sequence_function()

						#remove useless content from output folder
						self.clean_output_folder_function()

						self.display_message_function("Denoise done")
						return

				else:
					self.display_error_function("Impossible to launch denoise!")
			else:
				self.display_error_function("You have to define input and output path!")
				return


		if event.button.id in ["only_combine_button", "reinject_alpha_button"]:
			self.display_message_function('Not available for now!')


		if event.button.id == "only_compress_button":
			"""	
			get the input path content
			get the frame range ?
			get the channel to remove list
			for each frame launch the remove useless channels function
			"""


			self.channel_selection = self.query_one("#channel_list").selected
			self.channel_selection_name = []
			for item in self.channel_selection:
				self.channel_selection_name.append(self.input_channel_list[item])


			#get the content of the input path
			if (self.sequence_path == None) or (os.path.isdir(self.sequence_path) == False):
				self.display_error_function("You have to define an Input path first!")
				self.display_error_function("The Input path represent the path of the images you want to compress!")
				return
			else:
				self.combined_sequence_list = []
				content = os.listdir(self.sequence_path)
				for item in content:
					if os.path.isfile(os.path.join(self.sequence_path, item))==True:
						self.combined_sequence_list.append(os.path.join(self.sequence_path, item))
				if len(self.combined_sequence_list) == 0:
					self.display_error_function("No file to compress!")
					return
				#elif len(self.channel_selection_name) == 0:
				#	self.display_error_function("No channel to remove selected!")
				#	return 
				else:
					with self.suspend():

						try:
							self.remove_useless_channels_function()
						except:
							print(colored("Impossible to launch file compression!", "red"))
							sleep(2)

			

			
			



	async def on_key(self, event: events.Key) -> None:
		if event.key == "p":
			self.exit()
		



if __name__ == "__main__":
	app = RMD_Application()
	app.run()
	
