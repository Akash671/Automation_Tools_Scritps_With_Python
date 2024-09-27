"""
author : @akash
ATT and TMO Batch Downloader
"""

import sys
import threading
import requests
import shutil
import time
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar,
                             QGridLayout, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont



# import logging
# logger = logging.getLogger(__name__)
# #logging.basicConfig(filename='download_log.txt', level=logging.INFO)
# logging.basicConfig(filename='download_log.txt', level=logging.INFO, mode='a')

class DownloadThread(QThread):
    progress_updated = pyqtSignal(str, int, int)  # file, progress, total_size
    status_updated = pyqtSignal(str, str)  # file, status
    finished = pyqtSignal(bool)

    def __init__(self, url, destination):
        super().__init__()
        self.url = url
        self.destination = destination

    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            with open(self.destination, 'wb') as file:
                for data in response.iter_content(chunk_size=1024):
                    downloaded += len(data)
                    file.write(data)
                    self.progress_updated.emit(self.destination, downloaded, total_size)
            self.status_updated.emit(self.destination, "Completed")
            self.finished.emit(True)
        except requests.exceptions.RequestException as e:
            self.status_updated.emit(self.destination, f"Failed: {e}")
            self.finished.emit(False)
        except Exception as e:
            self.status_updated.emit(self.destination, f"Failed: {e}")
            self.finished.emit(False)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATT/TMO Batch Downloader")
        self.successful_downloads = 0
        self.failed_downloads = 0
        self.threads = []
        self.download_lock = threading.Lock()
        self.font = QFont()  # Create QFont object HERE
        self.font.setPointSize(10)  # Set font size
        self.initUI()  # Call initUI AFTER font is initialized

    def initUI(self):
        release_label = QLabel("Release Version (e.g., v58_810 or v66_810):")
        self.release_edit = QLineEdit()
        dest_label = QLabel("Enter Destination Folder Path:")
        self.dest_edit = QLineEdit()
        batch_label = QLabel("Batch Names (space-separated, e.g., 05a 06a):")
        self.batch_edit = QLineEdit()
        operator_label = QLabel("Select Operator:")
        self.operator_combo = QComboBox()
        self.operator_combo.addItems(["ATT", "TMO"])  # Add more operators as needed
        download_button = QPushButton("Start Download")
        download_button.clicked.connect(self.start_downloads)
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setFont(self.font)  # set font
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        grid = QGridLayout()
        grid.addWidget(release_label, 0, 0)
        grid.addWidget(self.release_edit, 0, 1)
        grid.addWidget(dest_label, 1, 0)
        grid.addWidget(self.dest_edit, 1, 1)
        grid.addWidget(batch_label, 2, 0)
        grid.addWidget(self.batch_edit, 2, 1)
        grid.addWidget(operator_label, 3, 0)
        grid.addWidget(self.operator_combo, 3, 1)
        grid.addWidget(download_button, 4, 0, 1, 2)
        grid.addWidget(self.status_label, 5, 0, 1, 2)
        grid.addWidget(self.progress_bar, 6, 0, 1, 2)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        self.setLayout(vbox)

    def start_downloads(self):
        release_version = self.release_edit.text()
        destination_folder = self.dest_edit.text()
        batch_names = self.batch_edit.text().split()
        selected_operator = self.operator_combo.currentText()

        if not release_version or not destination_folder or not batch_names or not selected_operator:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(batch_names))
        self.status_label.setText("Downloading...")

        for batch_name in batch_names:
            operator_prefix = "CAS" if selected_operator == "ATT" else "TAS"  # Adjust as needed for TMO
            url = f"http://10.97.116.239/GeneratedInstallImages/{operator_prefix}{batch_name}/{operator_prefix}_{batch_name}_{release_version}/Disk%20Image/{operator_prefix}_{batch_name}_{release_version}.zip"
            destination = os.path.join(destination_folder,
                                        f"{operator_prefix}_{batch_name}_{release_version}.zip")
            thread = DownloadThread(url, destination)
            thread.progress_updated.connect(self.update_progress)
            thread.status_updated.connect(self.update_status)
            thread.finished.connect(self.download_finished)
            thread.start()
            self.threads.append(thread)

    def update_progress(self, file_name, downloaded, total_size):
        with self.download_lock:
            percent = int((downloaded / total_size) * 100) if total_size > 0 else 0
            self.progress_bar.setValue(self.progress_bar.value() + 1)
            self.status_label.setText(f"Downloading {file_name}... {percent}%")

    def update_status(self, file_name, status):
        with self.download_lock:
            if "Failed" in status:
                # Extract the error message and escape HTML special characters
                error_message = status.split(":", 1)[1].strip()
                escaped_message = error_message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                self.status_label.setText(
                    f"<font color='red'>{file_name}: Failed: {escaped_message}</font><br>")
            else:
                self.status_label.setText(f"{file_name}: {status}<br>")

    def download_finished(self, success):
        with self.download_lock:
            if success:
                self.successful_downloads += 1
            else:
                self.failed_downloads += 1
            if len(self.threads) == self.successful_downloads + self.failed_downloads:
                self.show_completion_message()

    def show_completion_message(self):
        self.status_label.setText(
            f"Download completed.<br>Successful downloads: {self.successful_downloads}<br>Failed downloads: {self.failed_downloads}")
        self.progress_bar.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())