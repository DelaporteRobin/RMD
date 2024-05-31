import os
import sys
import colorama
import shutil

from termcolor import *

colorama.init()




class Application:
	def __init__(self):
		self.input_path = "D:/render_test_crash"

		self.double_frame_function()




	def double_frame_function(self):

		if os.path.isdir(self.input_path)==False:
			print("You have to enter a valid input path!")
			return


		frame_dictionnary = {}

		content = os.listdir(self.input_path)
		
		for i in range(len(content)):
			#print(content[i])
			try:

				#get file informations
				filename, extension = os.path.splitext(content[i])
				splited_filename = filename.split(".")
				#print(splited_filename)
				index = splited_filename[1]

				next_filename, next_extension = os.path.splitext(content[i+1])
				next_splited_filename = next_filename.split(".")
				next_index = next_splited_filename[1]

				if int(next_index) != int(index)+2:
					#print(content[i])
					next_filename = (".".join([splited_filename[0], str(int(index)+2)]))+extension

					
					
					frame_dictionnary[str(int(index)+2)] = content[i+1]
					content[i+1] = next_filename
			except IndexError:
				pass

		index_list = list(reversed(list(frame_dictionnary.keys())))
		file_list = list(reversed(list(frame_dictionnary.values())))

		for i in range(len(index_list)):
			#create the new filename
			filename, extension = os.path.splitext(file_list[i])
			name, index = filename.split(".")

			new_filename = ".".join([name,index_list[i]])+extension
			os.rename(os.path.join(self.input_path, file_list[i]), os.path.join(self.input_path, new_filename))

		
		
		content = os.listdir(self.input_path)
		"""
		go and check each file
		if the index is odd duplicate the file and give the even index
		"""
		for i in range(len(content)):
			try:
				filename, extension = os.path.splitext(content[i])
				name, index = filename.split(".")

				if int(index)%2 == 1:
					#duplicate the file and create the second frame
					new_file = ".".join([name, str(int(index)+1)])+extension 
					shutil.copy(os.path.join(self.input_path, content[i]), os.path.join(self.input_path, new_file))
					print("copied : %s"%new_file)
			except IndexError:
				pass
Application()