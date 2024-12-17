# -*- coding: utf-8 -*-

import os 
import sys
import pyfiglet
import colorama
import json
import OpenEXR
import Levenshtein
import traceback	

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

			self.SEQUENCE_SIZE = 0
			self.SEQUENCE_LENGTH = 0
			self.SEQUENCE_SIMILARITY = {}
			
			self.FINAL_SEQUENCE_DICTIONNARY = {}


			self.call_from_thread(self.display_notification_function, "CHECKING INPUT SEQUENCE")
			self.call_from_thread(self.display_notification_function, self.input_path)

			#get the content in the input path
			folder_content = os.listdir(self.input_path)


			self.call_from_thread(self.display_notification_function, "Separating sequences...")



			for i in range(len(folder_content)):


				
				if (os.path.isfile(os.path.join(self.input_path,folder_content[i]))==True) and (os.path.splitext(folder_content[i])[1] == ".exr"):

					#try to create the dictionnary of similarity inside of the sequence folder
					if i == 0:
						self.SEQUENCE_SIMILARITY[os.path.splitext(folder_content[i])[0].split(".")[0]] = [os.path.join(self.input_path,folder_content[i])]
					else:
						#check for each key of the dictionnary if the similarity is high enough
						#if yes add the file to the existing key
						#else create a new key
						added = False
						for key in self.SEQUENCE_SIMILARITY:
							ratio = Levenshtein.ratio(os.path.splitext(folder_content[i])[0].split(".")[0], key)
							#self.call_from_thread(self.display_message_function, "%s %s %s"%(ratio, os.path.splitext(folder_content[i])[0].split(".")[0], key))
							if ratio == 1:
								filelist = self.SEQUENCE_SIMILARITY[key]
								filelist.append(os.path.join(self.input_path,folder_content[i]))
								self.SEQUENCE_SIMILARITY[key] = filelist
								added=True
								break
							
						#create a new key in the dictionnary
						if added == False:
							self.SEQUENCE_SIMILARITY[os.path.splitext(folder_content[i])[0].split(".")[0]] = [os.path.join(self.input_path,folder_content[i])]
							

					#PROCESS TO CHECK EACH EXR FILE
					#self.call_from_thread(self.display_message_function, "  %s"%folder_content[i], False)
			self.call_from_thread(self.display_success_function, self.SEQUENCE_SIMILARITY.keys())
			
			i=0
			for sequence_name, sequence_frames in self.SEQUENCE_SIMILARITY.items():
				self.call_from_thread(self.display_notification_function, "SEQUENCE DETECTED : %s"%key)

				self.SEQUENCE_CHANNEL_LIST = []
				self.SEQUENCE_FRAME_LIST = []
				self.SEQUENCE_FRAME_SIZE_LIST = []
				self.SEQUENCE_SKIP_FRAMES = []
				self.SEQUENCE_FRAME_INDEX_LIST = []

				#CHECKING EACH FRAMES FOR THIS SEQUENCE
				for frame in sequence_frames:

					#self.call_from_thread(self.display_message_function, "%s : %s"%(os.path.isfile(frame), frame))
					
					try:
						render_file = OpenEXR.InputFile(frame)
						render_data = render_file.header()["channels"]
					except Exception as e:
						self.call_from_thread(self.display_error_function, "  %s"%os.path.basename(frame))
						self.call_from_thread(self.display_error_function, "     %s"%e)
						self.self.SEQUENCE_SKIP_FRAMES.append(frame)
						continue
					else:
						self.call_from_thread(self.display_message_function, "  %s"%os.path.basename(frame))
						self.call_from_thread(self.display_message_function, "     %s"%list(render_data.keys()))

						if self.SEQUENCE_CHANNEL_LIST == []:
							self.SEQUENCE_CHANNEL_LIST = render_data
							self.call_from_thread(self.display_message_function, "     CHANNEL LIST CACHE CREATED")
						else:
							if self.SEQUENCE_CHANNEL_LIST != render_data:
								#difference = list(set(self.SEQUENCE_CHANNEL_LIST) - set(render_data))
								difference = list(set(self.SEQUENCE_CHANNEL_LIST).symmetric_difference(set(render_data)))
								self.call_from_thread(self.display_warning_function, "     Channel difference detected")

								for diff in difference:
									self.call_from_thread(self.display_warning_function, "     %s"%diff)
						self.SEQUENCE_FRAME_LIST.append(frame)
						self.SEQUENCE_FRAME_SIZE_LIST.append(os.path.getsize(frame))
						#self.SEQUENCE_FRAME_INDEX_LIST(os.path.basename(os.path.splitext(frame)[0].split(".")[1]))
						self.SEQUENCE_FRAME_INDEX_LIST.append(i)
						i+=1


				#build the final channel list for the sequence
				final_channel_list = []
				for channel in self.SEQUENCE_CHANNEL_LIST:
					if (channel.split(".")[0], True) not in final_channel_list:
						final_channel_list.append((channel.split(".")[0], True))
				self.call_from_thread(self.display_success_function, "FINAL CHANNEL LIST CREATED")
					
				self.call_from_thread(self.display_success_function, "SEQUENCE CHECKED")

				self.FINAL_SEQUENCE_DICTIONNARY[sequence_name] = {
					"FRAME_LIST":self.SEQUENCE_FRAME_LIST,
					"FRAME_INDEX_LIST":self.SEQUENCE_FRAME_INDEX_LIST,
					"FRAME_SIZE_LIST":self.SEQUENCE_FRAME_SIZE_LIST,
					"FRAME_SKIPPED":self.SEQUENCE_SKIP_FRAMES,
					"CHANNEL_LIST":final_channel_list
				}

			self.call_from_thread(self.display_success_function, "ALL SEQUENCES CHECKED")



			

			


		


		except Exception as e:
			tb = traceback.format_exc()  # Retourne l'exception complète sous forme de chaîne

			# Extraire l'information sur la dernière ligne où l'erreur s'est produite
			last_traceback = traceback.extract_tb(e.__traceback__)[-1]
			file_name = last_traceback.filename
			line_number = last_traceback.lineno
			line_content = last_traceback.line
			
			self.call_from_thread(self.display_error_function, "Error happened while checking sequence")
			self.call_from_thread(self.display_error_function, "%s\n%s\n%s"%(file_name,line_number,line_content), False)
	
			return None



		else:
			try:
				#update lists
				self.call_from_thread(self.update_sequencelist)
			except Exception as e:
				self.call_from_thread(self.display_error_function, e)
			else:
				self.call_from_thread(self.display_message_function, "done")
			
		

