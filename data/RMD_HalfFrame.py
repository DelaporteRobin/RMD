import os
import sys
import colorama
import shutil

from termcolor import *

colorama.init()




class Application:
	def __init__(self):


		self.input_path = "D:/render_test_crash"

		self.delete_half_function()



	def display_error_function(self, message):
		print(colored(message, "red"))



	def delete_half_function(self):
		
		if os.path.isdir(self.input_path)==False:
			self.display_error_function("You have to enter a valid input path")
			return

		#create the output path
		self.output_path = "%s_output"%(self.input_path)
		#os.mkdir(self.output_path)


		"""
		get the content of the folder
		for each frame get index
		if index % 2 == 1 delete frame
		replace the frame by the next one duplicated
		"""

		content = os.listdir(self.input_path)

		#create the first frame
		#first_index = str(int(os.path.splitext(content[0])[0].split(".")[1])-1)
		#filename = ".".join([os.path.splitext(content[0])[0].split(".")[0], str(int(os.path.splitext(content[0])[0].split(".")[1])-1)])+os.path.splitext(content[0])[1]


		
		#shutil.copy(os.path.join(self.input_path, content[0]), os.path.join(self.input_path, ".".join([os.path.splitext(content[0])[0].split(".")[0], str(int(os.path.splitext(content[0])[0].split(".")[1])-1)])+os.path.splitext(content[0])[1]))
	


		
		content = os.listdir(self.input_path)
		for i in range(len(content)):
			if os.path.isfile(os.path.join(self.input_path, content[i]))==True:
				#get the frame index
				splited_filename = os.path.splitext(content[i])[0].split(".")
				if (len(splited_filename)==2) and (splited_filename[1].isdigit()==True):
					index = splited_filename[1]

					if int(index)%2 == 0:
						#get the index of the previous frame if possible
						try:
							next_frame_name = content[i + 1]

							print("REPLACE %s BY %s"%(index, str(int(index)+1)))

							os.remove(os.path.join(self.input_path,content[i+1]))
							#shutil.copy(os.path.join(self.input_path, content[i]), os.path.join(self.input_path, content[i+1]))
						except IndexError:
							pass
		


		#get the new content of the folder

		content = os.listdir(self.input_path)
		
		for i in range(len(content)):
			if os.path.isfile(os.path.join(self.input_path, content[i]))==True:
				splited_filename = os.path.splitext(content[i])[0].split(".")

				try:
					next_splited_filename = os.path.splitext(content[i+1])[0].split(".")
				except:
					print("error : %s"%content[i])
					break
				else:


					if (len(splited_filename) == 2) and (splited_filename[1].isdigit()==True):
						index = splited_filename[1]
						next_index = str(int(index)+1)

						
						next_filename = ".".join([os.path.splitext(content[i+1])[0].split(".")[0], next_index])+os.path.splitext(content[i+1])[1]
						print("%s  :  %s"%(content[i], next_filename))
						
						os.rename(os.path.join(self.input_path, content[i+1]), os.path.join(self.input_path, next_filename))
						content[i+1] = next_filename
	
		
		



					

Application()


