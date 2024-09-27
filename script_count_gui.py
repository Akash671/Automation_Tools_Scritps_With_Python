# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 06:11:11 2024
@author: akash
"""

#05a,06a,08a,09a,16a,18a,19c,22a,27a,30a

import os
from tkinter import Tk, Label, Entry, Button, StringVar, W, E, TOP, BOTTOM, X, Y, BOTH, LEFT, RIGHT, GROOVE, NONE, Scrollbar, Listbox, Toplevel, ttk
from tabulate import tabulate  # Import tabulate for table formatting
import tkinter as tk  # Import tkinter explicitly

def count_file_extensions(folder_path):
  """Counts the number of files with different extensions in a given folder.

  Args:
    folder_path: The path to the folder.

  Returns:
    A dictionary where keys are file extensions (without the dot) and values are the counts.
  """

  extension_counts = {}
  total_count = 0  # Initialize total count
  try:
    for filename in os.listdir(folder_path):
      # Get the file extension (without the dot)
      _, ext = os.path.splitext(filename)
      ext = ext[1:]  # Remove the leading dot

      # Increment the count for this extension
      if ext in extension_counts:
        extension_counts[ext] += 1
      else:
        extension_counts[ext] = 1
      
      total_count += 1  # Increment total count for each file
    return extension_counts, total_count  # Return both counts
  except Exception as e:
    # Handle any exceptions during file listing
    show_error(str(e))
    return None, None  # Return None if an error occurred

def process_batches():
  """Processes the batches and displays results in a table."""
  operator = operator_entry.get()
  batches = batch_entry.get()
  batches = batches.split(',')  # Split the input string by comma
  table_data = []
  if operator == "ATT":
    for batch in batches:
      batch = batch.strip()  # Remove leading/trailing spaces
      PATH = [
        f"C:\Keysight\SAS\Scripts\Carrier Acceptance Scripts Release {batch}.v58.810\Validated",
        f"C:\Keysight\SAS\Scripts\Carrier Acceptance Scripts Release {batch}.v58.810\Obsolete"
      ]
      for path in range(2):
        try:
          extension_counts, total_count = count_file_extensions(PATH[path])
          if extension_counts is not None:  # Check if counts were successfully retrieved
            status = "Validated" if path == 0 else "Obsolete"
            table_data.append([batch, status, total_count, *extension_counts.values()])
        except Exception as e:
          # Handle any exceptions during file counting
          show_error(str(e))
  elif operator == "TMO":
    for batch in batches:
      batch = batch.strip()  # Remove leading/trailing spaces
      PATH = [
        f"C:\Keysight\SAS\Scripts\T-Mobile Acceptance Scripts Release {batch}.v67.810\Validated",
        f"C:\Keysight\SAS\Scripts\T-Mobile Acceptance Scripts Release {batch}.v67.810\Obsolete"
      ]
      for path in range(2):
        try:
          extension_counts, total_count = count_file_extensions(PATH[path])
          if extension_counts is not None:  # Check if counts were successfully retrieved
            status = "Validated" if path == 0 else "Obsolete"
            table_data.append([batch, status, total_count, *extension_counts.values()])
        except Exception as e:
          # Handle any exceptions during file counting
          show_error(str(e))
  else:
    show_error("Invalid Operator")
    return

  # Display the results in a table
  headers = ["Batch", "Status", "Total Files", "ssc", "ssi", "psc", "sro"]
  table = tabulate(table_data, headers=headers, tablefmt="grid")

  # Clear previous text in the text widget
  result_text.delete("1.0", "end") 
  result_text.insert("1.0", table)

def show_error(error_message):
  """Displays an error message in a separate window."""
  error_window = Toplevel(root)
  error_window.title("Error")
  error_label = Label(error_window, text=error_message)
  error_label.pack(padx=10, pady=10)

# Create the main window
root = Tk()
root.title("SSC,SSI,PSC,SRO COUNTS")

# Set background color
root.configure(bg="#f0f0f0")  # Light gray background

# Create labels and entry widgets
operator_label = Label(root, text="Enter Operator:", bg="#f0f0f0")
operator_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)

operator_entry = Entry(root, width=10)
operator_entry.grid(row=0, column=1, sticky=W + E, padx=5, pady=5)

batch_label = Label(root, text="Enter Batches (comma-separated):", bg="#f0f0f0")
batch_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)

batch_entry = Entry(root, width=50)
batch_entry.grid(row=1, column=1, sticky=W + E, padx=5, pady=5)

# Create the process button
process_button = Button(root, text="Process", command=process_batches, bg="#4CAF50", fg="white")
process_button.grid(row=2, column=0, columnspan=2, sticky=W + E, padx=5, pady=5)

# Create a Text widget to display the results
result_text = tk.Text(root, wrap=tk.WORD, bg="#f5f5f5")  # Light gray background
result_text.grid(row=3, column=0, columnspan=2, sticky=W + E, padx=5, pady=5)

# Style the Text widget using ttk
style = ttk.Style()
style.configure("TText", background="#f5f5f5", foreground="black")
style.configure("TLabel", background="#f0f0f0", foreground="black")
style.configure("TButton", background="#4CAF50", foreground="white")

# Run the main loop
root.mainloop()