from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import shutil
import os
import sys

def InList(filetype, list):
	Found = False
	for i in list:
		if Found == False:
			if filetype == i:
				Found = True
	return Found

def ListFromFile(filepath):
	return_list = []
	file = open(filepath, 'r')
	for i in file:
		split_line = i.split(" ")
		for j in split_line:
			return_list.append(j)
	file.close()
	return return_list

def ListLower(list):
	return [i.lower() for i in list]

def GetSources():
	input("Press enter to select folders to clean, press cancel to stop selecting folders.\n")
	filepath_list = []
	directories_chosen = False
	directory = "c:\\"
	while directories_chosen == False:
		directory = filedialog.askdirectory(initialdir=(directory))    #gets the location of the file that will be edited
		if directory == "":
			directories_chosen = True
		elif os.path.isdir(directory) == True:
			filepath_list.append(directory)
		else:
			print("That directory doesn't exist!")
	return filepath_list

def GetBanned(source_folder):
	directory = source_folder
	ban_choice = input("Press enter to select folders to blacklist, press cancel to stop selecting folders. Type SKIP to skip\n")
	if ban_choice.upper() != "SKIP":
		filepath_list = []
		directories_chosen = False
		while directories_chosen == False:
			directory = filedialog.askdirectory(initialdir=(directory))    #gets the location of the file that will be edited
			if directory == "":
				directories_chosen = True
			elif os.path.isdir(directory) == True:
				appendyboi = os.path.basename(directory)
				filepath_list.append(appendyboi)
			else:
				print("That directory doesn't exist!")
		return filepath_list
	else:
		return []

def FullSort(filepath_list, txt_folder_path, destination_base):
	skip_choice = input("\nWould you like to skip all files with filename clashes? (y/n):   ")
	if skip_choice.lower() == "y":
		skip_all = True
	else:
		skip_all = False

	move_all_choice = input("Would you like to move unidentifiable files to an 'other' folder? (y/n):   ")

	if move_all_choice.lower() == "y":
		move_all = True
	else:
		move_all = False

	for filepath in filepath_list: #for each path
		SortFolder(filepath, destination_base, txt_folder_path, skip_all, move_all)

def CheckMakeFolder(folder):
	if os.path.isdir(folder) == False:
		try:
			os.makedirs(folder)
			print("Directory " + folder + " has been created. ")
		except:
			pass

def SortFolder(source, destination_base, txt_folder_path, skip_all, move_all):
	file_list = os.listdir(source)
	txt_files = os.listdir(txt_folder_path)
	dest_file_list = []
	list_of_folders = []
	for txt_filename in txt_files:
		list_of_folders.append(txt_filename.strip(".txt"))

	banned_folders = GetBanned(source)
	if banned_folders != []:
		for ban_folder in banned_folders:
			print(ban_folder)
		bansready = input("\nAre you sure you would like to ban these folders? (y/n):  ")
		if bansready.lower() == "y":
			for folder in banned_folders:
				list_of_folders.append(folder)
		else:
			banned_folders = []

	list_of_folders.append("Sorted")
	list_of_folders.append("Other")

	for file in file_list:         #for every file in file_list
		lower_file = file.lower()
		filetype_found = False

		if file in list_of_folders:
			if skip_all == True:
				move_folder_boi = "0"
			else:
				do_i_move_the_folder = input("\nThe file " + "\"" + file + "\"" + " is in the list of folders. This can create some issues with the naming system this program uses. Would you like to move it anyway? (y/n):    ")
				print("\n")
				if do_i_move_the_folder.lower() == "y":
					move_folder_boi = "1"
				else:
					move_folder_boi = "0"

		else:
			move_folder_boi = "1"

		if move_folder_boi == "1":
			for text_path in txt_files:
				if filetype_found == False:
					txt_path = os.path.join(txt_folder_path, text_path)
					filetype_list = ListFromFile(txt_path)

					for filetype in filetype_list:
						if filetype_found == False:
							lower_filetype = filetype.lower()
							if lower_file.endswith(lower_filetype):
								filetype_found = True
								move_file = True

								sort_into_folder = os.path.basename(txt_path)
								strippy_boi = sort_into_folder.strip(".txt")
								destination = os.path.join(destination_base, strippy_boi)
							else:
								move_file = False


			if move_file == False:
				if move_all == True:
					destination = os.path.join(destination_base, "Other")
					move_file = True

			if move_file == True:
				orig_file = os.path.join(source, file)
				dest_file = os.path.join(destination, file)

				try:
					dest_file_list = os.listdir(destination)
				except:
					pass

				try:
					dest_file_list_lower = ListLower(dest_file_list)
				except:
					pass

				if file.lower() not in dest_file_list_lower:
					try:
						CheckMakeFolder(destination)
						shutil.move(orig_file, dest_file)
						print(file + " has been moved to " + destination + "...")
					except:
						pass
				else:
					if skip_all != True:
						dealt_with = False
						while dealt_with == False:
							move_choice = input("\nThe file " + file + " already exists in " + destination + ". Would you like to skip (1), type a new filename (2), delete the file (3):  ")
							if move_choice == "1":
								dealt_with = True
							elif move_choice == "2":
								new_filename = input("Enter the new filename (with file extension):  ")
								if new_filename.lower() not in dest_file_list_lower:
									dest_file = os.path.join(destination, new_filename)
									CheckMakeFolder(destination)
									try:
										shutil.move(orig_file, dest_file)
										print(file + " has been moved to " + destination + "....")
									except:
										pass
									dealt_with = True
								else:
									print("The new filename already exists!!!")
							elif move_choice == "3":
								try:
									os.remove(orig_file)
								except:
									pass
								dealt_with = True

def GetDirectories(desktop):
	paths_chosen = "0"
	while paths_chosen == "0":
		filepath_list = []
		paths_chosen = input("\nWould you like to...\nClean The Desktop (1)\nClean Other Folders (2)\nExit The Program (3):  ")
		if paths_chosen == "3":
			sys.exit()

		elif paths_chosen == "1":
			filepath_list.append(desktop)

		elif paths_chosen == "2":
			filepath_list = GetSources()
			print("\nDirectory list:")
			for directory in filepath_list:
				print(directory)
			reassurance = input("\nAre you sure you would like to clean these folders? (y/n):  ")
			if reassurance != "y":
				paths_chosen = "0"
		else:
			sys.exit()
	return filepath_list

def GetDestination(desktop):
	destination_selected = False
	while destination_selected != True:
		destination_selection = input("\nWhere would you like the sorted files to go?\nOn desktop (1)\nType location new (2)\nType location existing (3):  ")
		if destination_selection == "1":
			destination_base = desktop + "\\" + "Sorted"
			if os.path.isdir(destination_base) == False:
				os.makedirs(destination_base)
			destination_selected = True
		elif destination_selection == "2":
			base_upper = input("Enter a path for the sorted folders.\nA new folder \"sorted\" will be created in this path, or this folder will be created:  ")
			if os.path.isdir(base_upper) == True:
				sorted_path = base_upper + "\\" + "Sorted"
				if not os.path.isdir(sorted_path) == True:
					destination_base = sorted_path
					destination_selected = True
				else:
					print("The path selected is already in use for sorting.\nPlease select option (3)")
			else:
				os.makedirs(base_upper)
				destination_base = base_upper
				destination_selected = True
		elif destination_selection == "3":
			base_path = input("\nPlease locate the \"sorted\" folder (or select a new base sorted folder):  ")
			if os.path.isdir(base_path) == True:
				destination_base = base_path
				destination_selected = True
			else:
				print("That location doesn't exist. Please select option (2) to create a save directory.")
	return destination_base

def donothing(event):
	print("it works")

def main():
	py_location = os.path.dirname(os.path.abspath(__file__))
	config_location = os.path.join(py_location, "default.txt")
	txt_folder_name = "filetype_resource"
	txt_folder_path = os.path.join(py_location, txt_folder_name)

	if os.path.isfile(config_location) == True:
		default_exists = True
	else:
		default_exists = False

	if default_exists == True:
		usedefault = input("*A default configuration file was found (default.txt)*\nWould you like to use this config? (y/n):   ")
		if usedefault.lower() == "y":
			filepath_list = []
			defaults = open("default.txt", "r")
			for line in defaults:
				if line.startswith("-"):
					appendyboi = line[1:]
					appendyboi = appendyboi.strip()
					destination_base = appendyboi
				else:
					appendyboi = line.strip()
					filepath_list.append(appendyboi)
		else:
			default_exists = False

	if default_exists == False:
		desktop = "c:" + os.path.join(os.environ["HOMEPATH"], "Desktop")
		filepath_list = GetDirectories(desktop)         #gets files
		destination_base = GetDestination(desktop)      #gets destinations



	FullSort(filepath_list, txt_folder_path, destination_base)
	input("Folder(s) sorted! Press Enter to continue... ")

	if os.path.isfile(config_location) == False:
		config_choice_set = False
		while config_choice_set == False:
			config_choice = input("\nWould you like to set this as your default configuration? (y/n):   ")
			if config_choice.lower == "y" or "yes":
				config_file = open('default.txt', 'w')
				for filepath in filepath_list:
					config_file.write(filepath + "\n")
				config_file.write("-" + destination_base)
				config_file.close()
			config_choice_set = True

root = Tk()
root.resizable(0,0)
root.title("Folder Sorter")

can_sort = False

if can_sort == True:
	btnSort = Button(root, text = "Sort", bg = "white", fg = "black", height = "2", width = "17") #command = print(gay) will print gay when the button is initialised
else:
	btnSort = Button(root, text = "Sort", bg = "grey", fg = "black", height = "2", width = "17")

btnSort.grid(row = 2, column = 2, padx = 50, pady = 30, columnspan = 2)      #sticky = S will stick it down

lblChoose = Label(root, text = "1:  Choose files", fg = "black", height = "2", width = "12")
lblChoose.grid(row = 1, column = 0, padx = 4, pady = 4)

lblSort = Label(root, text = "2:  Sort Folders", fg = "black", height = "2", width = "12")
lblSort.grid(row = 2, column = 0, padx = 4, pady = 4)

btnChooseFolders = Button(root, text = "F", bg = "white", fg = "black", height = "1", width = "2")
btnChooseFolders.grid(row = 1, column = 2, padx = 2, pady = 2)

btnChooseSaved = Button(root, text = "S", bg = "white", fg = "black", height = "1", width = "2")
btnChooseSaved.grid(row = 1, column = 3, padx = 2, pady = 2)

btnChooseFolders.bind("<Button-1>", donothing)

root.mainloop()
root.quit()

main()
