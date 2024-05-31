"""
CREATING JSON CONFIG FILE
passes list : 
	diffuse
	color
	albedo
	specular
	irradiance
	alpha

create config dictionnary from aov in exr
	from each aov in exr determine which channel it is

	define the required channel list to denoise (check that it's in exr file)

	for each aov check if it contains keywords:
		color:
			beauty
		diffuse:
			diffuse
		specular:
			specular
		albedo:
			albedo

"""


from termcolor import *
from datetime import datetime
from time import sleep

import plotext as plt
import threading
import subprocess
import OpenEXR
import Imath
import OpenEXR as exr
import os
import colorama
import json 
import numpy as np
import shutil

colorama.init()





class DenoiseCore():
	def __init__(self, sequence_path= None, output_path=None, display_message = True):

		self.program_log = [
			"\nDENOISE CORE - %s\n%s\n%s"%(str(datetime.now()), output_path, sequence_path)
		]

		self.program_path = os.getcwd()
		#self.config["RendermanPath"] = None

		self.display_message = display_message

		self.informations_log = {}
		#self.sequence_path = sequence_path
		#self.output_path = output_path 



		self.required_aov = [
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
			]

		self.data = {}


		self.delete_other_stuff = True
		self.combined_sequence_list = []
		self.alpha_sequence_list = []
		self.exr_list = []

	




	def denoise_core_check_function(self):
		return True

	"""
	def display_error_function(self,message):
		format_msg = "[ ERROR ] %s : %s"%(str(datetime.now()), message)
		print(colored(format_msg, "red"))
		self.program_log.append("%s\n"%format_msg)

	def display_notification_function(self,message):
		format_msg = "%s : %s"%(str(datetime.now()), message)
		print(colored(format_msg, "yellow"))
		self.program_log.append("%s\n"%format_msg)

	def display_status_function(self, message):
		format_msg = "%s : %s"%(str(datetime.now()), message)
		print(colored(format_msg, "cyan"))
		self.program_log.append("%s\n"%format_msg)

	def display_success_function(self,message):
		format_msg = "[ SUCESS ] %s : %s"%(str(datetime.now()), message)
		print(colored(format_msg, "green"))
		self.program_log.append("%s\n"%format_msg)
	"""




	def save_log_function(self):
		
		with open(os.path.join(self.output_path, "DenoiserCore_LOG.txt"), "a") as save_file:
			for line in self.program_log:
				save_file.write(line)
	
	
		self.display_message_function("LOG SAVED : %s"%os.path.join(self.output_path, "DenoiserCore_LOG.txt"))














	def create_config_function(self):
		#check if the folder path exists
		#print(self.sequence_path)

		#get min and max frames
		#check if the values are correct in order to launch denoising function
		self.display_message_function("%s : %s"%(self.max_frame, self.min_frame))
		if (int(self.max_frame) < int(self.min_frame)):
			self.display_error_function("You must enter a valid frame range!")
			return

		if os.path.isdir(self.sequence_path) == False:
			self.display_error_function("Folder doesn't exist!")
			return

		#list all exr files in folder
		folder_content = os.listdir(self.sequence_path)
		

		for item in folder_content:
			if os.path.isfile(os.path.join(self.sequence_path,item)) == True:
				#print(os.path.splitext(item)[1])
				if (os.path.splitext(item)[1] == ".exr") or (os.path.splitext(item)[1] == ".Exr"):
					if self.query_one("#frame_range_checkbox").value == True:
						#check if the index of the frame is contained in the frame range
						splited_file = os.path.splitext(item)[0].split(".")
						if (len(splited_file) != 2) or (splited_file[1].isdigit()==False):
							self.display_error_function("Impossible to get that frame index: %s"%item)
							return False
						else:
							#check if the frame index is contained in the interval
							frame_index = int(splited_file[1])

							#self.display_message_function("%s ; %s ; %s"%(frame_index, self.min_frame, self.max_frame))
							if (int(frame_index) >= int(self.min_frame)) and (int(frame_index) <= int(self.max_frame)):
								#print(os.path.join(self.sequence_path, item))
								self.exr_list.append(os.path.join(self.sequence_path, item))
					else:
						self.exr_list.append(os.path.join(self.sequence_path, item))
			

		if len(self.exr_list) == 0:
			self.display_message_function("No frame to denoise!")
			return

		#CHECK FOR EACH FILE OF THE EXR LIST THAT THERE IS REQUIRED AOVS
		self.display_message_function("Checking AOV's in .exr files:")
		for file in self.exr_list:
			render_file = exr.InputFile(file)
			render_data = render_file.header()["channels"]

			for aov in self.required_aov:
				exr_aov = []

				#define the list of aovs contained in exr
				for element in list(render_data.keys()):
					if element.split(".")[0] not in exr_aov:
						exr_aov.append(element.split(".")[0])

			#check that all required aovs are in the exr file
			for required_aov in self.required_aov:
				if required_aov not in exr_aov:
					self.display_error_function("REQUIRED AOV MISSING :\nAOV missing : %s\nEXR file : %s"%(required_aov, file))



		




		self.display_message_function("Define the list of AOV to denoise in file : ")
		#LAUNCH CREATIION OF THE JSON DICTIONNARY FROM THE FIRST EXR OF THE SEQUENCE
		#define the list of aovs contained in the first exr 
		#and remove the dodge list from the aov list 
		#then create the json dictionnary
		#print(self.exr_list)
		file = self.exr_list[0]
		file_pass = exr.InputFile(file).header()["channels"]
		file_aov = []


		for aov in list(file_pass.keys()):
			
			in_aov = False


			for dodge in self.config["DodgeList"]:
				if dodge in aov.split(".")[0]:
					in_aov=True
					break

			if (in_aov == False) and (aov.split(".")[0] not in file_aov):
				file_aov.append(aov.split(".")[0])
				print("aov added : %s"%aov.split(".")[0])
					

		

		self.display_message_function("Create Json config dictionnary...\n\n\n")

		
		config_dictionnary = {}
		aux_dictionnary = {}
		added_list = []

		
		
		for key, value in self.config["DenoiseKeywords"].items():
			
			keyword_list = value
			general_dictionnary = {}


			path = []
			layers = []

			for keyword in keyword_list:
				for aov in file_aov:
					#check if the keyword is contained in the aov
					if len(list(keyword)) > 3:
						if keyword in aov:
							if aov not in layers:
								layers.append(aov)

							if aov not in added_list:
								added_list.append(aov)

					#check if the keyword is equal to the aov
					else:
						if keyword == aov:
							if aov not in layers:
								layers.append(aov)

							if aov not in added_list:
								added_list.append(aov)


			general_dictionnary["paths"] = self.exr_list
			general_dictionnary["layers"] = layers

			aux_dictionnary[key] = [general_dictionnary]


		for aov in file_aov:
			if aov not in added_list:
				self.display_error_function("missed aov : %s"%aov)



		#FINISH THE DICTIONNARY WITH FINAL INFORMATIONS
		config_dictionnary["primary"] = self.exr_list
		config_dictionnary["aux"] = aux_dictionnary

		if self.settings["CrossFrame"] == True:
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
				"parameters": "%s/lib/denoise/20970-renderman.param"%self.config["RendermanPath"],
				"topology": "%s/lib/denoise/full_w7_4sv2_sym_gen2.topo"%self.config["RendermanPath"]
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
				"parameters": "%s/lib/denoise/20973-renderman.param"%self.config["RendermanPath"],
				"topology": "%s/lib/denoise/full_w1_5s_sym_gen2.topo"%self.config["RendermanPath"]
			}

		self.display_message_function("Generation of dictionnary done")

		if os.path.isfile(os.path.join(self.program_path, "data/final_config.json"))==True:
			try:
				os.remove(os.path.join(self.program_path, "data/final_config.json"))
				
			except:
				self.display_error_function("Impossible to remove old config")
			else:
				self.display_message_function("Old config removed")
		try:
			with open(os.path.join(self.program_path, "data/final_config.json"), "w") as save_config:
				json.dump(config_dictionnary, save_config, indent=4)
		
		except:
			self.display_error_function("Impossible to save JSON Config file")
			return False
		else:
			self.display_message_function("JSON Config file generated")
			return os.path.join(self.program_path, "data/final_config.json")
		




	def denoise_function(self):

		self.display_message_function("DENOISE FILES")

		

		#, os.path.join(self.program_path, "data/final_config.json")
		if self.settings["CrossFrame"] == False:
			self.display_message_function("Denoise without crossframe engaged")
		else:
			self.display_message_function("Denoise using crossframe engaged")
		try:
			self.display_message_function("Denoising function launched")
			os.system('"%s/bin/denoise_batch.exe" -j %s'%(self.config["RendermanPath"], self.config_path))
		except:
			self.display_error_function("Impossible to denoise")
		else:
			self.display_message_function("Denoise done")
		
		
		#command = ["%s/bin/denoise_batch.exe"%self.config["RendermanPath"], "-cf", "-j", os.path.join(self.program_path, "data/final_config.json"), "-o", self.output_path]

		#print(command)
		#process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		#output, error = process.communicate()
		






	def combine_exr_function(self):

			
			self.display_notification_function("COMBINE EXR FUNCTION")

			combined_sequence_data = {}
			render_file_list = []
			render_folder_list = []

			frame_data = {}
			combined_frame_data = {}

			#print(os.listdir(self.output_path))

			for element in os.listdir(self.output_path):
				#print(os.path.join(self.output_path, element))
				if os.path.isfile(os.path.join(self.output_path,element))==True:
					render_file_list.append(os.path.join(self.output_path,element))

					frame_data[os.path.join(self.output_path, element)] = (os.path.getmtime(os.path.join(self.output_path, element)) - os.path.getctime(os.path.join(self.output_path, element))) / 60
				elif os.path.isdir(os.path.join(self.output_path, element))==True:
					render_folder_list.append(os.path.join(self.output_path,element))


			self.display_notification_function("FOLDER LIST")
			for folder in render_folder_list:
				self.display_message_function(str(folder))
			#print("\n\n\n")

			i=0
			while True:
				if self.query_one("#frame_range_checkbox").value == False:
					if os.path.isdir("%s/Denoised%s"%(self.output_path, str(i)))==False:
						os.mkdir("%s/Denoised%s"%(self.output_path,str(i)))
						combined_path = "%s/Denoised%s"%(self.output_path,str(i))
						break
					else:
						i+=1
				else:
					#get input path folder name

					if os.path.isdir("%s/Denoised_[%s-%s]_%s_%s"%(self.output_path,self.min_frame, self.max_frame, os.path.basename(self.sequence_path),str(i)))==False:
						os.mkdir("%s/Denoised_[%s-%s]_%s_%s"%(self.output_path,self.min_frame, self.max_frame, os.path.basename(self.sequence_path),str(i)))
						combined_path = "%s/Denoised_[%s-%s]_%s_%s"%(self.output_path,self.min_frame, self.max_frame, os.path.basename(self.sequence_path),str(i))
						break
					else:
						i+=1
			self.display_notification_function("Ouput folder created : %s"%combined_path)

			for render in render_file_list:
				self.display_notification_function("CHECKING RENDER : %s"%render)
				combination_list = [render]

				for folder in render_folder_list:
					if (os.path.isfile(os.path.join(folder, os.path.basename(render)))==True) and (os.path.join(folder, os.path.basename(render)) not in combination_list):
						#print("render added %s"%os.path.join(folder, os.path.basename(render)))
						combination_list.append(os.path.join(folder, os.path.basename(render)))
						self.display_message_function("Render added to combining list : %s"%os.path.join(folder, os.path.basename(render)))

				#generate the command to use the renderman script
				#C:\Program Files\Pixar\RenderManProServer-25.2\bin

				command=""
				for item in combination_list:
					command = "%s %s"%(command, item)
				

				start_merge = (datetime.now())

				self.display_message_function("Launching combining command : %s"%command)
				command = '"%s/bin/exrmerge.exe" %s %s/Denoised_%s'%(self.config["RendermanPath"], command, combined_path, os.path.basename(render))
				os.system(command)


				if os.path.isfile("%s/Denoised_%s"%(combined_path, os.path.basename(render))) == False:
					self.display_error_function("Impossible to combine render : %s"%(os.path.basename(render)))
				else:
					self.display_success_function("Combined render created : %s"%(os.path.basename(render)))
					self.combined_sequence_list.append("%s/Denoised_%s"%(combined_path, os.path.basename(render)))

					combined_sequence_data["Denoised_%s"%os.path.basename(render)] = os.stat("%s/Denoised_%s"%(combined_path, os.path.basename(render))).st_size / (1024 * 1024)
				
				combined_frame_data[render] = (os.path.getmtime("%s/Denoised_%s"%(combined_path, os.path.basename(render))) - os.path.getctime("%s/Denoised_%s"%(combined_path, os.path.basename(render)))) / 60
			self.display_message_function("Combination of Main renders done!")

			self.data["CombinedSequenceTime"] = combined_frame_data
			self.data["DenoiseTime"] = frame_data
			self.data["CombinedSequence"] = combined_sequence_data





	def remove_useless_channels_function(self, output_folder = False):
		combined_remove_sequence_data = {}
		for file in self.combined_sequence_list:
			#remove in each file the aovs present in remove useless channel list
			if output_folder == False:
				value = self.remove_channel_function(file, file, self.channel_selection_name, True)
			else:
				value = self.remove_channel_function(file, os.path.join(output_folder, file), self.channel_selection_name,True)
			combined_remove_sequence_data[os.path.basename(file)] = os.stat(file).st_size / (1024 * 1024)
			if value == True:
				self.display_message_function("Useless channel removed from final render : %s"%file)

			else:
				self.display_error_function("Impossible to remove useless channel from final render : %s"%file)
		self.display_message_function("USELESS CHANNELS REMOVED FROM RENDER SEQUENCE")
		self.data["CombinedWithoutUseless"] = combined_remove_sequence_data






	def create_alpha_copy_function(self):
		os.makedirs(os.path.join(self.output_path, "sequence_alpha_folder"), exist_ok=True)
		self.display_message_function("Alpha folder created")

		#for each file of the original sequence
		#call the remove channnel function (with alpha)
		for file in self.exr_list:
			output_file = os.path.join(self.output_path, "sequence_alpha_folder/%s"%os.path.basename(file))
			value = self.remove_channel_function(file, output_file, ["a", "A"], False)
			if value == True:
				self.display_message_function("Alpha extracted in : %s"%self.output_path)
				self.alpha_sequence_list.append(os.path.join(self.output_path,"sequence_alpha_folder/%s"%os.path.basename(file)))
			else:
				self.display_error_function("Impossible to extract alpha from : %s"%file)

		self.display_message_function("ALPHA SEQUENCE CREATED")




	def remove_channel_function(self, file, output_file, remove_list, value=False):
		try:

			#if value == False -> delete all channels not in list
			#if value == True -> delete all channels in list
			exr_file = OpenEXR.InputFile(file)
			header = exr_file.header()
			header["compression"] = Imath.Compression(self.compression_mode_list[self.compression_mode])
			self.display_message_function("Compression type changed")
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
						self.display_error_function("Impossible to remove channel : %s"%channel)
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





	def combine_alpha_with_sequence_function(self):
		
		#print(self.combined_sequence_list)
		#print(self.alpha_sequence_list)

		if (len(self.combined_sequence_list)==0) or (len(self.alpha_sequence_list)==0):
			self.display_error_function("No file to combine")
			return 
		if len(self.combined_sequence_list) != len(self.alpha_sequence_list):
			self.display_error_function("Combine list are differents")
			return

		for i in range(len(self.combined_sequence_list)):

			self.display_message_function("Trying to combine final renders : %s ; %s"%(self.combined_sequence_list[i], self.alpha_sequence_list[i]))
			#print("trying to combine alpha : %s ; %s"%(self.combined_sequence_list[i], self.alpha_sequence_list[i]))
			#get the combined filename to check if matching with other sequence filename
			combined_filename = os.path.basename(self.combined_sequence_list[i]).split("Denoised_")[1]
			alpha_filename = os.path.basename(self.alpha_sequence_list[i])

			if combined_filename == alpha_filename:
				#combine both files
				self.display_message_function("Combining %s - %s"%(self.combined_sequence_list[i], self.alpha_sequence_list[i]))
				command = '"%s/bin/exrmerge.exr" %s %s'%(self.config["RendermanPath"], self.combined_sequence_list[i], self.alpha_sequence_list[i])
				print(command)
				os.system(command)

		self.display_message_function("ALPHA COMBINE DONE")



	"""
	def check_input_sequence_function(self):

		if os.path.isdir(self.sequence_path)==True:
			if (self.min_frame >= self.max_frame):
				self.display_error_function("You have to enter a valid frame range")
				return


			else:
				input_folder_content = os.listdir(self.sequence_path)

				data_dictionnary = {}
				file_data_dictionnary = {}

				for item in input_folder_content:
					if os.path.isfile(os.path.join(self.sequence_path, item))==True:
						#check if file is .exr
						if os.path.splitext(os.path.join(self.sequence_path, item))[1] == ".exr":
							file_size = os.path.getsize(os.path.join(self.sequence_path, item))
							file_data_dictionnary[os.path.join(self.sequence_path)]
	"""




	
	def check_input_function(self):
		if os.path.isdir(self.sequence_path):
			final_channel_list = []
			size_dictionnary = {}
			global_size_informations = {}
			average_size = 0
			frame_list = []

			if (self.min_frame >= self.max_frame):
				self.display_error_function("You have to enter a valid frame range")

			full_size_added = 0
			full_size_item_number = 0

			channel_compare_list = None

			content = os.listdir(self.sequence_path)

			for item in content:
				if os.path.isfile(os.path.join(self.sequence_path, item))==True:
					#get the frame index
				


					if (os.path.splitext(item)[1] == ".exr") or (os.path.splitext(item)[1] == ".Exr"):
						#get the channel list
						input_file = OpenEXR.InputFile(os.path.join(self.sequence_path, item))
						channel_list = input_file.header()["channels"].keys()

						for channel in channel_list:
							if channel.split(".")[0] not in final_channel_list:
								final_channel_list.append(channel.split(".")[0])

						if channel_compare_list == None:
							channel_compare_list = channel_list
						else:
							for channel in channel_list:
								if channel not in channel_compare_list:
									self.display_message_function("Missing channel [ %s ] on frame : %s"%(channel, os.path.join(self.sequence_path, item)))
						#get the size of the file and add it to the full_size_added list
						full_size_item_number += 1
						size = os.stat(os.path.join(self.sequence_path, item)).st_size / (1024*1024)
						full_size_added += size 
						size_dictionnary[item] = size

			try:
				average_size = full_size_added / full_size_item_number
			except ZeroDivisionError:
				self.display_error_function("No frame contained in the folder!")
				return

			low_size_file_list = {}
			no_size_file_list = {}

			global_size_informations["Average"] = average_size
			#global_size_informations["UpperSize"] = (average_size * 95)/100
			global_size_informations["LowerSize"] = (average_size * 5)/100

			for key, value in size_dictionnary.items():
				
				if (value <= global_size_informations["LowerSize"]):
					low_size_file_list[key] = value
				if value == 0:
					no_size_file_list[key] = value
			global_size_informations["LowSizeFiles"] = low_size_file_list
			global_size_informations["NoSizeFiles"] = no_size_file_list


			return final_channel_list, global_size_informations, size_dictionnary
		else:
			return False, False, False
	






	def clean_output_folder_function(self):
		#get the output path

		output_content = os.listdir(self.output_path)
		for item in output_content:
			
			item_path = os.path.join(self.output_path, item)

			if item.startswith("Denoised") == False:
				if os.path.isfile(item_path)==True:
					try:
						os.remove(item_path)
					except:
						self.display_error_function("Impossible to delete file : %s"%item_path)
				if os.path.isdir(item_path)==True:
					try:
						shutil.rmtree(item_path)
					except:
						self.display_error_function("Impossible to remove directory : %s"%item_path)


		self.display_message_function("DONE")





	


#MANUAL LAUNCH
#DenoiseCore("D:/RMDENOISEAOV/batch/", "D:/RMDENOISEAOV/output")



