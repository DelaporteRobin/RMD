# -*- coding: utf-8 -*-



import os
import sys
import json
import OpenEXR
import traceback
import pyfiglet
import shutil


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



		#self.display_notification_function("CALLING DENOISE FUNCTION")
		self.display_notification_function(pyfiglet.figlet_format("RMD DENOISE", font=ASCII_FONT_TERMINAL), False)


		for sequence_name, sequence_data in self.FINAL_SEQUENCE_DICTIONNARY.items():
			if os.path.isfile(os.path.join(os.getcwd(), "config/config_%s.json"%sequence_name)):
				self.display_success_function("CONFIG FOUND FOR %s"%sequence_name)
			else:
				self.display_error_function("CONFIG NOT FOUND FOR %s"%sequence_name)
				continue


			self.display_notification_function("LAUNCHING DENOISE TASK FOR %s"%sequence_name.upper())
			try:
				print("Launching Renderman Command")
				os.system('"%s/bin/denoise_batch.exe" -j %s' % (PIXAR_PATH, os.path.join(os.getcwd(), "config/config_%s.json"%sequence_name)))
			except Exception as e:
				self.display_error_function("Impossible to call denoising process")
				self.display_error_function(e)
			else:
				


				self.create_alpha_copy_function(sequence_name, sequence_data)
				self.combine_exr_function(sequence_name, sequence_data)
				self.combine_alpha_with_sequence_function(sequence_name, sequence_data)
				self.remove_useless_channels_function(sequence_name, sequence_data)
				self.clean_output_folder_function()


				self.display_success_function("Task done")






	def create_alpha_copy_function(self, sequence_name, sequence_data):
		self.ALPHA_SEQUENCE_LIST = []

		self.display_message_function("\n\n\n", False)
		self.display_notification_function("EXTRACTING ALPHA FROM INPUT SEQUENCE : %s"%sequence_name)

		#create alpha folder
		try:
			os.makedirs(os.path.join(self.output_path, "input_alpha"), exist_ok=True)
		except Exception as e:
			self.display_error_function("Impossible to create input alpha folder")
			return
		else:
			self.display_success_function("Input alpha folder created")
			self.display_success_function(os.path.join(self.output_path, "input_alpha"))

			for file in sequence_data["FRAME_LIST"]:
				self.display_message_function("\n",False)
				self.display_notification_function("Trying to extract alpha from %s"%file)
				output_file = os.path.join(self.output_path, "input_alpha/%s"%os.path.basename(file))
				value = self.remove_channel_function(file, output_file, ["a", "A"], False)
				if value == True:
					self.display_success_function("Alpha extracted")
					self.display_success_function("File writen : %s"%output_file)
					self.ALPHA_SEQUENCE_LIST.append(output_file)
				else:
					self.display_error_function("Impossible to extract alpha")







	def remove_channel_function(self, file, output_file, remove_list, value=False):
		self.display_message_function("\n", False)
		self.display_message_function("Removing channels : %s"%remove_list)

		try:

			#if value == False -> delete all channels not in list
			#if value == True -> delete all channels in list
			exr_file = OpenEXR.InputFile(file)
			header = exr_file.header()
			header["compression"] = Imath.Compression(COMPRESSION_ALGORYTHM[self.COMPRESSION_MODE])
			self.display_message_function("Compression type changed : %s"%self.COMPRESSION_MODE)
			channels = header["channels"]
			channel_list = list(channels.keys())

			for channel in channel_list:
				found=False

				if value==False:
					if channel.split(".")[0] not in remove_list:
						found=True


				if value==True:
					
					for remove in remove_list:
						if remove == channel.split(".")[0]:
							found=True
							break

				if found==True:
					try:
						channels.pop(channel)
					except:
						self.display_error_function("Failed to remove channel : %s"%channel)
					else:
						self.display_message_function("Channel removed : %s"%channel)

			new_dict = {}
			for ch in header["channels"]:
				new_dict[ch] = exr_file.channel(ch)
			exr_file.close()

			exr = OpenEXR.OutputFile(output_file, header)
			exr.writePixels(new_dict)
			exr.close()
		except:
			self.display_error_function("Error trying to remove channel from file: %s"%file)
			return False 
		else:
			
			return True








	def combine_exr_function(self, sequence_name, sequence_data):

		self.display_message_function("\n\n\n", False)
		self.display_notification_function("COMBINING .EXR FILES")


		self.COMBINED_SEQUENCE_LIST = []

		combined_sequence_data = {}
		render_file_list = []
		render_folder_list = []

		frame_data = {}
		combined_frame_data = {}


		for element in os.listdir(self.output_path):
			#print(os.path.join(self.output_path, element))
			if os.path.isfile(os.path.join(self.output_path,element))==True:
				render_file_list.append(os.path.join(self.output_path,element))

			elif os.path.isdir(os.path.join(self.output_path, element))==True:
				render_folder_list.append(os.path.join(self.output_path,element))

		i=0
		while True:
			
			if os.path.isdir("%s/Denoised_%s_%s"%(self.output_path, sequence_name, str(i)))==False:
				os.mkdir("%s/Denoised_%s_%s"%(self.output_path, sequence_name, str(i)))
				combined_path = "%s/Denoised_%s_%s"%(self.output_path, sequence_name, str(i))
				break
			else:
				i+=1

		self.display_notification_function("Ouput folder created : %s"%combined_path)


		for render in render_file_list:
			self.display_message_function("\n", False)
			self.display_notification_function("Creating combination list : %s"%render)
			combination_list = [render]

			for folder in render_folder_list:
				if (os.path.isfile(os.path.join(folder, os.path.basename(render)))==True) and (os.path.join(folder, os.path.basename(folder)) not in combination_list):
					combination_list.append(os.path.join(folder, os.path.basename(render)))
					self.display_message_function("		Render added to combination list : %s"%os.path.join(folder, os.path.basename(render)), False)





			self.display_notification_function("Creating Shell Combination command")
			command = ""
			for item in combination_list:
				command = "%s %s"%(command,item)
			command = '"%s/bin/exrmerge.exe" %s %s/Denoised_%s' % (PIXAR_PATH, command, combined_path, os.path.basename(render))
			self.display_message_function("Command built successfully")
			self.display_message_function("%s"%command, False)

			try:
				os.system(command)
			except Exception as e:
				self.display_error_function("Impossible to execute Combination command")
				self.display_error_fucntion(e)
			else:
				self.display_success_function("Command executed successfully")

			if os.path.isfile("%s/Denoised_%s"%(combined_path, os.path.basename(render)))==False:
				self.display_error_function("Impossible to combine render : %s"%os.path.basename(render))
			else:
				self.display_success_function("Combination done successfully : %s"%os.path.basename(render))
				self.COMBINED_SEQUENCE_LIST.append("%s/Denoised_%s"%(combined_path, os.path.basename(render)))

		self.display_message_function("\n", False)
		self.display_success_function("COMBINATION FUNCTION DONE")







	def combine_alpha_with_sequence_function(self, sequence_name, sequence_data):
		self.display_message_function("\n", False)
		self.display_notification_function("COMBINE ALPHA WITH SEQUENCE FUNCTION")

		if len(self.COMBINED_SEQUENCE_LIST)==0 or len(self.ALPHA_SEQUENCE_LIST) == 0:
			self.display_error_function("Impossible to combine alpha sequence with denoised sequence")
			return 
		if len(self.COMBINED_SEQUENCE_LIST) != len(self.ALPHA_SEQUENCE_LIST):
			self.display_error_function("Alpha list length is different from Denoised list length!")
			return


		for i in range(len(self.COMBINED_SEQUENCE_LIST)):
			self.display_message_function("Combining alpha with denoised : ")
			self.display_message_function("	%s"%self.COMBINED_SEQUENCE_LIST[i], False)
			self.display_message_function("	%s"%self.ALPHA_SEQUENCE_LIST[i], False)

			try:
				command = '"%s/bin/exrmerge.exr" %s %s' % (PIXAR_PATH, self.COMBINED_SEQUENCE_LIST[i], self.ALPHA_SEQUENCE_LIST[i])
			except Exception as e:
				self.display_error_function("Impossible to combine alpha with denoised sequence")
				self.display_error_function(e)
			else:
				self.display_success_function("Alpha combined with denoised sequence")

		self.display_message_function("\n", False)
		self.display_success_function("COMBINE ALPHA WITH SEQUENCE DONE")





	def remove_useless_channels_function(self, sequence_name, sequence_data):
		self.display_message_function("\n", False)
		self.display_notification_function("REMOVE USELESS CHANNELS FUNCTION")



		for file in self.COMBINED_SEQUENCE_LIST:
			self.display_notification_function("Removing useless channels for %s"%file)
			for channel in sequence_data["CHANNEL_LIST"]:
				if channel[1] == False:
					#call the remove channel function
					value = self.remove_channel_function(file, file, [channel[0]], True)

		self.display_success_function("USELESS CHANNELS REMOVED FROM SEQUENCE")






	def clean_output_folder_function(self):
		output_folder_content = os.listdir(self.output_path)

		self.display_message_function("\n", False)
		self.display_notification_function("CLEANING OUTPUT FOLDER")

		for item in output_folder_content:
			if os.path.isfile(os.path.join(self.output_path, item))==True:
				try:
					os.remove(os.path.join(self.output_path, item))
				except Exception as e:
					self.display_warning_function("Impossible to remove file : %s"%item)
					self.display_warning_function("  %s"%e)
				else:
					self.display_success_function("File removed : %s"%item)

			if (os.path.isdir(os.path.join(self.output_path, item))==True) and (item.startswith("Denoised")==False):
				try:
					shutil.rmtree(os.path.join(self.output_path, item))
				except Exception as e:
					self.display_warning_function("Impossible to remove folder : %s"%item)
					self.display_warning_function("  %s"%e)
				else:
					self.display_success_function("Folder removed : %s"%item)


		self.display_success_function("OUTPUT FOLDER CLEANED")



				



