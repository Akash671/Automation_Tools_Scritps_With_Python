# -*- coding: utf-8 -*-
"""
author : @akash

"""

import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def search_replace_ssc_files():
    # Get the folder path from the user
    folder_path = folder_path_entry.get()
    if not folder_path:
        messagebox.showerror("Error", "Please select a folder.")
        return

    # Get the search and replace strings from the user
    search_string = search_entry.get()
    replace_string = replace_entry.get()

    # Iterate through the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.ssc'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r+') as file:
                # Read the file contents
                content = file.read()

                # Search for the string and replace it
                updated_content = re.sub(search_string, replace_string, content)

                # Go back to the beginning of the file and overwrite the content
                file.seek(0)
                file.write(updated_content)
                file.truncate()

            print(f"Updated file: {filename}")

    messagebox.showinfo("Success", "Search and replace operation completed.")

# Create the GUI window
window = tk.Tk()
window.title("Search and Replace SSC Files")
window.geometry("400x300")
window.configure(bg="#F0F0F0")

# Folder path label and entry
folder_label = tk.Label(window, text="Folder path:", bg="#F0F0F0", fg="black", font=("Helvetica", 12))
folder_label.pack(pady=10)
folder_path_entry = tk.Entry(window, font=("Helvetica", 12))
folder_path_entry.pack(pady=5)

# Search string label and entry
search_label = tk.Label(window, text="Search string:", bg="#F0F0F0", fg="black", font=("Helvetica", 12))
search_label.pack()
search_entry = tk.Entry(window, font=("Helvetica", 12))
search_entry.pack(pady=5)

# Replace string label and entry
replace_label = tk.Label(window, text="Replace string:", bg="#F0F0F0", fg="black", font=("Helvetica", 12))
replace_label.pack()
replace_entry = tk.Entry(window, font=("Helvetica", 12))
replace_entry.pack(pady=5)

# Start button
start_button = tk.Button(window, text="Start", bg="#008CBA", fg="white", font=("Helvetica", 14, "bold"), 
                         command=search_replace_ssc_files)
start_button.pack(pady=20)

# Run the GUI event loop
window.mainloop()