# -*- coding: utf-8 -*-

import os 
import sys
import pyfiglet
import colorama
import json
import OpenEXR
import Levenshtein

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

		SEQUENCE_SIZE = 0
		SEQUENCE_LENGTH = 0
		SEQUENCE_SIMILARITY = {}
		SEQUENCE_CHANNEL_CACHE = []

		try:
			self.call_from_thread(self.display_notification_function, "CHECKING INPUT SEQUENCE")
			self.call_from_thread(self.display_notification_function, self.input_path)

			#get the content in the input path
			folder_content = os.listdir(self.input_path)


			self.call_from_thread(self.display_notification_function, "Separating sequences...")



			for i in range(len(folder_content)):


				
				if (os.path.isfile(os.path.join(self.input_path,folder_content[i]))==True) and (os.path.splitext(folder_content[i])[1] == ".exr"):

					#try to create the dictionnary of similarity inside of the sequence folder
					if i == 0:
						SEQUENCE_SIMILARITY[os.path.splitext(folder_content[i])[0].split(".")[0]] = [folder_content[i]]
					else:
						#check for each key of the dictionnary if the similarity is high enough
						#if yes add the file to the existing key
						#else create a new key
						added = False
						for key in SEQUENCE_SIMILARITY:
							ratio = Levenshtein.ratio(os.path.splitext(folder_content[i])[0].split(".")[0], key)
							if ratio > 0.8:
								filelist = SEQUENCE_SIMILARITY[key]
								filelist.append(folder_content[i])
								SEQUENCE_SIMILARITY[key] = filelist
								added=True
								break
							
						#create a new key in the dictionnary
						if added == False:
							SEQUENCE_SIMILARITY[os.path.splitext(folder_content[i])[0].split(".")[0]] = [folder_content[i]]
							

					#PROCESS TO CHECK EACH EXR FILE
					#self.call_from_thread(self.display_message_function, "  %s"%folder_content[i], False)



			for sequence_name, sequence_frames in SEQUENCE_SIMILARITY.items():
				self.call_from_thread(self.display_message_function, "SEQUENCE DETECTED : %s"%key)

				#CHECKING EACH FRAMES FOR THIS SEQUENCE
				try:
					input_file = OpenEXR

				


		except Exception as e:
			self.call_from_thread(self.display_error_function, e)
