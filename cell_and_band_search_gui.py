# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 19:48:23 2024

@author: Administrator
"""

import os
import re
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

def search_patterns():
    """Searches for CellID and Band patterns in .ssc files within the selected folder."""
    global folder_path
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        results = search_patterns_in_files(folder_path)
        display_results(results)

def search_patterns_in_files(folder_path):
    """Searches for CellID and Band patterns in .ssc files within a given folder.

    Args:
        folder_path: The path to the folder.

    Returns:
        A list of dictionaries containing the results for each file.
    """
    results = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".ssc"):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    cell_ids = set(re.findall(r'<CellID>(\w)</CellID>', content))
                    bands = re.findall(r'<Band>(\w+)</Band>', content)
                    for cell_id in cell_ids:
                        results.append({
                            "File": file_name,
                            "CellID": cell_id,
                            "Band": bands[0] if bands else ""
                        })
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {file_name}: {e}")
    return results

def display_results(results):
    """Displays the search results in a table format."""
    headers = {"File": "File", "CellID": "CellID", "Band": "Band"}
    table = tabulate(results, headers=headers, tablefmt="grid")
    result_text.delete("1.0", "end")
    result_text.insert("1.0", table)

# Create the main window
root = tk.Tk()
root.title("CellID and Band Search")

# Set background color
root.configure(bg="#f0f0f0")

# Create a label for the folder selection
folder_label = tk.Label(root, text="Select Folder:", bg="#f0f0f0")
folder_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

# Create a button to browse for the folder
browse_button = tk.Button(root, text="Browse", command=search_patterns, bg="#4CAF50", fg="white")
browse_button.grid(row=0, column=1, sticky=tk.W + tk.E, padx=5, pady=5)

# Create a Text widget to display the results
result_text = tk.Text(root, wrap=tk.WORD, bg="#f5f5f5")
result_text.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=5)

# Style the Text widget using ttk
style = ttk.Style()
style.configure("TText", background="#f5f5f5", foreground="black")
style.configure("TLabel", background="#f0f0f0", foreground="black")
style.configure("TButton", background="#4CAF50", foreground="white")

# Run the main loop
root.mainloop()