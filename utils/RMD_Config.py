# -*- coding: utf-8 -*-



import os
import sys
import json
import OpenEXR
import traceback


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


	def find_renderman_proserver_function(self):
		if os.path.isdir("C:/Program Files/Pixar")==False:
			self.display_error_function("Impossible to find Pixar folder!")
			return
		else:
			proserver_list = []

			for item in os.listdir("C:/Program Files/Pixar"):
				if os.path.isdir(os.path.join("C:/Program Files/Pixar", item))==True and (item.startswith("RenderManProServer")):
					proserver_list.append(os.path.join("C:/Program Files/Pixar", item))
			if len(proserver_list) != 0:
				self.display_success_function("Last proserver version : %s"%proserver_list[-1])
			else:
				self.display_error_function("Impossible to find proserver version")
				return

			if os.path.isfile(os.path.join(os.getcwd(), "config/user_config.json"))==False:
				#create the new folder
				os.makedirs(os.path.join(os.getcwd(), "config"), exist_ok=True)

				user_config = {}
				

			else:
				#read the file
				try:
					with open(os.path.join(os.getcwd(), "config/user_config.json"), "r") as read_file:
						user_config = json.load(read_file)
				except Exception as e:
					self.display_error_function("Impossible to read user config file!")
					self.display_error_function(e)
					return

			user_config["RENDERMAN_PROSERVER"] = proserver_list[-1]

			#save the new file
			try:
				with open(os.path.join(os.getcwd(), "config/user_config.json"), "w") as save_file:
					json.dump(user_config,save_file, indent=4)

			except Exception as e:
				self.display_error_function("Impossible to save user file")
				self.display_error_function(e)
			else:
				self.display_success_function("User config saved")

			#change the textfield content
			#self.input_proserverpath.clear()
			self.input_proserverpath.value = str(user_config["RENDERMAN_PROSERVER"])











	def load_personnal_settings_function(self):
		if os.path.isfile(os.path.join(os.getcwd(), "config/user_config.json"))==True:
			try:
				with open(os.path.join(os.getcwd(), "config/user_config.json"), "r") as read_file:
					user_config = json.load(read_file)

			except Exception as e:
				self.display_error_function("Impossible to load user config file")
				self.display_error_function(e)
				return

			else:
				self.display_success_function("User config loaded")


			if "RENDERMAN_PROSERVER" in user_config:
				self.input_proserverpath.value = user_config["RENDERMAN_PROSERVER"]

			if "COMPRESSION_MODE" in user_config:
				self.listview_compression.index = list(COMPRESSION_ALGORYTHM.keys()).index(user_config["COMPRESSION_MODE"])
				self.display_notification_function("Compression mode loaded : %s"%user_config["COMPRESSION_MODE"])



				














	def create_config_function(self):
		crossframe_value = True
		self.CONFIG_LIST = []
		
		try:
			#self.display_message_function, "\n\n", False)
			#self.display_notification_function, "CALLING JSON CONFIG FUNCTION")
			self.display_notification_function("CALLING JSON CONFIG FUNCTION")

			if self.FINAL_SEQUENCE_DICTIONNARY == {}:
				self.display_error_function("Sequence dictionnary is empty")
				os.system("pause")
				return 

			if (os.path.isdir(self.output_path)==False):
				self.display_warning_function("Output path not existing")

				try:
					os.makedirs(self.output_path, exist_ok=True)
				except Exception as e:
					self.display_error_function("Impossible to create output path")
					self.display_error_function(e)
				else:
					self.display_success_function("Output path folder created")

			
			
			for sequence_name, sequence_data in self.FINAL_SEQUENCE_DICTIONNARY.items():
				#create the final aov list from true value
				final_sequence_channel_list = []

				
				self.display_notification_function("Creating json config for sequence : %s"%sequence_name)

				for channel in sequence_data["CHANNEL_LIST"]:
					#if channel[1] == True:
					final_sequence_channel_list.append(channel[0])
					self.display_message_function("  %s"%channel[0], False)


				config_dictionnary = {}
				aux_dictionnary = {}
				added_list = []


				for channel_name, keyword_list in AOV_KEYWORD.items():

					general_dictionnary = {}
					path = []
					layers = []

					for keyword in keyword_list:
						for aov in final_sequence_channel_list:
							if len(list(keyword)) > 3:
								if keyword in aov:
									if aov not in layers:
										layers.append(aov)

									if aov not in added_list:
										added_list.append(aov)

							else:
								if keyword == aov:
									if aov not in layers:
										layers.append(aov)

									if aov not in added_list:
										added_list.append(aov)
					general_dictionnary["paths"] = sequence_data["FRAME_LIST"]
					general_dictionnary["layers"] = layers

					aux_dictionnary[channel_name] = [general_dictionnary]

				for channel in final_sequence_channel_list:
					if channel not in added_list:
						self.display_error_function("  Aov not writen in .json config : %s"%channel)

				config_dictionnary["primary"] = sequence_data["FRAME_LIST"]
				config_dictionnary["aux"] = aux_dictionnary

				if crossframe_value == True:
					config_dictionnary["config"] = {
						"asymmetry": 0.0,
						"flow": False,
						"debug": False,
						"output-dir": self.output_path,
						"passes": [
							"albedo",
							"color",
							"specular",
							"diffuse",
						],
						"parameters": "%s/lib/denoise/20970-renderman.param"%PIXAR_PATH,
						"topology": "%s/lib/denoise/full_w7_4sv2_sym_gen2.topo"%PIXAR_PATH
					}
				else:
					config_dictionnary["config"] = {
						"asymmetry": 0.0,
						"flow": False,
						"debug": False,
						"output-dir": self.output_path,
						"passes": [
							"albedo",
							"color",
							"specular",
							"diffuse",
						],
						"parameters": "%s/lib/denoise/20973-renderman.param"%PIXAR_PATH,
						"topology": "%s/lib/denoise/full_w1_5s_sym_gen2.topo"%PIXAR_PATH
					}

				self.display_success_function("   Dictionnary created for sequence")

				try:
					if os.path.isdir(os.path.join(os.getcwd(), "config"))==False:
						os.mkdir(os.path.join(os.getcwd(), "config"))

					config_path = os.path.join(os.getcwd(), "config/config_%s.json"%sequence_name)
				except Exception as e:
					self.display_error_function(e)
				try:
					with open(config_path, "w") as save_config:
						json.dump(config_dictionnary, save_config, indent=4)
				except Exception as e:
					self.display_error_function("    Impossible to save json file")
					self.display_error_function("    %s"%e)
				else:
					self.display_success_function("    Json file created for sequence : %s"%sequence_name)
					self.display_success_function("    %s"%config_path)

					#UPDATE THE CONFIG LIST
					self.CONFIG_LIST.append(config_path)






						


			self.display_success_function("DONE CREATING CONFIG FILE")





		except Exception as e:
			tb = traceback.format_exc()

			last_traceback = traceback.extract_tb(e.__traceback__)[-1]
			file_name = last_traceback.filename
			line_number = last_traceback.lineno
			line_content = last_traceback.line
			
			self.display_error_function("Error happened while creating config")
			self.display_error_function("%s\n%s\n%s\n%s"%(file_name,line_number,line_content,e), False)




		self.denoise_function()

		os.system("pause")