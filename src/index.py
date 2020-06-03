from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.uic import loadUiType

from helpers.validators import is_url
from helpers.file_system import check_file_existance

import os
from os import path
import urllib.request
import sys

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "../ui/main.ui"))


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_ui()
        self.handle_buttons()

    def handle_ui(self):
        self.setFixedSize(615, 427)
        self.progressBar.setValue(0)
        self.UrlText.setText("https://files.wikicourses.net/c/c-c-basics.zip")

    def handle_buttons(self):
        self.NormalDownloadButton.clicked.connect(self.handle_normal_download)
        self.BrowseButton.clicked.connect(self.handle_browse_button)
        # self.YouTubeVideoDownloadButton.clicked.connect(self.handle_youtube_video_download)
        # self.PlayListDownloadButton.clicked.connect(self.handle_youtube_playlist_download)

    def handle_progress_bar(self, blocknum, blocksize, totalsize):
        downloaded = blocknum * blocksize
        self.DSizeLcd.display(downloaded / 1000000)
        self.TSizeLcd.display(totalsize / 1000000)
        if totalsize > 0:
            precent = downloaded * 100 // totalsize
        self.progressBar.setValue(precent)
        QApplication.processEvents()

    def handle_browse_button(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All files (*.*)")
        self.SaveLocationText.setText(save_location[0])

    def handle_youtube_video_download(self):
        pass

    def handle_youtube_playlist_download(self):
        pass

    def handle_normal_download(self):

        url = self.UrlText.text()
        save_location = self.SaveLocationText.text().strip()
        if not save_location:
            QMessageBox.warning(self, "Download Location", "Please Enter a download location")
            return
        if is_url(url):
            try:
                save_location += f".{url.split('.')[-1]}"
                urllib.request.urlretrieve(url, save_location, self.handle_progress_bar)
                QMessageBox.information(self, "Download Completed", "The Download finished")
            except Exception as e:
                QMessageBox.warning(self, "Download Error", f"The Download failed with exception {e}")


        else:
            QMessageBox.warning(self, "Invalid Url", "Please Enter a Valid url")


# https://aahmedsamy.me
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
