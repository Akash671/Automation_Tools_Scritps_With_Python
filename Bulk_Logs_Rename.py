# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 16:26:10 2023

author: @akash
"""


import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk




def rename_folders(root_directory, UE_Name):
    print(UE_Name)
  
    try:
        # Iterate through all folders in the root directory
        for c_folder_name in os.listdir(root_directory):
            c_folder_path = os.path.join(root_directory, c_folder_name)

            # Check if it's a directory
            if os.path.isdir(c_folder_path):
                # Get a list of all files in the 'C' folder
                files_in_c_folder = os.listdir(c_folder_path)

                # Filter for files with the ".ssc" and ".rtt" extensions
                ssc_files = [filename for filename in files_in_c_folder if filename.endswith('.ssc')]
                rtt_files = [filename for filename in files_in_c_folder if filename.endswith('.rtt')]

                # Ensure there is one .ssc file and at least one .rtt file
                if len(ssc_files) == 1 and len(rtt_files) >= 1:
                    ssc_file_name = ssc_files[0]

                    # Read the content of the first .rtt file
                    rtt_file_path = os.path.join(c_folder_path, rtt_files[0])
                    with open(rtt_file_path, 'r') as rtt_file:
                        rtt_content = rtt_file.read().strip()

                    # Determine the new 'C' folder name based on .rtt content
                    if "Final Verdict - PASS" in rtt_content:
                        new_c_folder_name = os.path.splitext(ssc_file_name)[0] +"_" + UE_Name+"_Pass"
                    else:
                        new_c_folder_name = os.path.splitext(ssc_file_name)[0] +"_" + UE_Name+"_Fail"

                    # Check if the new name already exists
                    if os.path.exists(os.path.join(root_directory, new_c_folder_name)):
                        # If it does, add a unique suffix to the name
                        suffix = 1
                        while os.path.exists(os.path.join(root_directory, f"{new_c_folder_name}_{suffix}")):
                            suffix += 1
                        new_c_folder_name = f"{new_c_folder_name}_{suffix}"

                    # Rename the 'C' folder
                    os.rename(c_folder_path, os.path.join(root_directory, new_c_folder_name))

                    # Display old and new folder names
                    result_label.config(text=f"Old folder name: {c_folder_name}\nNew folder name: {new_c_folder_name}")

        result_label.config(text="'Logs' folders renamed successfully.")
    except Exception as e:
        result_label.config(text=f"An error occurred: {str(e)}")

def browse_directory():
    root_directory = filedialog.askdirectory()
    if root_directory:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, root_directory)





# Create the main window
root = tk.Tk()
root.title("Folder Renamer")


# path = "Keysight.png"  # Replace with the actual path to your logo image
# load = Image.open(path)
# render = ImageTk.PhotoImage(load)

# root.iconphoto(False, render)



# Create and place widgets for folder path
label_path = tk.Label(root, text="Enter Root Directory:")
label_path.grid(row=0, column=0, pady=5)


entry_path = tk.Entry(root, width=50)
entry_path.grid(row=0, column=1, pady=5)

# Create and place widgets for UE name
label_path2 = tk.Label(root, text="Enter the UE Name:")
label_path2.grid(row=1, column=0, pady=5)


entry_path2 = tk.Entry(root, width=50)
entry_path2.grid(row=1, column=1, pady=5)

browse_button = tk.Button(root, text="Browse", bg='skyblue', activebackground='lightblue', command=browse_directory)
browse_button.grid(row=0, column=2, pady=5)

rename_button = tk.Button(root, text="Rename Folders", bg='lightgreen', activebackground='lightblue',command=lambda: rename_folders(entry_path.get(), entry_path2.get()))
rename_button.grid(row=2, column=1, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=2, column=0, columnspan=3)

# Start the main loop
root.mainloop()



"""

try:
    # Iterate through all folders in the root directory
    for c_folder_name in os.listdir(root_directory):
        c_folder_path = os.path.join(root_directory, c_folder_name)

        # Check if it's a directory
        if os.path.isdir(c_folder_path):
            # Get a list of all files in the 'C' folder
            files_in_c_folder = os.listdir(c_folder_path)

            # Filter for files with the ".ssc" and ".rtt" extensions
            ssc_files = [filename for filename in files_in_c_folder if filename.endswith('.ssc')]
            rtt_files = [filename for filename in files_in_c_folder if filename.endswith('.rtt')]

            # Ensure there is one .ssc file and at least one .rtt file
            if len(ssc_files) == 1 and len(rtt_files) >= 1:
                ssc_file_name = ssc_files[0]

                # Read the content of the first .rtt file
                rtt_file_path = os.path.join(c_folder_path, rtt_files[0])
                with open(rtt_file_path, 'r') as rtt_file:
                    rtt_content = rtt_file.read().strip()

                # Determine the new 'C' folder name based on .rtt content
                if "Final Verdict - PASS" in rtt_content:
                    new_c_folder_name = os.path.splitext(ssc_file_name)[0] + "_MTK_Pass"
                else:
                    new_c_folder_name = os.path.splitext(ssc_file_name)[0] + "_MTK_Fail"

                # Check if the new name already exists
                if os.path.exists(os.path.join(root_directory, new_c_folder_name)):
                    # If it does, add a unique suffix to the name
                    suffix = 1
                    while os.path.exists(os.path.join(root_directory, f"{new_c_folder_name}_{suffix}")):
                        suffix += 1
                    new_c_folder_name = f"{new_c_folder_name}_{suffix}"

                # Rename the 'C' folder
                os.rename(c_folder_path, os.path.join(root_directory, new_c_folder_name))

    print("'Run' folders renamed successfully.")
except Exception as e:
    print(f"An error occurred: {str(e)}")








import os

# Define the root directory
root_directory = 'C:/AKASH/R&D/application/20230928'


# Function to check if the "Final Verdict - PASS" string is present in a .rtt file
def is_pass(folder_path):
    rtt_file_path = os.path.join(folder_path, '.rtt')
    if os.path.isfile(rtt_file_path):
        with open(rtt_file_path, 'r') as rtt_file:
            return "Final Verdict - PASS" in rtt_file.read()
    return False

try:
    # Iterate through all folders in the root directory
    for folder_name in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder_name)
        if os.path.isdir(folder_path):
            new_folder_name = folder_name + '_MTK_Pass' if is_pass(folder_path) else folder_name + '_MTK_Fail'
            # Rename the folder
            os.rename(folder_path, os.path.join(root_directory, new_folder_name))
    
    print("Folders renamed successfully.")
except Exception as e:
    print(f"An error occurred: {str(e)}")



# Function to check if the "Final Verdict - PASS" string is present in a file
def is_pass(folder_path):
    rtt_file_path = os.path.join(folder_path, '.rtt')
    if os.path.isfile(rtt_file_path):
        with open(rtt_file_path, 'r') as rtt_file:
            return "Final Verdict - PASS" in rtt_file.read()
    return False

try:
    # Iterate through all folders in the root directory
    for folder_name in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder_name)
        if os.path.isdir(folder_path):
            if is_pass(folder_path):
                new_name = folder_name + '_MTK_Pass'
            else:
                new_name = folder_name + '_MTK_Fail'
            
            # Rename the folder
            os.rename(folder_path, os.path.join(root_directory, new_name))
    
    print("Folders renamed successfully.")
except Exception as e:
    print(f"An error occurred: {str(e)}")






import os

# Path to the "Parent" directory
parent_directory = "C:/AKASH/R&D/application/20230928"

# Iterate through the child folders in the "Parent" directory
for child_folder_name in os.listdir(parent_directory):
    child_folder_path = os.path.join(parent_directory, child_folder_name)

    # Check if the item is a directory
    if os.path.isdir(child_folder_path):
        # Find the corresponding .rtt file in the child folder
        rtt_file = None
        for file_name in os.listdir(child_folder_path):
            if file_name.endswith(".rtt"):
                rtt_file = os.path.join(child_folder_path, file_name)
                break

        # Initialize a flag to determine folder renaming
        pass_found = False

        # If an .rtt file is found, read its content and check for "Final Verdict - PASS"
        if rtt_file:
            with open(rtt_file, 'r') as rtt_file:
                content = rtt_file.read()
            if "Final Verdict - PASS" in content:
                pass_found = True

        # Find the corresponding .ssc file in the child folder
        ssc_file = None
        for file_name in os.listdir(child_folder_path):
            if file_name.endswith(".ssc"):
                ssc_file = os.path.join(child_folder_path, file_name)
                break

        # Determine the new folder name based on whether "Final Verdict - PASS" was found
        if pass_found:
            new_folder_name = os.path.splitext(child_folder_name)[0] + "_MTK_Pass"
        elif ssc_file:
            new_folder_name = os.path.splitext(os.path.basename(ssc_file))[0] + "_MTK_Fail"
        else:
            new_folder_name = child_folder_name

        new_folder_path = os.path.join(parent_directory, new_folder_name)

        # Check if the target folder name already exists
        if os.path.exists(new_folder_path):
            # Append a suffix to the folder name to avoid conflicts
            suffix = 1
            while os.path.exists(f"{new_folder_path}-{suffix}"):
                suffix += 1
            new_folder_path = f"{new_folder_path}-{suffix}"

        os.rename(child_folder_path, new_folder_path)
        print(f'Renamed folder "{child_folder_name}" to "{new_folder_name}"'


import os

# Path to the "Parent" directory
parent_directory = "C:/AKASH/R&D/application/20230928"

# Iterate through the child folders in the "Parent" directory
for child_folder_name in os.listdir(parent_directory):
    child_folder_path = os.path.join(parent_directory, child_folder_name)

    # Check if the item is a directory
    if os.path.isdir(child_folder_path):
        # Find the corresponding .ssc file in the child folder
        ssc_file = None
        for file_name in os.listdir(child_folder_path):
            if file_name.endswith(".ssc"):
                ssc_file = os.path.join(child_folder_path, file_name)
                break

        # Initialize a flag to determine folder renaming
        pass_found = False

        # If an .ssc file is found, use its name for renaming
        if ssc_file:
            new_folder_name = os.path.splitext(os.path.basename(ssc_file))[0]
        else:
            new_folder_name = child_folder_name

        new_folder_name += "_MTK_Pass" if pass_found else "_MTK_Fail"
        new_folder_path = os.path.join(parent_directory, new_folder_name)

        # Check if the target folder name already exists
        if os.path.exists(new_folder_path):
            # Append a suffix to the folder name to avoid conflicts
            suffix = 1
            while os.path.exists(f"{new_folder_path}-{suffix}"):
                suffix += 1
            new_folder_path = f"{new_folder_path}-{suffix}"

        os.rename(child_folder_path, new_folder_path)
        print(f'Renamed folder "{child_folder_name}" to "{new_folder_name}"')

import os

# Path to the "Parent" directory
parent_directory = "C:/AKASH/R&D/application/20230928"

# Iterate through the child folders in the "Parent" directory
for child_folder_name in os.listdir(parent_directory):
    child_folder_path = os.path.join(parent_directory, child_folder_name)

    # Check if the item is a directory
    if os.path.isdir(child_folder_path):
        # Find the corresponding .rtt file in the child folder
        rtt_file = None
        for file_name in os.listdir(child_folder_path):
            if file_name.endswith(".rtt"):
                rtt_file = os.path.join(child_folder_path, file_name)
                break

        # Initialize a flag to determine folder renaming
        pass_found = False

        # If an .rtt file is found, read its content and check for "Final Verdict - PASS"
        if rtt_file:
            with open(rtt_file, 'r') as rtt_file:
                content = rtt_file.read()
            if "Final Verdict - PASS" in content:
                pass_found = True

        # Determine the new folder name based on whether "Final Verdict - PASS" was found
        new_folder_name = os.path.splitext(child_folder_name)[0]

        if pass_found:
            new_folder_name += "_MTK_Pass"
        else:
            new_folder_name += "_MTK_Fail"

        new_folder_path = os.path.join(parent_directory, new_folder_name)

        # Check if the target folder name already exists
        if os.path.exists(new_folder_path):
            # Append a suffix to the folder name to avoid conflicts
            suffix = 1
            while os.path.exists(f"{new_folder_path}-{suffix}"):
                suffix += 1
            new_folder_path = f"{new_folder_path}-{suffix}"

        os.rename(child_folder_path, new_folder_path)
        print(f'Renamed folder "{child_folder_name}" to "{new_folder_name}"')



import os

# Path to the "Parent" directory
parent_directory = "C:/AKASH/R&D/application/20230928"

# Iterate through the folders in the "Parent" directory
for folder_name in os.listdir(parent_directory):
    folder_path = os.path.join(parent_directory, folder_name)

    # Check if the item is a directory
    if os.path.isdir(folder_path):
        # Find the corresponding .ssc file in the folder
        ssc_file = None
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".ssc"):
                ssc_file = os.path.join(folder_path, file_name)
                break

        # Initialize a flag to determine folder renaming
        pass_found = False

        # If a .ssc file is found, check if a corresponding .rtt file exists
        if ssc_file:
            rtt_file_name = os.path.splitext(os.path.basename(ssc_file))[0] + ".rtt"
            rtt_file_path = os.path.join(folder_path, rtt_file_name)
            if os.path.exists(rtt_file_path):
                # Read the content of the .rtt file and check for "Final Verdict - PASS"
                with open(rtt_file_path, 'r') as rtt_file:
                    content = rtt_file.read()
                if "Final Verdict - PASS" in content:
                    pass_found = True

        # Determine the new folder name based on whether "Final Verdict - PASS" was found
        if pass_found:
            new_folder_name = os.path.splitext(os.path.basename(ssc_file))[0] + "_MTK_Pass"
        else:
            new_folder_name = os.path.splitext(os.path.basename(ssc_file))[0] + "_MTK_Fail"

        new_folder_path = os.path.join(parent_directory, new_folder_name)

        # Check if the target folder name already exists
        if os.path.exists(new_folder_path):
            # Append a suffix to the folder name to avoid conflicts
            suffix = 1
            while os.path.exists(f"{new_folder_path}-{suffix}"):
                suffix += 1
            new_folder_path = f"{new_folder_path}-{suffix}"

        os.rename(folder_path, new_folder_path)
        print(f'Renamed folder "{folder_name}" to "{new_folder_name}"')




"""
