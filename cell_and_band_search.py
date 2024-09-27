# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 06:11:11 2024
@author: akash
"""


import os
import re
from tabulate import tabulate  # Import tabulate for table formatting

# Function to search for patterns in .ssc files
def search_patterns_in_files(folder_path):
    results = []  # List to store results for each file

    # Loop through files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".ssc"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                content = file.read()
                cell_ids = set(re.findall(r'<CellID>(\w)</CellID>', content))  # Convert to set for uniqueness
                bands = re.findall(r'<Band>(\w+)</Band>', content)

                # Store results for this file
                for cell_id in cell_ids:
                    results.append({
                        "File": file_name,
                        "CellID": cell_id,
                        "Band": bands[0] if bands else ""  # Get the first band if available
                    })

    return results

try:
 # User input: Folder path
 folder_path = input("Enter the folder path: ")

 # Search for patterns in .ssc files
 results = search_patterns_in_files(folder_path)

 # Print the results in table format
 headers = {"File": "File", "CellID": "CellID", "Band": "Band"}  # Define headers as a dictionary
 table = tabulate(results, headers=headers, tablefmt="grid")
 print(table)
except:
    print("Invalid path")